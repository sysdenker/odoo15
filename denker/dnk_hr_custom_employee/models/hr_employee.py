
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    # _order = 'job_sequence'

    # Sobreescribir que esta función no realice lo que establece odoo nativo
    @api.onchange('address_id')
    def _onchange_address(self):
        pass
        # self.work_phone = self.address_id.phone
        # self.mobile_phone = self.address_id.mobile

    def toggle_active(self):
        res = super(HrEmployee, self).toggle_active()
        for rec in self:
            if rec.job_id:
                rec.job_id._compute_vacantes_abiertas()
        return res

    @api.depends('fecha_1er_contrato')
    def _compute_termino_1er_contrato(self):
        for rec in self:
            if rec.fecha_1er_contrato:
                fecha_1er_contrato = fields.Datetime.from_string(rec.fecha_1er_contrato)
                if rec.tipo_nomina:
                    if rec.tipo_nomina != 'produccion':
                        contract_days = 90.0
                    else:
                        contract_days = 30.0
                    rec.termino_1er_contrato = fecha_1er_contrato + timedelta(days=contract_days)

    @api.depends('recruitment_history_ids', 'fecha_1er_contrato')
    def _compute_fecha_ingreso(self):
        for rec in self:
            if rec.recruitment_history_ids:
                employ_dates_list = []
                baja_dates_list = []
                administrative_leave_dates_list = []
                company_ids_list = []
                company_count = 0
                for recruitment_history_id in rec.recruitment_history_ids:
                    employ_dates_list.append(fields.Datetime.from_string(recruitment_history_id.employ_date))
                    administrative_leave_dates_list.append(fields.Datetime.from_string(recruitment_history_id.administrative_leave_date))
                    company_ids_list.append(recruitment_history_id.company_id)
                    if recruitment_history_id.administrative_leave_date:
                        baja_dates_list.append(recruitment_history_id.administrative_leave_date)
                    company_count += 1

                if employ_dates_list:
                    rec.fecha_ingreso_actual = fields.Datetime.to_string(max(employ_dates_list))
                    rec.company_id = company_ids_list[company_count - 1]
                    if len(baja_dates_list):
                        rec.fecha_baja_ultima = max(baja_dates_list)

                if company_count > 1:
                    rec.anterior_fecha_ingreso = employ_dates_list[company_count - 2]
                    rec.anterior_fecha_baja = administrative_leave_dates_list[company_count - 2]
                    rec.anterior_company_id = company_ids_list[company_count - 2]
                # Configurar la compañía actual del empleado, la úñtima
                rec.company_id = company_ids_list[company_count - 1]
            else:
                rec.fecha_ingreso_actual = rec.fecha_1er_contrato

    @api.depends('birthday')
    def _compute_age(self):
        for rec in self:
            if rec.birthday and rec.birthday <= fields.Date.today():
                rec.edad = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(rec.birthday)).years
            else:
                rec.edad = 0

    @api.depends('documentos_legales_ids', 'documentos_personales_ids')
    def _compute_employee_checklist(self):
        documentos_count = 0
        documentos_completados_count = 0
        documentos_legales_state = True

        if self.documentos_legales_ids:
            for documentos_legal_id in self.documentos_legales_ids:
                documentos_count += 1
                if documentos_legal_id.state is True:
                    documentos_completados_count += 1
                elif documentos_legal_id.name.required:
                    documentos_legales_state = False
        self.documentos_legales_state = documentos_legales_state

        documentos_personales_state = True
        if self.documentos_personales_ids:
            for documentos_personal_id in self.documentos_personales_ids:
                documentos_count += 1
                if documentos_personal_id.state is True:
                    documentos_completados_count += 1
                elif documentos_personal_id.name.required:
                    documentos_personales_state = False
        self.documentos_personales_state = documentos_personales_state
        if documentos_count != 0:
            self.documentos_porcentaje_completado = (documentos_completados_count / documentos_count) * 100
        else:
            self.documentos_porcentaje_completado = 0.00

    # Campos originales que se les modificó algún atributo
    active = fields.Boolean('Active', related='resource_id.active', default=True, store=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], groups="hr.group_hr_user", default="male", required=True,  ondelete='cascade')
    birthday = fields.Date('Date of Birth', groups="hr.group_hr_user")
    job_id = fields.Many2one('hr.job', 'Job Position', required=True)
    # job_sequence = fields.Integer(string='- Job Sequence', related='job_id.sequence', store=True)
    resource_calendar_id = fields.Many2one(
        'resource.calendar', 'Working Hours',
        default=lambda self: self.env['res.company']._company_default_get().resource_calendar_id,
        index=True, related='resource_id.calendar_id', required=True)
    ############################################################################

    no_empleado = fields.Char('- Número de empleado', groups='hr.group_hr_user', copy=False)
    tipo_pago = fields.Selection(selection=[
        ('transferencia', 'Transferencia'),
        ('efectivo', 'Efectivo'),
        ('deposito', 'Deposito')],
        string='- Tipo de Pago',
        groups='hr.group_hr_user',
    )
    banco = fields.Many2one('res.bank', '- Banco', groups='hr.group_hr_user')
    no_cuenta = fields.Char('- No. cuenta', groups='hr.group_hr_user')
    rfc = fields.Char('- RFC', groups='hr.group_hr_user')
    curp = fields.Char('- CURP', groups='hr.group_hr_user')
    segurosocial = fields.Char('- Seguro social', groups='hr.group_hr_user')
    correo_electronico = fields.Char('- Correo electrónico', groups='hr.group_hr_user')

    regimen = fields.Selection(
        selection=[('02', '02 - Sueldos'),
                   ('03', '03 - Jubilados'),
                   ('04', '04 - Pensionados'),
                   ('05', '05 - Asimilados Miembros Sociedades Cooperativas Produccion'),
                   ('06', '06 - Asimilados Integrantes Sociedades Asociaciones Civiles'),
                   ('07', '07 - Asimilados Miembros consejos'),
                   ('08', '08 - Asimilados comisionistas'),
                   ('09', '09 - Asimilados Honorarios'),
                   ('10', '10 - Asimilados acciones'),
                   ('11', '11 - Asimilados otros'),
                   ('12', '12 - Jubilados o Pensionados'),
                   ('13', '13 - Indemnización o Separación'),
                   ('99', '99 - Otro Regimen'), ],
        string=_('- Régimen'),
        groups='hr.group_hr_user'
    )
    contrato = fields.Selection(
        selection=[('01', '01 - Contrato de trabajo por tiempo indeterminado'),
                   ('02', '02 - Contrato de trabajo para obra determinada'),
                   ('03', '03 - Contrato de trabajo por tiempo determinado'),
                   ('04', '04 - Contrato de trabajo por temporada'),
                   ('05', '05 - Contrato de trabajo sujeto a prueba'),
                   ('06', '06 - Contrato de trabajo con capacitación inicial'),
                   ('07', '07 - Modalidad de contratación por pago de hora laborada'),
                   ('08', '08 - Modalidad de trabajo por comisión laboral'),
                   ('09', '09 - Modalidades de contratación donde no existe relación de trabajo'),
                   ('10', '10 - Jubilación, pensión, retiro'),
                   ('99', '99 - Otro contrato'), ],
        string=_('- Contrato'),
        groups='hr.group_hr_user'
    )

    jornada = fields.Selection(
        selection=[('01', '01 - Diurna'),
                   ('02', '02 - Nocturna'),
                   ('03', '03 - Mixta'),
                   ('04', '04 - Por hora'),
                   ('05', '05 - Reducida'),
                   ('06', '06 - Continuada'),
                   ('07', '07 - Partida'),
                   ('08', '08 - Por turnos'),
                   ('99', '99 - Otra Jornada'), ],
        string=_('- Jornada'),
        groups='hr.group_hr_user'
    )
    estado = fields.Many2one('res.country.state', '- Lugar donde labora (Estado)', groups='hr.group_hr_user')
    fondo_ahorro = fields.Float(string=_('- Fondo de ahorro'), readonly=True, groups='hr.group_hr_user')
    dias_utilidad = fields.Float(string='- Dias para cálculo de Utilidad', groups='hr.group_hr_user')
    sueldo_utilidad = fields.Float(string='- Sueldo para cálculo de Utilidad', groups='hr.group_hr_user')
    fecha_utilidad_inicio = fields.Date(readonly=True, groups='hr.group_hr_user')
    fecha_utilidad_fin = fields.Date(readonly=True, groups='hr.group_hr_user')

    ############################################################################
    """ Reeplazado por Degree (type_id) hr.recruitment.degree
    nivel_estudios = fields.Selection(
        selection=[('sin_estudio', 'Sin estudio'),
                   ('primaria', 'Primaria'),
                   ('secundaria', 'Secundaria'),
                   ('bachillerato', 'Bachillerato'),
                   ('licenciatura', 'Licenciatura'),
                   ('posgrado', 'Posgrado'),],
        string=_('- Nivel de estudios'),
    )"""
    type_id = fields.Many2one('hr.recruitment.degree', "- Degree", groups='hr.group_hr_user')
    edad = fields.Integer(
        string='- Edad',
        compute='_compute_age',
        help='Edad calculada a partir de la fecha de naciemiento',
        groups='hr.group_hr_user')
    extension_telefonica = fields.Char(
        string='- Extension telefónica', required=False,
        help='Extensión telefónica del empleado',
        groups='hr.group_hr_user')
    tiene_credito_infonavit = fields.Boolean(string='- ¿Tiene crédito Infonavit?', groups='hr.group_hr_user')
    numero_credito_infonavit = fields.Char(string='- No. crédito Infonavit', size=16, groups='hr.group_hr_user')
    tiene_credito_fonacot = fields.Boolean(string='- ¿Tiene crédito Fonacot?', groups='hr.group_hr_user')
    numero_credito_fonacot = fields.Char(string='- No. crédito Fonacot', size=16, groups='hr.group_hr_user')
    fecha_1er_contrato = fields.Date(
        string='- 1er Contrato',
        help='Fecha del primer contrato',
        groups='hr.group_hr_user')
    termino_1er_contrato = fields.Date(
        string='- Termino 1er Contrato', required=False,
        compute='_compute_termino_1er_contrato', store=True, readonly=False,
        help='Fecha de Término del primer contrato',
        groups='hr.group_hr_user')
    fecha_planta_contrato = fields.Date(
        string='- Contrato Planta', required=False,
        help='Fecha del tercer contrato',
        groups='hr.group_hr_user')
    fecha_ingreso_actual = fields.Date(
        string='- Fecha de Ingreso', readonly=True,
        compute='_compute_fecha_ingreso', store=True,
        help='Fecha de Ingreso del empleado',
        groups='hr.group_hr_user')
    fecha_baja_ultima = fields.Date(
        string='- Fecha de Baja', readonly=True, compute='_compute_fecha_ingreso', store=True,
        help='Fecha de Baja del empleado',
        groups='hr.group_hr_user')
    anterior_fecha_ingreso = fields.Date(
        string='- Fecha de Ingreso Anterior', readonly=True,
        compute='_compute_fecha_ingreso', store=True,
        help='Fecha de Ingreso del empleado',
        groups='hr.group_hr_user')
    anterior_fecha_baja = fields.Date(
        string='- Fecha de Baja Anterior', readonly=True,
        compute='_compute_fecha_ingreso', store=True,
        help='Fecha de Ingreso del empleado',
        groups='hr.group_hr_user')
    anterior_company_id = fields.Many2one(
        'res.company', string='- Compañía Anterior',
        compute='_compute_fecha_ingreso', store=True,
        groups='hr.group_hr_user')
    recruitment_history_ids = fields.One2many(
        comodel_name='hr.employee.recruitment.history',
        inverse_name='employee_id', string='- Historial de reclutamiento',
        help='Para tener un historial de inicio y fin de reclutamiento en cada compañía',
        groups='hr.group_hr_user')
    contacto_emergencia = fields.Char(string='- Contacto de Emergencia', size=32, copy=False, groups='hr.group_hr_user')
    telefono_emergencia = fields.Char(string='- Teléfono de emergencia', size=16, copy=False, groups='hr.group_hr_user')
    sangre_tipo = fields.Selection(
        selection=[('AB+', 'AB+'),
                   ('AB-', 'AB-'),
                   ('A+', 'A+'),
                   ('A-', 'A-'),
                   ('B+', 'B+'),
                   ('B-', 'B-'),
                   ('O+', 'O+'),
                   ('O-', 'O-'), ],
        string='- Tipo de Sangre',
        groups='hr.group_hr_user'
    )
    tipo_nomina = fields.Selection(
        selection=[('administrativo', 'Administrativo'),
                   ('produccion', 'Producción'), ],
        string='- Tipo de Nómina',
        groups='hr.group_hr_user'
    )
    medium_id = fields.Many2one(
        'utm.medium',
        string='- Medio de reclutamiento', groups='hr.group_hr_user')
    source_id = fields.Many2one(
        'utm.source',
        string='- Fuente de reclutamiento', groups='hr.group_hr_user')
    reference = fields.Many2one(
        'hr.employee',
        string='- Recomendado por', copy=False,
        help='Persona quién recomendó a este empleado',
        groups='hr.group_hr_user')
    # Campos para control de Documentos
    documentos_porcentaje_completado = fields.Float(
        string="- Porcentaje Completado", store=True,
        compute=_compute_employee_checklist,
        default=0.00, groups='hr.group_hr_user')
    documentos_legales_state = fields.Boolean(
        string='- Documentos Legales', store=True,
        help='If checked, all required points was verified by the hr user',
        compute=_compute_employee_checklist,
        default=False,
        groups='hr.group_hr_user')
    documentos_legales_ids = fields.One2many(
        comodel_name='hr.employee.checklist',
        inverse_name='employee_id',
        string='- Documentos Legales', copy=False,
        domain=[('category_id', '=', 'Documentos Legales')],
        groups='hr.group_hr_user')
    documentos_personales_state = fields.Boolean(
        string='- Documentos Personales', store=True,
        help='If checked, all required points was verified by the hr user',
        compute=_compute_employee_checklist, groups='hr.group_hr_user', default=False)
    documentos_personales_ids = fields.One2many(
        comodel_name='hr.employee.checklist',
        inverse_name='employee_id',
        string='- Documentos Personales', copy=False,
        domain=[('category_id', '=', 'Documentos Personales')],
        groups='hr.group_hr_user')
    beneficiary_ids = fields.One2many(
        comodel_name='hr.employee.beneficiary',
        inverse_name='employee_id',
        string='- Designación de Beneficiarios',
        copy=False, groups='hr.group_hr_user')

    # UNIFORMES Y ZAPATO
    talla_camisa_blusa = fields.Selection(
        selection=[('xch', 'XCH'),
                   ('ch', 'CH'),
                   ('m', 'M'),
                   ('g', 'G'),
                   ('xg', 'XG'),
                   ('xxg', 'XXG'),
                   ('xxxg', 'XXXG'), ],
        string='- Camisa/blusa',
        groups='hr.group_hr_user'
    )
    talla_playera_polo = fields.Selection(
        selection=[('xch', 'XCH'),
                   ('ch', 'CH'),
                   ('m', 'M'),
                   ('g', 'G'),
                   ('xg', 'XG'),
                   ('xxg', 'XXG'),
                   ('xxxg', 'XXXG'), ],
        string='- Playera polo',
        groups='hr.group_hr_user'
    )
    talla_playera_cuello_redondo = fields.Selection(
        selection=[('xch', 'XCH'),
                   ('ch', 'CH'),
                   ('m', 'M'),
                   ('g', 'G'),
                   ('xg', 'XG'),
                   ('xxg', 'XXG'),
                   ('xxxg', 'XXXG'), ],
        string='- Playera cuello redondo',
        groups='hr.group_hr_user'
    )
    talla_zapato_industrial = fields.Char(
        string='Zapato Indistrial', size=2,
        groups='hr.group_hr_user')

    @api.model
    def create(self, vals):
        ChecklistLines = self.env['hr.employee.checklist.line'].search([('category_id', '=', 'Documentos Legales')])
        documentos_legales_list = []
        for ChecklistLine in ChecklistLines:
            new_documento_legal = (0, 0, {'name': ChecklistLine.id})
            documentos_legales_list.append(new_documento_legal)

        ChecklistLines = self.env['hr.employee.checklist.line'].search([('category_id', '=', 'Documentos Personales')])
        documentos_personales_list = []
        for ChecklistLine in ChecklistLines:
            new_documento_personal = (0, 0, {'name': ChecklistLine.id})
            documentos_personales_list.append(new_documento_personal)

        vals.update({'documentos_legales_ids': documentos_legales_list, 'documentos_personales_ids': documentos_personales_list, })
        res = super(HrEmployee, self).create(vals)
        return res

    def contract_fields_validate(self):
        if not self.fecha_1er_contrato:
            raise UserError(_('The following field is invalid: 1er Contrato'))

        """o.employee_id.fecha_ingreso_actual
        o.employee_id.resource_calendar_id.dnk_tiempo_comida

        o.employee_id.address_home_id (Private Address)
        o.employee_id.address_home_id.street_name
        o.employee_id.address_home_id.street_number
        o.employee_id.address_home_id.street_number2
        o.employee_id.address_home_id.l10n_mx_edi_colony
        o.employee_id.address_home_id.zip
        o.employee_id.address_home_id.city
        o.employee_id.address_home_id.state_id

        o.employee_id.address_id.l10n_mx_edi_locality
        o.employee_id.address_id.l10n_mx_edi_locality
        o.employee_id.address_id.state_id"""

        action = self.env.ref('hr_contract.act_hr_employee_2_hr_contract').read()[0]
        return action


