# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015 Deltatech All Rights Reserved
#                    Dorin Hongu <dhongu(@)gmail(.)com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.osv.query import Query
from odoo.models import BaseModel
from odoo.exceptions import AccessError
import logging

_logger = logging.getLogger(__name__)


class BaseModelExtend(models.AbstractModel):

    _name = 'basemodel.extend'
    _description = 'Basemodel Extend'

    @api.model
    def _register_hook(self):

        @api.model
        def check_field_access_rights(self, operation, fields):
            """
            Check the user access rights on the given fields. This raises Access
            Denied if the user does not have the rights. Otherwise it returns the
            fields (as is if the fields is not falsy, or the readable/writable
            fields if fields is falsy).
            """
            if self.env.su:
                return fields or list(self._fields)

            def valid(fname):
                """ determine whether user has access to field ``fname`` """
                field = self._fields.get(fname)
                if field and field.groups:
                    return self.user_has_groups(field.groups)
                else:
                    return True

            if not fields:
                fields = [name for name in self._fields if valid(name)]
            else:
                invalid_fields = {name for name in fields if not valid(name)}
                if invalid_fields:
                    _logger.info('Access Denied by ACLs for operation: %s, uid: %s, model: %s, fields: %s',
                                 operation, self._uid, self._name, ', '.join(invalid_fields))

                    description = self.env['ir.model']._get(self._name).name
                    if not self.env.user.has_group('base.group_no_one'):
                        raise AccessError(
                            _('You do not have enough rights to access the fields "%(fields)s" on %(document_kind)s (%(document_model)s). '\
                              'Please contact your system administrator.\n\n(Operation: %(operation)s)') % {
                            'fields': ','.join(list(invalid_fields)),
                            'document_kind': description,
                            'document_model': self._name,
                            'operation': operation,
                        })

                    def format_groups(field):
                        anyof = self.env['res.groups']
                        noneof = self.env['res.groups']
                        for g in field.groups.split(','):
                            if g.startswith('!'):
                                noneof |= self.env.ref(g[1:])
                            else:
                                anyof |= self.env.ref(g)
                        strs = []
                        if anyof:
                            strs.append(_("allowed for groups %s") % ', '.join(
                                anyof.sorted(lambda g: g.id)
                                     .mapped(lambda g: repr(g.display_name))
                            ))
                        if noneof:
                            strs.append(_("forbidden for groups %s") % ', '.join(
                                noneof.sorted(lambda g: g.id)
                                      .mapped(lambda g: repr(g.display_name))
                            ))
                        return '; '.join(strs)

                    raise AccessError(_("""The requested operation can not be completed due to security restrictions.

    Document type: %(document_kind)s (%(document_model)s)
    Operation: %(operation)s
    User: %(user)s
    Fields:
    %(fields_list)s""") % {
                        'document_model': self._name,
                        'document_kind': description or self._name,
                        'operation': operation,
                        'user': self._uid,
                        'fields_list': '\n'.join(
                            '- %s (%s)' % (f, format_groups(self._fields[f]))
                            for f in sorted(invalid_fields)
                        )
                    })

            return fields

        models.AbstractModel.check_field_access_rights = check_field_access_rights
        return super(BaseModelExtend, self)._register_hook()
