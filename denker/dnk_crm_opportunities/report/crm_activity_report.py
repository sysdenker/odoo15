# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ActivityReport(models.Model):
    _inherit = 'crm.activity.report'

    dnk_activity_create_date = fields.Datetime('- Activity Creation Date', readonly=True)

    def _select(self):
        select_activity_report = ", m.create_date AS dnk_activity_create_date"

        return super(ActivityReport, self)._select() + select_activity_report
