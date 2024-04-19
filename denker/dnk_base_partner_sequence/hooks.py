# -*- coding: utf-8 -*-

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    domain = [('ref', '=', False), ('customer_rank', '>', 0), ('is_company', '=', True)]
    res_ids = env['res.partner'].search(domain).mapped('id')

    iIndex = 0
    for partner in env['res.partner'].browse(res_ids):
        iIndex += 1
        vals = {'ref': partner._get_next_ref()}
        partner.write(vals)
