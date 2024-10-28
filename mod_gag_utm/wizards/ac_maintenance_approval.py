# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import datetime

class TransientACMaintenanceApproval(models.TransientModel):
    _name = 'oa.acmaintenanceapproval.wizard'
    _description = 'Electricity Consumption Approval Wizard'

    id_ac_maintenance = fields.Many2one('oa.acmaintenance.request', string='ID')
    approval_reason_id = fields.Many2one('oa.approval.reason', string='Approval Reason', required=True)
    approval_note = fields.Text(string="Remarks", required=True)
    approval_route_id = fields.Many2one('approval.route', string='Approval Route')
    current_step_id = fields.Many2one('approval.step', string='Current Step')
    existing_status = fields.Char(string="Current Status", tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", tracking=True)

    @api.model
    def default_get(self, fields):
        res = super(TransientACMaintenanceApproval, self).default_get(fields)
        if self._context.get('active_id'):
            model = self.env['oa.acmaintenance.request'].browse(self._context.get('active_id'))
            res['id_ac_maintenance'] = model.id
            res['approval_route_id'] = model.approval_route_id
            res['current_step_id'] = model.current_step_id
            res['existing_status'] = model.existing_status
            res['upcoming_status'] = model.upcoming_status
            res['pending_approval_by'] = model.pending_approval_by
        return res
    def action_confirm(self):
        if self.env.user != self.current_step_id.user_id:
            raise ValidationError('You do not have the required permissions to approve this task.')
        next_step = self.approval_route_id.get_next_step(self.current_step_id)
        if next_step:
            vals = {
                'current_step_id':next_step,
                'existing_status':self.approval_reason_id.name,
                'pending_approval_by':next_step.user_id,
                'upcoming_status':next_step
            }
        else:
            vals = {
                'state':'approve',
                'existing_status' : self.approval_reason_id.name,
                'pending_approval_by': None,
                'upcoming_status' : None
            }
        records = self.env['oa.acmaintenance.request'].browse(self.id_ac_maintenance.id)
        records.write(vals)
