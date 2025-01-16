# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class BagPrintedSubstrate(models.Model):
    _name = 'dnk.bag.printed.substrate'
    _description = 'Printed Substrate'
    _rec_name = 'name'
    _order = 'name, sequence'

    name = fields.Char('- Name', index=True, required=True, translate=True)
    sequence = fields.Integer('- Sequence')
    description = fields.Text(
        '- Description', translate=True)
    

class BagLamination(models.Model):
    _name = 'dnk.bag.lamination'
    _description = 'Lamination'
    _rec_name = 'name'
    _order = 'name, sequence'

    name = fields.Char('- Name', index=True, required=True, translate=True)
    sequence = fields.Integer('- Sequence')
    description = fields.Text(
        '- Description', translate=True)



class BagThickness(models.Model):
    _name = 'dnk.bag.thickness'
    _description = 'Bag Thickness'
    _rec_name = 'name'
    _order = 'name, sequence'

    name = fields.Char('- Name', index=True, required=True, translate=True)
    sequence = fields.Integer('- Sequence')
    description = fields.Text(
        '- Description', translate=True)