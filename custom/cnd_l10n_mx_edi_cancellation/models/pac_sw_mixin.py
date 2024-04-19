# -*- coding: utf-8 -*-
from odoo import models, _
import json


class PACSWMixin(models.AbstractModel):
    """PAC SW Mixin is a mixin Abstract class to add methods
    in order to call services of the PAC SW.
    It defines standard name methods that are auto-called from account.move
    or account.payment.

    Re-using code as soon as possible.

    It class is not defining new fields.
    In fact, It is using the standard fields defined by a l10n_mx_edi classes
    """
    _inherit = 'l10n_mx_edi.pac.sw.mixin'

    def _l10n_mx_edi_sw_cancel(self, pac_info):
        token, req_e = self._l10n_mx_edi_sw_token(pac_info)
        if not token:
            self.l10n_mx_edi_log_error(
                _("Token could not be obtained %s") % req_e)
            return
        url = pac_info['url']
        headers = {
            'Authorization': "bearer " + token,
            'Content-Type': "application/json"
        }
        for rec in self:
            xml = rec.l10n_mx_edi_get_xml_etree()
            tfd_node = rec.l10n_mx_edi_get_tfd_etree(xml)
            certificate_ids = rec.company_id.l10n_mx_edi_certificate_ids
            certificate = certificate_ids.sudo().get_valid_certificate()
            data = {
                'rfc': xml.Emisor.get('Rfc'),
                'b64Cer': certificate.content.decode('UTF-8'),
                'b64Key': certificate.key.decode('UTF-8'),
                'password': certificate.password,
                'uuid': tfd_node.get('UUID'),
                'motivo': self.l10n_mx_edi_cancellation_type,
            }
            if self.l10n_mx_edi_cancellation_related_uuid:
                data['folioSustitucion'] = self.l10n_mx_edi_cancellation_related_uuid
            response_json = self._l10n_mx_edi_sw_post(
                url, headers, payload=json.dumps(data).encode('UTF-8'))
            cancelled = response_json['status'] == 'success'
            code = response_json.get('message')
            msg = response_json.get('messageDetail')
            rec._l10n_mx_edi_post_cancel_process(
                cancelled, code=code, msg=msg)
