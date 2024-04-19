# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from .amount_to_text_es_MX import amount_to_text
import datetime
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import locale
import logging
_logger = logging.getLogger(__name__)


class Contract(models.Model):
    _inherit = "hr.contract"

    def format_date(self, dt, format=False):
        # lang = self.env.context['lang']
        lang = 'es_ES'
        locale.setlocale(locale.LC_TIME, lang + '.utf8')
        if format:
            timestamp = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S').strftime(format)
        else:
            timestamp = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S').strftime(tools.DEFAULT_SERVER_DATETIME_FORMAT)
        return timestamp

    @api.depends('sueldo_diario')
    def _compute_desde_sueldo_diario(self):
        for rec in self:
            if rec.sueldo_diario:
                rec.sueldo_diario_palabras = amount_to_text().amount_to_text_cheque(rec.sueldo_diario, 'pesos', 'M. N.')
                rec.bono_asistencia = rec.sueldo_diario * 30 * 0.1
                rec.bono_puntualidad = rec.bono_asistencia
                rec.fondo_ahorro = rec.sueldo_diario * 30 * 0.033

    @api.depends('total_vales_despensa')
    def _compute_total_vales_despensa(self):
        for rec in self:
            if rec.total_vales_despensa:
                rec.total_vales_despensa_palabras = amount_to_text().amount_to_text_cheque(rec.total_vales_despensa, 'pesos', 'M. N.')

    @api.depends('periodicidad_pago')
    def _compute_ciclo_pago(self):
        for rec in self:
            if rec.periodicidad_pago:
                switcher = {
                    '01': 'día',
                    '02': 'semana',
                    '03': 'catorcena',
                    '04': 'quincena',
                    '05': 'mes',
                    '06': 'bimestre',
                    '07': 'obra',
                    '08': 'comisión',
                    '09': 'precio alzado',
                    '10': 'pago por consignación',
                    '99': 'indefinido',
                }
                rec.ciclo_pago = switcher[rec.periodicidad_pago]
                if rec.ciclo_pago == 'semana':
                    rec.total_vales_despensa = 180
                elif rec.ciclo_pago == 'quincena':
                    rec.total_vales_despensa = 360

    periodicidad_pago = fields.Selection(
        selection=[('01', 'Diario'),
                   ('02', 'Semanal'),
                   ('03', 'Catorcenal'),
                   ('04', 'Quincenal'),
                   ('05', 'Mensual'),
                   ('06', 'Bimensual'),
                   ('07', 'Unidad obra'),
                   ('08', 'Comisión'),
                   ('09', 'Precio alzado'),
                   ('10', 'Pago por consignación'),
                   ('99', 'Otra periodicidad'), ],
        string=_('Periodicidad de pago CFDI'),
    )
    ciclo_pago = fields.Selection(
        selection=[('día', 'Día'),
                   ('semana', 'Semana'),
                   ('catorcena', 'Catorcena'),
                   ('quincena', 'Quincena'),
                   ('mes', 'Mes'),
                   ('bimestre', 'Bimestre'),
                   ('obra', 'Obra'),
                   ('comisión', 'Comisión'),
                   ('precio alzado', 'Precio alzado'),
                   ('pago por consignación', 'Pago por consignación'),
                   ('indefinido', 'Otra periodicidad'), ],
        string=_('Ciclo de pago CFDI'), compute='_compute_ciclo_pago', store=True,
    )

    riesgo_puesto = fields.Selection(
        selection=[('1', 'Clase I'),
                   ('2', 'Clase II'),
                   ('3', 'Clase III'),
                   ('4', 'Clase IV'),
                   ('5', 'Clase V'),
                   ('99', 'No aplica'), ],
        string=_('Riesgo del puesto'),
    )
    sueldo_diario = fields.Monetary(
        'Sueldo diario', currency_field='company_currency_id',
        help="Salario diario en la moneda de la compañía a la que pertenece el empleado.")
    sueldo_hora = fields.Monetary(
        'Sueldo por hora', currency_field='company_currency_id')
    sueldo_diario_integrado = fields.Monetary(
        'Sueldo diario integrado', currency_field='company_currency_id')
    sueldo_base_cotizacion = fields.Monetary('Sueldo base cotización', currency_field='company_currency_id')
    tablas_cfdi_id = fields.Many2one('tablas.cfdi', 'Tabla CFDI')

    bono_productividad = fields.Monetary(
        'Bono productividad', currency_field='company_currency_id', help="Bono de asistencia asignado al empleado.")
    bono_asistencia = fields.Monetary(
        'Bono asistencia', compute='_compute_desde_sueldo_diario', readonly=True, store=True,
        currency_field='company_currency_id', help="Bono de asistencia asignado al empleado.")
    bono_puntualidad = fields.Monetary(
        'Bono puntualidad', compute='_compute_desde_sueldo_diario', readonly=True, store=True,
        currency_field='company_currency_id', help="Bono de puntualidad asignado al empleado.")
    fondo_ahorro = fields.Monetary(
        'Fondo de ahorro', compute='_compute_desde_sueldo_diario', readonly=True, store=True,
        currency_field='company_currency_id', help="Fondo de ahorro asignado al empleado.")

    infonavit_fijo = fields.Float('Infonavit (fijo)')
    infonavit_vsm = fields.Float('Infonavit (vsm)')

    infonavit_porc = fields.Float('Infonavit (%)')
    anticipo_sueldo = fields.Float('Anticipo sueldo')
    deduc_gral = fields.Float('Dedudcion general')
    prestamo_fonacot = fields.Float('Prestamo FONACOT')
    pago_de_serv = fields.Float('Pago de servicio')
    pens_alim = fields.Float('Pensión alimienticia')
    prest_financ = fields.Float('Prestamo financiero')
    prevision_social = fields.Monetary('Prevision Social', currency_field='company_currency_id',)
    dias_aguinaldo = fields.Float(string=_('Días de aguinaldo'), default='15')
    antiguedad_anos = fields.Float('Años de antiguedad', readonly=True)
    dias_base = fields.Float('Días base', default='90')
    dias_x_ano = fields.Float('Días por cada año trabajado', default='20')
    dias_totales = fields.Float('Total de días', readonly=True)
    indemnizacion = fields.Boolean("Indemnizar al empleado")
    dias_pendientes_pagar = fields.Float('Días a pagar')
    dias_vacaciones = fields.Float('Días de vacaciones')

    # ***************************** GRUPO DENKER ******************************
    company_currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', string="Company Currency", readonly=True,
        help='Utility field to express amount currency', store=True)
    sueldo_diario_palabras = fields.Char(
        string='- Sueldo Diario en Palabras', compute='_compute_desde_sueldo_diario', store=True,
        help='Certificate of incorporation date text')
    total_vales_despensa = fields.Monetary(
        string="- Vales de Despensa", compute='_compute_ciclo_pago', readonly=True, store=True,
        currency_field='company_currency_id', help="Total de Vales de Despensa asignado al empleado.")
    total_vales_despensa_palabras = fields.Char(
        string='- Total de Vales de Despensa en Palabras', compute='_compute_total_vales_despensa', store=True,
        help='Total de Vales de Despensa en palabras asignado al empleado.')
    ingreso_bruto = fields.Monetary(
        string="- Ingreso Bruto", currency_field='company_currency_id',
        help="Ingreso bruto se refiere a la cantidad de dinero que le queda después de contabilizar impuestos, créditos y otras deducciones.")
    ingreso_neto = fields.Monetary(
        string="- Ingreso Neto", currency_field='company_currency_id',
        help="Es el dinero final que llega al trabajador luego de hacer los respectivos descuentos de nómina (aportes obligatorios, impuestos, entre otros).")
    # ***************************************************************************

    @api.onchange('wage')
    def _compute_sueldo(self):
        if self.wage:
            values = {
                'sueldo_diario': self.wage / 30,
                'sueldo_hora': self.wage / 30 / 8,
                'sueldo_diario_integrado': self.calculate_sueldo_diario_integrado(),
            }
            self.update(values)

