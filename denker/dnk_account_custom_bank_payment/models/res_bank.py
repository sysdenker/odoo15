# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    _sql_constraints = [
        ('unique_number', 'check (1 != 1)', 'Account Number NOT must be unique'),
        # Original
        # ('unique_number', 'unique(sanitized_acc_number, company_id)', 'Account Number must be unique'),
    ]