class EmployeeChecklist(models.Model):
    _name = 'hr.employee.beneficiary'
    _description = '- Beneficiarios'

    name = fields.Char(string='- Nombre Completo', required=True)
    relationship = fields.Many2one(
        'hr.family.connection',
        string='- Parentesco', required=True)
    percentage = fields.Float(string=_('- Porcentaje'), digits=(3, 2), required=True)
    employee_id = fields.Many2one('hr.employee', string='- Employee')


class EmployeeChecklist(models.Model):
    _name = 'hr.family.connection'
    _description = '- Relación'

    name = fields.Char(string='- Nombre')


class EmployeeChecklist(models.Model):
    _name = 'hr.employee.checklist'
    _description = 'Employee checklist'
    # _order = 'sequence'

    name = fields.Many2one('hr.employee.checklist.line', '- Point')
    category_id = fields.Many2one('hr.employee.checklist.category', '- Category', related='name.category_id')
    sequence = fields.Integer('- Sequence', related='name.sequence', help="Orden del checklist.")
    employee_id = fields.Many2one('hr.employee', '- Employee')
    description = fields.Char(string='-Description', related='name.description', readonly=True)
    state = fields.Boolean(
        string='- State',
        help='If checked, the point was verified by the hr user',
        default=False)

    _sql_constraints = [
        ('number_uniq', 'unique(name, employee_id)', "Checklist Line Already Exists in this Employee!"),
    ]


