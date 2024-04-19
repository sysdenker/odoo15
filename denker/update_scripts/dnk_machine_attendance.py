#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import xmlrpc
from xmlrpc.server import SimpleXMLRPCServer
from datetime import datetime
# import pymssql
import math
import os

import base64
import hashlib
from mimetypes import MimeTypes


def login(url):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
    return models


def connect_odoo(url, db, username, password):
    common = login(url)
    uid = common.authenticate(db, username, password, {})
    return uid

def GetDnkMachineAttendaceSourceData(url, db, uid, password):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    attendance = models.execute_kw(
        db, uid, password,
        'dnk.machine.attendance', 'search_read',
        # [[['id', '=', lead_id]]],
        [[['punching_time_utc', '>', '2021-10-01 00:00:00']]],
        {'fields': (
            'id',
            'attendance_type',
            'punch_type',
            'punching_time',
            'punching_time_utc',
            'dnk_device_id',
            'dnk_device_user_id')})
    if attendance:
        return attendance
    return False
#  ############################## ODOO SOURCE #################################


# url_source = 'https://grupodenker.odoo.com'
url_source = 'http://187.190.42.134:811'
# db_source = 'grupodenker-master-113629'
# db_source = '29Ago2021Prod'
db_source = 'grupodenker20201119'
username_source = 'admin'
# password_source = 'SCD160118@2019'
password_source = 'Odoo11SCD160118@2019'
uid_source = connect_odoo(url_source, db_source, username_source, password_source)

if uid_source:
    print("You are logged in Odoo Source")
else:
    print("You are NOT logged in Odoo Source")
#############################################################################


#  ############################## ODOO TARGET #################################
url_target = 'http://localhost:8013'
# url_target = 'https://denker-pruebas.odoo.com'
# db_target = 'grupodenker-06oct2021-3361955'
db_target = '29Ago2021Prod'
username_target = 'admin'
password_target = 'SCD160118@2019'

uid_target = connect_odoo(url_target, db_target, username_target, password_target)

if uid_target:
    print("You are logged in Odoo Target")
else:
    print("You are NOT logged in Odoo Target")


################################################################################
#  ######################### Actualización de res_partner ######################

model = 'dnk.machine.attendance'

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_target))
models_source = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_source))

print(datetime.today())

Attendance = GetDnkMachineAttendaceSourceData(url_source, db_source, uid_source, password_source)
if Attendance:
    print(len(Attendance))
    for attendace in Attendance:
        attendace_id = attendace['id']
        'id',
        'attendance_type',
        'punching_time',
        'punch_type',
        'punching_time_utc',
        'dnk_device_id',
        'dnk_device_user_id'

        data = {
            'punch_type': attendace['punch_type'],
            'attendance_type': attendace['attendance_type'],
            'punching_time': attendace['punching_time'],
            'punching_time_utc': attendace['punching_time_utc'],
            'dnk_device_id': attendace['dnk_device_id'],
            'dnk_device_user_id': attendace['dnk_device_user_id']
        }
        attendace_target = models.execute_kw(db_target, uid_target, password_target, model, 'create', [data])
        if attendace_target:
            vals = {
                'dnk_is_sync': 1,
            }
            attendace_source = models_source.execute_kw(db_source, uid_source, password_source, model, 'write', [attendace_id, vals])

print(datetime.today())
print("Fin proceso Attendance")
exit()
