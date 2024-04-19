#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import xmlrpclib
from datetime import datetime
# import pymssql
import math
import os

import base64
import hashlib
from mimetypes import MimeTypes


def login(url):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
    return models


def connect_odoo(url, db, username, password):
    common = login(url)
    uid = common.authenticate(db, username, password, {})
    return uid


#############################################################################
#                             MAIN                                          #
#############################################################################


def GetCRMSourceData(url, db, uid, password, lead_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    lead = models.execute_kw(
        db, uid, password,
        'crm.lead', 'search_read',
        [[['id', '=', lead_id]]],
        {'fields': (
            'id',
            'name',
            'dnk_sale_city_id',
            'dnk_final_customer_id',
            'dnk_family_id',
            'dnk_subfamily_id',
            'dnk_product_id',
            'dnk_pieces',
            'dnk_price',
            'dnk_is_vendor'), 'limit': 1})
    if lead:
        return lead[0]
    return False


def GetCRMTargetData(url, db, uid, password, lead_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    lead = models.execute_kw(
        db, uid, password,
        'crm.lead', 'search_read',
        [[['id', '=', lead_id]]],
        {'fields': ('id', 'name'), 'limit': 1})
    return lead[0]

#  ############################## ODOO SOURCE #################################


url_source = 'https://grupodenker.odoo.com'
db_source = 'grupodenker-master-113629'
username_source = 'admin'
password_source = 'SCD160118@2019'

uid_source = connect_odoo(url_source, db_source, username_source, password_source)

if uid_source:
    print("You are logged in Odoo Source")
else:
    print("You are NOT logged in Odoo Source")
#############################################################################


#  ############################## ODOO TARGET #################################
# url_target = 'http://localhost:8013'
url_target = 'https://sysdenker-odoo13-23oct2020test-1610757.dev.odoo.com'
db_target = 'sysdenker-odoo13-23oct2020test-1610757'
# db_target = 'Migracion13Ago2020'
username_target = 'admin'
password_target = 'SCD160118@2019'

uid_target = connect_odoo(url_target, db_target, username_target, password_target)

if uid_target:
    print("You are logged in Odoo Target")
else:
    print("You are NOT logged in Odoo Target")


################################################################################
#  ######################### Actualización de crm_lead ######################

model = 'crm.lead'

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url_target))

print(datetime.today())

Leads = models.execute_kw(
    db_target, uid_target, password_target,
    model, 'search_read',
    # [[['id', '=', '10739']]],
    [[]],
    # {'fields': ('id', 'name'), 'order': 'id asc', 'limit': 10})
    {'fields': ('id', 'name'), 'order': 'id asc'})
print(len(Leads))
for lead in Leads:
    lead_id = lead['id']
    lead_source = GetCRMSourceData(url_source, db_source, uid_source, password_source, lead_id)
    # print(lead_source)
    lead_target = GetCRMTargetData(url_target, db_target, uid_target, password_target, lead_id)
    # Validar Name, por si acaso
    if lead_source and lead_target and lead_source['name'] == lead_target['name']:
        print(lead_id, lead_source['name'])
        vals = {
            'dnk_sale_city_id': lead_source['dnk_sale_city_id'][0] if lead_source['dnk_sale_city_id'] else False,
            'dnk_final_customer_id': lead_source['dnk_final_customer_id'],
            'dnk_family_id': lead_source['dnk_family_id'][0] if lead_source['dnk_family_id'] else False,
            'dnk_subfamily_id': lead_source['dnk_subfamily_id'][0] if lead_source['dnk_subfamily_id'] else False,
            'dnk_pieces': lead_source['dnk_pieces'],
            'dnk_price': lead_source['dnk_price'],
            'dnk_product_id': lead_source['dnk_product_id'][0] if lead_source['dnk_product_id'] else False,
            'dnk_is_vendor': lead_source['dnk_is_vendor']
        }
        lead_mod = models.execute_kw(db_target, uid_target, password_target, model, 'write', [lead_id, vals])
print(datetime.today())
print("Fin proceso CRM Lead")
exit()