#    @api.depends('dias_base', 'dias_x_ano', 'antiguedad_anos')
#    def _dias_totales(self):
#        self.dias_totales = self.antiguedad_anos * self.dias_x_ano + self.dias_base

    def calcular_liquidacion(self):
        if self.date_end:
            date_start = datetime.strptime(self.date_start, "%Y-%m-%d")
            date_end = datetime.strptime(self.date_end, "%Y-%m-%d")
            diff_date = date_end - date_start
            years = diff_date.days / 365.0
            self.antiguedad_anos = int(years)
            self.dias_totales = self.antiguedad_anos * self.dias_x_ano + self.dias_base

    def button_dummy(self):
        self.calcular_liquidacion()
        return True

    @api.model
    def calculate_sueldo_diario_integrado(self):
        for rec in self:
            if rec.date_start:
                # date_start = datetime.strptime(rec.date_start, "%Y-%m-%d")
                date_start = rec.date_start
                today = datetime.today().date()
                print("FECHAS ", date_start, today)
                diff_date = today - date_start
                print("DATE DIFF", diff_date)
                years = diff_date.days / 365.0
                tablas_cfdi = self.tablas_cfdi_id
                if not tablas_cfdi:
                    tablas_cfdi = self.env['tablas.cfdi'].search([], limit=1)
                if not tablas_cfdi:
                    return
                if years < 1.0:
                    tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad >= years).sorted(key=lambda x: x.antiguedad)
                else:
                    tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad <= years).sorted(key=lambda x: x.antiguedad, reverse=True)
                if not tablas_cfdi_lines:
                    return
                tablas_cfdi_line = tablas_cfdi_lines[0]
                max_sdi = tablas_cfdi.uma * 25
                sdi = ((365 + tablas_cfdi_line.aguinaldo + (tablas_cfdi_line.vacaciones) * (tablas_cfdi_line.prima_vac / 100)) / 365) * self.wage / 30
                if sdi > max_sdi:
                    sueldo_diario_integrado = max_sdi
                else:
                    sueldo_diario_integrado = sdi
                    # _logger.info('sueldo_diario_integrado ... %s max_sdi %s', tablas_cfdi.uma, max_sdi)
            else:
                sueldo_diario_integrado = 0
            return sueldo_diario_integrado
