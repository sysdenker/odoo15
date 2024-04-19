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


def GetSaleOrderSourceData(url, db, uid, password, order_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    order = models.execute_kw(
        db, uid, password,
        'sale.order', 'search_read',
        [[['id', '=', order_id]]],
        {'fields': (
            'id',
            'name',
            'dnk_amount_untaxed_usd',
            'dnk_final_customer_id',
            'dnk_sale_city_id'), 'limit': 1})
    if order:
        return order[0]
    return False


def GetSaleOrderTargetData(url, db, uid, password, order_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    order = models.execute_kw(
        db, uid, password,
        'sale.order', 'search_read',
        [[['id', '=', order_id]]],
        {'fields': ('id', 'name'), 'limit': 1})
    return order[0]

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
# db_target = 'Migracion13Ago2020'
url_target = 'https://sysdenker-odoo13-23oct2020test-1610757.dev.odoo.com'
db_target = 'sysdenker-odoo13-23oct2020test-1610757'

username_target = 'admin'
password_target = 'SCD160118@2019'

uid_target = connect_odoo(url_target, db_target, username_target, password_target)

if uid_target:
    print("You are logged in Odoo Target")
else:
    print("You are NOT logged in Odoo Target")


################################################################################
#  ######################### Actualización de sale_order ######################

model = 'sale.order'

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url_target))

print(datetime.today())

Orders = models.execute_kw(
    db_target, uid_target, password_target,
    model, 'search_read',
    # [[['id', '=', '7121']]],
    [[]],
    # {'fields': ('id', 'name'), 'order': 'id asc', 'limit': 10})

    {'fields': ('id', 'name'), 'order': 'id asc'})

print(len(Orders))
for order in Orders:
    order_id = order['id']
    order_source = GetSaleOrderSourceData(url_source, db_source, uid_source, password_source, order_id)
    # print(order_source)
    order_target = GetSaleOrderTargetData(url_target, db_target, uid_target, password_target, order_id)
    # Validar Name, por si acaso
    if order_source and order_target and order_source['name'] == order_target['name']:
        print(order_id, order_source['name'])
        vals = {
            'dnk_usd_amount': order_source['dnk_amount_untaxed_usd'],
            'dnk_final_customer_id': order_source['dnk_final_customer_id'][0] if order_source['dnk_final_customer_id'] else False,
            'dnk_sale_city_id': order_source['dnk_sale_city_id'][0] if order_source['dnk_sale_city_id'] else False,
        }
        order_mod = models.execute_kw(db_target, uid_target, password_target, model, 'write', [order_id, vals])
print(datetime.today())
print("Fin proceso Sale order")
exit()
