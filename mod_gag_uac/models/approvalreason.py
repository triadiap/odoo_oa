# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class MasterApprovalReason(models.Model):
    _name = 'oa.approval.reason'
    _description = 'Office Automation Approval Reason Master'

    name = fields.Char(string="Name / Label", required=True)
    oa_ar_code = fields.Char(string="Code", required=True)
    oa_ar_summary  = fields.Text(string="Summary", required=True)

    @api.model
    def create(self, vals):
        if 'oa_ar_code' in vals:
            existing_record = self.search([('oa_ar_code', '=', vals['oa_ar_code'])])
            if existing_record:
                raise ValidationError(
                    'Selected Model ID "{}" already exists. Please choose a different one.'.format(
                        vals['oa_ar_code']))
        return super(MasterApprovalReason, self).create(vals)

    def write(self, vals):
        if 'oa_ar_code' in vals:
            existing_record = self.search([('oa_ar_code', '=', vals['oa_ar_code'])])
            if existing_record:
                raise ValidationError(
                    'Selected Model ID "{}" already exists. Please choose a different one.'.format(
                        vals['oa_ar_code']))
        return super(MasterApprovalReason, self).create(vals)

