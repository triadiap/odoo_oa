# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class RefusalReason(models.Model):
    _name = 'oa.refusal.reason'
    _description = 'Office Automation Refusal Reason'

    name = fields.Char(string="Name",required=True)
    refusal_code = fields.Char(string="Code", required=True)
    refusal_label = fields.Char(string="Label", required=True)
    refusal_summary = fields.Char(string="Summary")

    @api.model
    def create(self,vals):
        if 'refusal_code' in vals:
            existing_record = self.search([('refusal_code', '=', vals['refusal_code'])])
            if existing_record:
                raise ValidationError(
                    'Selected Model ID "{}" already exists. Please choose a different one.'.format(vals['refusal_code']))
        return super(RefusalReason, self).create(vals)
    def write(self,vals):
        if 'refusal_code' in vals:
            existing_record = self.search([('refusal_code', '=', vals['refusal_code'])])
            if existing_record:
                raise ValidationError(
                    'Selected Model ID "{}" already exists. Please choose a different one.'.format(vals['refusal_code']))
        return super(RefusalReason, self).create(vals)