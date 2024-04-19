# -*- coding: utf-8 -*-
import pytz
from datetime import datetime,date, timedelta
from odoo import api, fields, models
from workalendar.america import Mexico

class DnkHrAttendance(models.Model):
    _inherit = 'hr.attendance'

    dnk_device_user_id = fields.Integer(string='Biometric Device User ID')
    dnk_device_id = fields.Many2one('dnk.zk.machine', string='Device')
    check_in = fields.Datetime(string="Check In", default=fields.Datetime.now, required=False)
    dnk_attendance_stat = fields.Char(string='- Status', help='Attendance Status')

    # @api.constrains('check_in', 'check_out', 'employee_id')
    # def _check_validity(self):
    #    res = super(DnkHrAttendance, self)._check_validity()



    @api.model
    def cron_create_default_attendance_data(self):
        print ("++++++++++++Cron Executed++++++++++++++++++++++")
        self.dnk_crate_att()


    def dnk_create_att_from_date(self, ini_date=False, end_date=False):
        print ("++++++++++++dnk_create_att_from_date++++++++++++++++++++++")
        if ini_date is False:
            return False
        if end_date is False:
            end_date = date.today().strftime('%Y-%m-%d')

        ini_date_obj = datetime.strptime(ini_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        days = end_date_obj-ini_date_obj
        for dia in range (0,days.days+1):
            attendance_date = ini_date_obj + timedelta(days=dia)
            print (attendance_date)
            self.dnk_crate_att(attendance_date.strftime('%Y-%m-%d'))

    def dnk_crate_att(self, ini_date=False):
        print ("++++++++++++dnk_crate_att++++++++++++++++++++++")
        if ini_date is False:
            ini_date = date.today().strftime('%Y-%m-%d')
        ini_datetime = datetime.strptime(ini_date + " 00:00:01",'%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(ini_date + " 23:59:59",'%Y-%m-%d %H:%M:%S')
        local_tz = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
        local_ini_dt = local_tz.localize(ini_datetime, is_dst=None)
        local_end_dt = local_tz.localize(end_datetime, is_dst=None)
        utc_dt = local_ini_dt.astimezone(pytz.utc)
        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
        ini_date_utc = datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
        utc_dt = local_end_dt.astimezone(pytz.utc)
        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
        end_date_utc = datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
        week_day = ini_datetime.weekday()

        hr_employees = self.env['hr.employee']
        employee_ids = hr_employees.search([('active', '=', True), ('dnk_device_user_id', '!=',False)])
        dnk_attendance_stat = ""
        print(len(employee_ids))
        for employee in employee_ids:
            # print("employee.id",employee.id)
            # print("ini_date_utc", ini_date_utc)
            # print("end_date_utc", end_date_utc)
            # print("ini_datetime", ini_datetime)
            # print("end_datetime", end_datetime)
            # search_att = self.search([('employee_id', '=', employee.id),('check_in', '>=', ini_date_utc.strftime("%Y-%m-%d %H:%M:%S")),('check_in', '<=', end_date_utc.strftime("%Y-%m-%d %H:%M:%S"))])
            search_att = self.search([('employee_id', '=', employee.id),('check_in', '>=', ini_datetime),('check_in', '<=', end_datetime)])
            # print("Búsqueda en attendace no en checador", search_att)
            if search_att:
                continue
            calendar_att =  self.env['resource.calendar.attendance'].search([('calendar_id', '=', employee.resource_calendar_id.id),('dayofweek', '=',week_day)],limit=1)
            if calendar_att:
                holydaysmex = Mexico()
                Leaves = self.env['hr.leave'].search(
                    [('employee_id', '=', employee.id), ('state', 'in', ['validate','validate1']),
                    ('date_from', '>=', ini_date_utc), ('date_to', '<=', end_datetime)])

                if employee.birthday and datetime.strftime(employee.birthday, '%m-%d') == ini_date[5:10]:
                    # print ("Fechas cumpleaños",datetime.strftime(employee.birthday, '%m-%d'), ini_date[5:10])
                    dnk_attendance_stat = "Cumpleaños"
                elif Leaves:
                    # print("Sí hay vacaciones", Leaves)
                    dnk_attendance_stat = "Vacaciones"
                elif holydaysmex.is_working_day(datetime.strptime(ini_date,'%Y-%m-%d')):
                    dnk_attendance_stat = "Ausencia"
                elif week_day in (5,6):
                    dnk_attendance_stat = "Ausencia"
                else:
                    dnk_attendance_stat = "Festivo"
            else :
                dnk_attendance_stat = "Descanso"

            self.create({
                'employee_id': employee.id,
                'check_in':ini_date_utc,
                'check_out':ini_date_utc,
                'dnk_device_id':False,
                'dnk_device_user_id':employee.dnk_device_user_id,
                'dnk_attendance_stat':dnk_attendance_stat})


    def dnk_update_attendance(self, ini_date=False, end_date=False):
        # print("Ya entre a la función de las asistencias")
        #Ya no lo haré de los dispositivos, pediré la función y si no recibo, actualizaré la del día
        if not ini_date:
            ini_date = date.today().strftime('%Y-%m-%d')
        if not end_date:
            end_date = date.today().strftime('%Y-%m-%d')

        # min_date  = device.zk_after_date if device.zk_after_date else "2021-10-01 00:00:00"
        # device_id =device.id if device.id else False
        # str_ini_date = datetime.strftime(datetime.strptime(min_date,'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d')
        # str_ini_date = datetime.strftime(min_date, '%Y-%m-%d')
        # str_end_date = datetime.now().strftime('%Y-%m-%d')
        ini_date = datetime.strptime(ini_date,'%Y-%m-%d').date()
        #ini_date_ts = datetime.strptime(min_date,'%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date,'%Y-%m-%d').date()
        days = end_date-ini_date

        # print("ini_date",ini_date)
        # print("end_date",end_date)
        # print("days",days.days+1)
        self._cr.execute("SELECT DISTINCT(dnk_device_user_id) FROM dnk_machine_attendance WHERE punching_time_utc > %s", [ini_date])
        for user in self.env.cr.fetchall():
            hr_employees = self.env['hr.employee']
            employee = hr_employees.search([('dnk_device_user_id', 'in', user)])
            # employee = hr_employees.search([('no_empleado', '=', user[0])])
            if employee:
                print(employee)
                for dia in range (0,days.days+1):
                    print("día:", dia)
                    attendance_date = ini_date + timedelta(days=dia)
                    week_day = attendance_date.weekday()
                    ini_dia = attendance_date.strftime('%Y-%m-%d') + " 00:00:00"
                    fin_dia = attendance_date.strftime('%Y-%m-%d') + " 23:59:59"
                    #Tengo que transformarla a UTC
                    local_tz = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
                    local_dt = local_tz.localize(datetime.strptime(ini_dia, '%Y-%m-%d %H:%M:%S'), is_dst=None)
                    utc_dt = local_dt.astimezone(pytz.utc)
                    utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                    ini_dia_utc = datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
                    local_dt = local_tz.localize(datetime.strptime(fin_dia, '%Y-%m-%d %H:%M:%S'), is_dst=None)
                    utc_dt = local_dt.astimezone(pytz.utc)
                    utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                    fin_dia_utc = datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")

                    self._cr.execute(
                                """SELECT  MIN(punching_time_utc) as check_in, MAX(punching_time_utc) AS check_out, COUNT(*) AS total
                                  FROM dnk_machine_attendance
                                  WHERE punching_time_utc BETWEEN %s AND %s
                                  AND dnk_device_user_id = %s""", [ini_dia_utc,fin_dia_utc,user[0]])
                    for attendance in self.env.cr.fetchall():
                        regs = attendance[2]
                        inicio = attendance[0]
                        fin = attendance[1]
                        dnk_device_id = self.env['dnk.machine.attendance'].search([('dnk_device_user_id', '=', user[0]),('punching_time_utc', '=',inicio)],limit=1).dnk_device_id
                        #print ("Registros", regs, "Inicio:", inicio,  "Fin:",fin)
                        if regs < 1:
                            #Se supone que no hay registro en checador, tons ps no hago nada
                            continue
                        # Voy a buscar el registro de asistencia del día, para actualizarlo porque se supone que ya siempre habrá uno
                        # pero en hr_attendance el check in y check out no tienen zona horaria, tons se lo tengo que quitar para buscarla :(.

                        # ini_datetime = datetime.strptime(inicio,'%Y-%m-%d %H:%M:%S')
                        # end_datetime = datetime.strptime(fin,'%Y-%m-%d %H:%M:%S')
                        ini_datetime = inicio
                        end_datetime = fin
                        search_att = self.search([('employee_id', '=', employee.id),('check_in', '>=', ini_dia_utc.strftime("%Y-%m-%d %H:%M:%S")),('check_out', '<=', fin_dia_utc.strftime("%Y-%m-%d %H:%M:%S"))])
                        if search_att :

                            if search_att.check_in != inicio:
                                #Actualizar, en teoría, la asistencia encontrada es la automática, entonces tengo que actualizar todos los campos
                                calendar_att =  self.env['resource.calendar.attendance'].search([('calendar_id', '=', employee.resource_calendar_id.id),('dayofweek', '=',week_day)],limit=1)
                                if calendar_att:
                                        calendar_hour_in = ini_dia_utc + timedelta(hours=calendar_att.hour_from)
                                        calendar_hour_in = calendar_hour_in + timedelta(minutes=1)
                                        if calendar_hour_in >= ini_datetime:
                                            att_stat = "A tiempo"
                                        elif calendar_hour_in + timedelta(minutes=10) >= ini_datetime:
                                            att_stat = "Tolerancia"
                                        else:
                                            att_stat = "Retardo"
                                else:
                                    att_stat=search_att.dnk_attendance_stat
                                #else:
                                if regs == 1:
                                    att_stat = att_stat + '-Sin Salida'
                                search_att.write({
                                        'check_in': inicio,
                                        'check_out':fin,
                                        'dnk_device_id':dnk_device_id,
                                        'dnk_device_user_id':user[0],
                                        'dnk_attendance_stat':att_stat})
                            else:
                                #print ("Horario de salida es diferente")
                                if search_att.check_in == inicio and search_att.check_out != fin and regs > 1:
                                    att_stat=search_att.dnk_attendance_stat
                                    if (search_att.dnk_attendance_stat.find('-Sin Salida') != -1):
                                        att_stat=att_stat[0:att_stat.find('-Sin Salida')]
                                    else :
                                        att_stat= search_att.dnk_attendance_stat
                                    search_att.write({
                                            'check_out':fin,
                                            'dnk_attendance_stat':att_stat})


                                #else :
                                    #print ("Ps no hay nada por hacer")
                        else:
                            print ("No encontré registro automático de asistencia")
