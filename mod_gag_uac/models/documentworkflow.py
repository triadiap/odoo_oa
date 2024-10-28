# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class DocumentWorkflow(models.Model):
    _name = 'oa.document.workflow.config'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Office Automation Document Workflow Setup'

    model_id = fields.Many2one('ir.model', string='Model', required=True, help="Select the model that will use this approval route.",ondelete='cascade', tracking=True)
    approval_route_id = fields.Many2one('approval.route', string='Approval Route', required=True,  ondelete='cascade', help="Select the approval route to be used for this model.", tracking=True)
    notes = fields.Text(string="Notes", tracking=True)


    @api.model
    def create(self,vals):
        if 'model_id' in vals:
            existing_record = self.search([('model_id', '=', vals['model_id'])])
            if existing_record:
                raise ValidationError(
                    'Selected Model ID "{}" already exists. Please choose a different one.'.format(vals['model_id']))
        return super(DocumentWorkflow, self).create(vals)
    def write(self,vals):
        if 'model_id' in vals:
            existing_record = self.search([('model_id', '=', vals['model_id'])])
            if existing_record:
                raise ValidationError(
                    'Selected Model ID "{}" already exists. Please choose a different one.'.format(vals['model_id']))
        return super(DocumentWorkflow, self).create(vals)