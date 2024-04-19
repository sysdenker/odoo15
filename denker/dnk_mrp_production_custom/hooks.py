# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    res_ids = env['mrp.production'].search([]).mapped('id')
    env['mrp.production'].browse(res_ids)._compute_workorder_done_count()
