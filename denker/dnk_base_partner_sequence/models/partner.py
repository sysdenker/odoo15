# -*- coding: utf-8 -*-

from odoo import api, models, exceptions, _


class ResPartner(models.Model):
    """Assigns 'ref' from a sequence on creation and copying"""

    _inherit = 'res.partner'

    def _get_next_ref(self, vals=None):
        return self.env['ir.sequence'].next_by_code('res.partner')

    @api.model
    def create(self, vals):
        if not vals.get('ref') and self._needsRef(vals=vals):
            vals['ref'] = self._get_next_ref(vals=vals)
        return super(ResPartner, self).create(vals)

    def copy(self, default=None):
        default = default or {}
        if self._needsRef():
            default['ref'] = self._get_next_ref()
        return super(ResPartner, self).copy(default)

    def write(self, vals):
        for partner in self:
            if not vals.get('ref') and partner._needsRef(vals) and \
               not partner.ref:
                vals['ref'] = partner._get_next_ref(vals=vals)
            super(ResPartner, partner).write(vals)
        return True

    def _needsRef(self, vals=None):
        """
        Checks whether a sequence value should be assigned to a partner's 'ref'

        :param vals: known field values of the partner object
        :return: true iff a sequence value should be assigned to the\
                      partner's 'ref'
        """
        if not vals and not self:  # pragma: no cover
            raise exceptions.UserError(_(
                'Either field values or an id must be provided.'))
        # only assign a 'ref' to commercial partners
        if self:
            vals = {}
            vals['is_company'] = self.is_company
            vals['customer_rank'] = self.customer_rank
        return vals.get('customer_rank') and vals.get('is_company')

    @api.model
    def _commercial_fields(self):
        """
        Make the partner reference a field that is propagated
        to the partner's contacts
        """
        return super(ResPartner, self)._commercial_fields() + ['ref']
