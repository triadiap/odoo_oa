# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class DocumentGeneral(models.Model):
    _name = 'gag.oa.general.document'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'OA General Docuemnt'

    name = fields.Char("Docuement Name")
    tanggal = fields.Date("Document Date")
    
    document_type = fields.Many2one("oa.document.type","Document Type")
    document_file = fields.Binary("Document File")
    groupid = fields.Many2one('res.groups', string="Groups", tracking=True, required=True)
    status = fields.Selection([
        ('0', 'Draft'),
        ('1', 'Request Approval'),
        ('2', 'Approved')
    ], default="0", string="Status", tracking=True)


    def domain_groupids(self):
        matching_records = self.env['oa.documenttype.approvalroute'].search([('group_id', 'in', self.env.user.groups_id.ids)]).mapped('document_type_id')

    @api.onchange('tanggal')
    def _onchange_tanggal_update_doc(self):
        """Update options in field_b_id based on the selected field_a_id."""
        if self.tanggal:
            # Search for matching records in Model C
            return {
                'domain': {
                    'groupid':[('id','in',self.env.user.groups_id.ids),('name','like','OA-')]
                }
            }
        else:
            # No value selected in field_a_id, clear field_b_id and set domain to empty
            self.document_type = False
            return {
                'domain': {
                    'groupid': [('id', '=', False)]
                }
            }
    @api.onchange('groupid')
    def _onchange_groupid_update_doc(self):
        """Update options in field_b_id based on the selected field_a_id."""
        if self.groupid:
            # Search for matching records in Model C
            matching_records = self.env['oa.documenttype.approvalroute'].search([('group_id', '=', self.groupid.id)]).mapped('document_type_id')
            if matching_records:
                # Set domain to show matching records
                return {
                    'domain': {
                        'document_type': [('id', 'in', matching_records.ids)],
                    }
                }
            else:
                # No matching records found, clear field_b_id and set domain to empty
                self.document_type = False
                return {
                    'domain': {
                        'document_type': [('id', '=', False)]
                    }
                }
        else:
            # No value selected in field_a_id, clear field_b_id and set domain to empty
            self.document_type = False
            return {
                'domain': {
                    'document_type': [('id', '=', False)]
                }
            }