class EmployeeChecklistCategory(models.Model):
    _name = 'hr.employee.checklist.category'
    _description = 'Employee checklist category'

    name = fields.Char(string='- Category')
    sequence = fields.Integer('- Sequence', help="Orden de la categorías de checklist.")


class EmployeeChecklist(models.Model):
    _name = 'hr.employee.checklist.line'
    _description = 'Employee checklist line'

    name = fields.Char(string='- Line')
    description = fields.Char(string='- Description')
    sequence = fields.Integer('- Sequence', help='Orden de la categoría de checklist.')
    category_id = fields.Many2one('hr.employee.checklist.category', '- Category', required=True)
    required = fields.Boolean(
        string='- Required', help='If checked, this line is required', default=True)

    def unlink(self):
        # Delete all hr.employee.checklist related to this line
        for checklist_line in self:
            checklists = self.env['hr.employee.checklist'].search([('name', '=', checklist_line.id)])
            for checklist in checklists:
                checklist.unlink()

        return super(EmployeeChecklist, self).unlink()

    @api.model
    def create(self, vals):
        res = super(EmployeeChecklist, self).create(vals)

        # (0, 0,  { values })    link to a new record that needs to be created with the given values dictionary
        # (1, ID, { values })    update the linked record with id = ID (write *values* on it)
        # (2, ID)                remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)
        # (3, ID)                cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)
        # (4, ID)                link to existing record with id = ID (adds a relationship)
        # (5)                    unlink all (like using (3,ID) for all linked records)
        # (6, 0, [IDs])          replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
        employee_ids = self.env['hr.employee'].search([])
        for employee_id in employee_ids:
            reg = self.env['hr.employee.checklist'].create({'name': res.id, 'employee_id': employee_id.id, })

        return res


