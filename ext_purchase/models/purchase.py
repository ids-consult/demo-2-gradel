# -*- encoding: utf-8 -*-
##############################################################################
#
#    ServerPLM, Open Source Product Lifcycle Management System    
#    Copyright (C) 2020-2022 Didotech srl (<http://www.didotech.com>). All Rights Reserved
#
#    Created on: 2022-09-22
#    Author : Fabio Colognesi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import base64

from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

##############################################################################
#   Overrides original methods
##############################################################################

    def action_rfq_send(self):
        '''
        This function opens a window to compose an email, with the edi purchase template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            if self.env.context.get('send_rfq', False):
                template_id = ir_model_data._xmlid_lookup('purchase.email_template_edi_purchase')[2]
            else:
                template_id = ir_model_data._xmlid_lookup('purchase.email_template_edi_purchase_done')[2]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[2]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'purchase.order',
            'active_model': 'purchase.order',
            'active_id': self.ids[0],
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'mark_rfq_as_sent': True,
        })

        # In the case of a RFQ or a PO, we want the "View..." button in line with the state of the
        # object. Therefore, we pass the model description in the context, in the language in which
        # the template is rendered.
        lang = self.env.context.get('lang')
        if {'default_template_id', 'default_model', 'default_res_id'} <= ctx.keys():
            template = self.env['mail.template'].browse(ctx['default_template_id'])
            if template and template.lang:
                lang = template._render_lang([ctx['default_res_id']])[ctx['default_res_id']]

        self = self.with_context(lang=lang)
        if self.state in ['draft', 'sent']:
            ctx['model_description'] = _('Request for Quotation')
        else:
            ctx['model_description'] = _('Purchase Order')
##############################################################################
#   Code injection
##############################################################################
        if template:
            product_ids = self.order_line.mapped('product_id')
            pdftext = product_ids.getPDFbyProducts(level=-1)  
            name = self.name.split('\\')[-1].split('/')[-1].split('.')[0] + '-Drawings.pdf'
            attachment = self.env['ir.attachment'].create({
                    'name': name,
                    'res_id': template.id,
                    'res_model': template._name,
                    'datas': base64.encodebytes(pdftext),
                    'type': 'binary',
                    'mimetype': 'application/pdf',
                })
            template.attachment_ids = attachment
##############################################################################
#   Code injection
##############################################################################
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

##############################################################################
#   Overrides original methods
##############################################################################

