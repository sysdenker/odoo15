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


def GetAttachments(url, db, uid, password, attach_list_fields, model, company_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    attachments = models.execute_kw(
        db, uid, password,
        'ir.attachment', 'search_read',
        [[['res_model', '=', model], ['company_id', '=', company_id]]],
        {'fields': attach_list_fields})

    return attachments


def GetInvoiceData(url, db, uid, password, invoice_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    invoice = models.execute_kw(
        db, uid, password,
        'account.invoice', 'search_read',
        [[['id', '=', invoice_id]]],
        {'fields': ('id', 'number', 'name', 'partner_id', 'state', 'customer_purchase_order_file', 'move_name', 'origin', 'company_id', 'l10n_mx_edi_cfdi_name'), 'limit': 1})
    if invoice:
        return invoice[0]
    else:
        return False


def SearchTargetInvoice(url, db, uid, password, invoice_name, company_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

    invoice = models.execute_kw(
        db, uid, password,
        'account.invoice', 'search_read',
        [[['origin', '=', invoice_name], ['company_id', '=', company_id], ['x_studio_field_O8kb3', '!=', False]]],
        {'fields': ('id', 'number', 'name', 'partner_id', 'state', 'x_studio_field_O8kb3', 'l10n_mx_edi_cfdi_name', 'origin'), 'limit': 1})
    if invoice:
        return invoice[0]
    else:
        return False


def SearchAttachedFile(url, db, uid, password, res_model, res_id, file_name):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

    attachtment = models.execute_kw(
        db, uid, password,
        'ir.attachment', 'search_read',
        [[['res_id', '=', res_id], ['res_model', '=', res_model], ['name', '=', file_name]]],
        {'fields': ('id'), 'limit': 1})
    if attachtment:
        return attachtment[0]
    else:
        return False


def GetAttachDataByID(url, db, uid, password, attachment_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

    attachtments = models.execute_kw(
        db, uid, password,
        'ir.attachment', 'search_read',
        [[['id', '=', attachment_id]]],
        {'fields': ('res_model', 'name', 'res_id', 'type', 'datas_fname', 'store_fname', 'mimetype', 'datas')})
    if attachtments:
        return attachtments[0]
    else:
        return False


def GetAttachData(url, db, uid, password, res_model, res_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

    attachtments = models.execute_kw(
        db, uid, password,
        'ir.attachment', 'search_read',
        [[['res_id', '=', res_id], ['res_model', '=', res_model]]],
        {'fields': ('res_model', 'name', 'res_id', 'type', 'datas_fname', 'store_fname', 'mimetype', 'datas')})
    return attachtments


def WriteAttachData(url, db, uid, password, data):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    attachment = models.execute_kw(db, uid, password, 'ir.attachment', 'create', [data])
    return(attachment)


def AttachFile(url, db, uid, password, filename, new_filename, res_model, res_id):

    if not os.path.isfile(filename):
        return("Error: Archivo no existe")

    with open(filename, 'rb') as f:
        bin_data = f.read()
        # print("Longitud: ", len(bin_data))

        contents = base64.b64encode(bin_data)
        sha = hashlib.sha1(bin_data or b'').hexdigest()
        fname = sha[:2] + '/' + sha

        mime = MimeTypes()
        mime_type = mime.guess_type(filename)
        # print(mime_type[0])

        data = {
            'res_model': res_model,
            'name': new_filename,
            'res_id': res_id,
            'type': 'binary',
            'datas_fname': new_filename,
            'store_fname': fname,
            'mimetype': mime_type[0],
            'datas': contents,
        }

        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        attachment = models.execute_kw(db, uid, password, 'ir.attachment', 'create', [data])
        return(attachment)


#############################################################################
#                             MAIN                                          #
#############################################################################


def GetPartnerSourceData(url, db, uid, password, partner_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    partner = models.execute_kw(
        db, uid, password,
        'res.partner', 'search_read',
        [[['id', '=', partner_id]]],
        {'fields': (
            'id',
            'name',
            'credit_limit',
            'block_sales',
            'dnk_l10n_mx_edi_usage',
            'dnk_l10n_mx_edi_payment_method_id',
            'dnk_is_final_customer',
            'dnk_purchase_order_required',
            'dnk_attach_purchase_order'), 'limit': 1})
    if partner:
        return partner[0]
    return False


def GetPartnerTargetData(url, db, uid, password, partner_id):
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    partner = models.execute_kw(
        db, uid, password,
        'res.partner', 'search_read',
        [[['id', '=', partner_id]]],
        {'fields': ('credit_limit', 'dnk_blocked_sales', 'name'), 'limit': 1})
    return partner[0]

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
# db_target = 'Migracion13Ago2020'
db_target = 'sysdenker-odoo13-23oct2020test-1610757'
username_target = 'admin'
password_target = 'SCD160118@2019'

uid_target = connect_odoo(url_target, db_target, username_target, password_target)

if uid_target:
    print("You are logged in Odoo Target")
else:
    print("You are NOT logged in Odoo Target")


################################################################################
#  ######################### Actualización de res_partner ######################

model = 'res.partner'

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url_target))

print(datetime.today())

Partners = models.execute_kw(
    db_target, uid_target, password_target,
    model, 'search_read',
    [[]],
    {'fields': ('id', 'name'), 'order': 'id asc'})
print(len(Partners))
for partner in Partners:
    partner_id = partner['id']
    partner_source = GetPartnerSourceData(url_source, db_source, uid_source, password_source, partner_id)
    partner_target = GetPartnerTargetData(url_target, db_target, uid_target, password_target, partner_id)
    # Validar Name, por si acaso
    if partner_source and partner_target and partner_source['name'] == partner_target['name']:
        print(partner_id, partner_source['name'])
        vals = {
            'credit_limit': partner_source['credit_limit'],
            'dnk_blocked_sales': partner_source['block_sales'],
            'dnk_l10n_mx_edi_usage': partner_source['dnk_l10n_mx_edi_usage'],
            'dnk_l10n_mx_edi_payment_method_id': partner_source['dnk_l10n_mx_edi_payment_method_id'][0] if partner_source['dnk_l10n_mx_edi_payment_method_id'] else False,
            'dnk_is_final_customer': partner_source['dnk_is_final_customer'],
            'dnk_purchase_order_required': partner_source['dnk_purchase_order_required'],
            'dnk_attach_purchase_order': partner_source['dnk_attach_purchase_order']
        }
        partner_mod = models.execute_kw(db_target, uid_target, password_target, model, 'write', [partner_id, vals])
print(datetime.today())
print("Fin proceso Partner")
exit()