class EmployeeRecruitmentHistory(models.Model):
    _name = 'hr.employee.recruitment.history'
    _description = 'Employee recruitment history'
    _order = 'employ_date'

    employee_id = fields.Many2one('hr.employee', '- Employee', required=True)
    company_id = fields.Many2one('res.company', string='- Company', required=True)
    employ_date = fields.Date(string='- Fecha de Ingreso', required=True)
    administrative_leave_date = fields.Date(string='- Fecha de Baja')
    leave_cause_id = fields.Many2one(
        'hr.employee.leave.cause',
        string='- Motivo de Baja',
        required=False)


"""
Ya no se necesita ya que se usó el modelo "xxx" del módulo recruitment
class EmployeeRecruitmentSource(models.Model):
    _name = 'hr.employee.recruitment.source'
    _description = 'Fuente de reclutamiento'

    # Por ejemplo: OCC, Computrabajo, Recomendado
    name = fields.Char(
        string='Nombre',
        size=16)

security csv
access_hr_employee_recruitment_source_user,hr.employee.recruitment.source,model_hr_employee_recruitment_source,hr.group_hr_user,1,0,0,0
access_hr_employee_recruitment_source_manager,hr.employee.recruitment.source,model_hr_employee_recruitment_source,hr.group_hr_manager,1,1,1,1

"""
