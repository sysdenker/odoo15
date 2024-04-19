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


def GetProductTemplateSourceData(url, db, uid, password, template_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    template = models.execute_kw(
        db, uid, password,
        'product.template', 'search_read',
        [[['id', '=', template_id]]],
        {'fields': (
            'id',
            'name',
            'dnk_costs_currency_id',
            'dnk_im_cost_id',
            'dnk_lc_cost_ids',
            'dnk_material_id',
            'dnk_volume_quotation'), 'limit': 1})
    if template:
        return template[0]
    return False


def GetProductLabourCostSourceData(url, db, uid, password, reg_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    registro = models.execute_kw(
        db, uid, password,
        'dnk.product.labour.cost.min', 'search_read',
        [[['id', '=', reg_id]]],
        {'fields': (
            'id',
            'dnk_name',
            'create_uid',
            'create_date',
            'dnk_product_tmpl_id',
            'dnk_product_labour_cost_id',
            'dnk_unit_price_usd',
            'dnk_product_labour_minutes_qty'), 'limit': 1})
    if registro:
        return registro[0]
    return False


def GetProductTemplateTargetData(url, db, uid, password, template_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    template = models.execute_kw(
        db, uid, password,
        'product.template', 'search_read',
        [[['id', '=', template_id]]],
        {'fields': ('id', 'name'), 'limit': 1})
    return template[0]

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
#  ######################### Actualización de Product Cost ######################
"""
UPDATE dnk_indirect_manufacturing_cost SET id = id + 100;

UPDATE dnk_indirect_manufacturing_cost SET id = 1 WHERE dnk_name = 'Empaque T5 - Bata';
UPDATE dnk_indirect_manufacturing_cost SET id = 2 WHERE dnk_name = 'Flete Interno - Ropa';
UPDATE dnk_indirect_manufacturing_cost SET id = 3 WHERE dnk_name = 'Flete Sobre Venta - Bata';
UPDATE dnk_indirect_manufacturing_cost SET id = 4 WHERE dnk_name = 'Empaque T5 - Guarda';
UPDATE dnk_indirect_manufacturing_cost SET id = 6 WHERE dnk_name = 'Flete Sobre Venta - Guarda';
UPDATE dnk_indirect_manufacturing_cost SET id = 8 WHERE dnk_name = 'Flete Sobre Venta - Prenda';
UPDATE dnk_indirect_manufacturing_cost SET id = 9 WHERE dnk_name = 'Empaque T5 - Overol';
UPDATE dnk_indirect_manufacturing_cost SET id = 7 WHERE dnk_name = 'Empaque T5 - Prenda';
UPDATE dnk_indirect_manufacturing_cost SET id = 10 WHERE dnk_name = 'Flete Sobre Venta - Overol';
UPDATE dnk_indirect_manufacturing_cost SET id = 11 WHERE dnk_name = 'Renta de Maquinaria Broche YKK - Ropa';

UPDATE dnk_labour_cost SET id = 1 WHERE dnk_name = 'COSTURA Y CORTE';
UPDATE dnk_labour_cost SET id = 2 WHERE dnk_name = 'BORDADO';


UPDATE dnk_product_material SET id = 7 WHERE dnk_name = 'Tela Poliester';
UPDATE dnk_product_material SET id = 8 WHERE dnk_name = 'vinil panal';

DELETE FROM dnk_product_labour_cost_min;
"""
################################################################################
#  ######################### Actualización de Product Template ######################

model = 'product.template'

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url_target))

print(datetime.today())

Templates = models.execute_kw(
    db_target, uid_target, password_target,
    model, 'search_read',
    [[['id', '=', '47564']]],
    # [[]],
    # {'fields': ('id', 'name'), 'order': 'id asc'})
    {'fields': ('id', 'name'), 'order': 'id asc', 'limit': 10})

print(len(Templates))
for template in Templates:
    template_id = template['id']
    template_source = GetProductTemplateSourceData(url_source, db_source, uid_source, password_source, template_id)
    template_target = GetProductTemplateTargetData(url_target, db_target, uid_target, password_target, template_id)
    # Validar Name, por si acaso
    if template_source and template_target and template_source['name'] == template_target['name']:
        print(template_id, template_source['name'])
        vals = {
            'dnk_cost_currency_id': template_source['dnk_costs_currency_id'][0] if template_source['dnk_costs_currency_id'] else False,
            'dnk_imc_ids': template_source['dnk_im_cost_id'],
            'dnk_material_id': template_source['dnk_material_id'][0] if template_source['dnk_material_id'] else False,
            'dnk_volume_quotation': template_source['dnk_volume_quotation'],
        }
        # print(vals)
        template_mod = models.execute_kw(db_target, uid_target, password_target, model, 'write', [template_id, vals])
print(datetime.today())
print("Fin proceso Product template")
exit()
