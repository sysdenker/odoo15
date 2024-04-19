# -*- coding: utf-8 -*-
from odoo.addons import decimal_precision as dp
from odoo import _, models, fields, api, exceptions
import base64
from lxml.objectify import fromstring
from lxml import etree


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    @api.model
    def l10n_mx_edi_get_addenda_etree(self, cfdi):
        '''Get the Addenda node from the cfdi.

        :param cfdi: The cfdi as etree
        :return: the cfdi:Addenda node
        '''
        if not hasattr(cfdi, 'Addenda'):
            return None
        node = cfdi.Addenda
        return node[0] if len(node) else False

    # Agregar la Addenda Manual Post-Timbrado
    def l10n_mx_edi_regenerate_addenda(self):
        self.ensure_one()

        attachment_id = self.l10n_mx_edi_retrieve_last_attachment()
        if not attachment_id:
            raise exceptions.UserError(_(
                'Xml file not attached.'))
        xml_data = base64.b64decode(attachment_id.datas)

        addenda = self.partner_id.commercial_partner_id.l10n_mx_edi_addenda
        if not addenda:
            return False
        values = {
            'record': self,
        }

        tree = fromstring(xml_data)
        addenda_node = fromstring(addenda.render(values=values))
        if addenda_node.tag != '{http://www.sat.gob.mx/cfd/3}Addenda':
            node = etree.Element(etree.QName(
                'http://www.sat.gob.mx/cfd/3', 'Addenda'))
            node.append(addenda_node)
            addenda_node = node

        current_addenda_node = self.l10n_mx_edi_get_addenda_etree(tree)
        if current_addenda_node is not None:
            tree.Addenda = addenda_node
        else:
            tree.append(addenda_node)

        self.message_post(
            body=_('Addenda has been replaced in the CFDI with success'),
            subtype='account.mt_invoice_validated')

        xml_signed = base64.encodestring(etree.tostring(
            tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        attachment_id.write({
            'datas': xml_signed,
            'mimetype': 'application/xml'
        })
        return xml_signed
