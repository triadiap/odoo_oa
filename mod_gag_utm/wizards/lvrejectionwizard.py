# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import datetime

class LVRejectionWizard(models.TransientModel):
    _name = 'lv.rejection.wizard'
    _description = 'Unit LV Report Rejection Wizard'

    id_lv_report = fields.Many2one('oa.lvdaily.report', string='Related ID')
    refusal_reason_id = fields.Many2one('oa.refusal.reason', string='Rejection Reason', required=True)
    rejection_note = fields.Text(string="Remarks", required=True)
    approval_route_id = fields.Many2one('approval.route', string='Approval Route')
    current_step_id = fields.Many2one('approval.step', string='Current Step')
    existing_status = fields.Char(string="Current Status", tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", tracking=True)

    @api.model
    def default_get(self, fields):
        res = super(LVRejectionWizard, self).default_get(fields)
        if self._context.get('active_id'):
            model = self.env['oa.lvdaily.report'].browse(self._context.get('active_id'))
            res['id_lv_report'] = model.id
            res['approval_route_id'] = model.approval_route_id
            res['current_step_id'] = model.current_step_id
            res['existing_status'] = model.existing_status
            res['upcoming_status'] = model.upcoming_status
            res['pending_approval_by'] = model.pending_approval_by
        return res

    def action_reject(self):
        if self.env.user != self.current_step_id.user_id:
            raise ValidationError('You do not have the required permissions to approve this document.')

        vals = {
                'state':'rejected',
                'existing_status' : f"Rejected by {self.pending_approval_by.name}",
                'pending_approval_by': None,
                'upcoming_status' : None,
                'approver_notes' : self.rejection_note
            }
        records = self.env['oa.lvdaily.report'].browse(self.id_lv_report.id)
        records.write(vals)



