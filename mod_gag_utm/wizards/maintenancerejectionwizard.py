# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import datetime

class TransientMachineMaintenanceCancelationWizard(models.TransientModel):
    _name = 'oa.machinemaintenance.rejection'
    _description = 'Machine Maintenance Task Cancelation Wizard'

    id_machine_maintenance = fields.Many2one('oa.machine.maintenance', string='ID')
    refusal_reason_id = fields.Many2one('oa.refusal.reason', string='Rejection Reason', required=True)
    rejection_note = fields.Text(string="Remarks", required=True)
    approval_route_id = fields.Many2one('approval.route', string='Approval Route')
    current_step_id = fields.Many2one('approval.step', string='Current Step')
    existing_status = fields.Char(string="Current Status", tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", tracking=True)

    @api.model
    def default_get(self, fields):
        res = super(TransientMachineMaintenanceCancelationWizard, self).default_get(fields)
        if self._context.get('active_id'):
            model = self.env['oa.machine.maintenance'].browse(self._context.get('active_id'))
            res['id_machine_maintenance'] = model.id
            res['approval_route_id'] = model.approval_route_id
            res['current_step_id'] = model.current_step_id
            res['existing_status'] = model.existing_status
            res['upcoming_status'] = model.upcoming_status
            res['pending_approval_by'] = model.pending_approval_by
        return res

    def action_reject(self):
        if self.env.user != self.current_step_id.user_id:
            raise ValidationError('You do not have the required permissions to reject this document.')
        vals = {
            'current_step_id': None,
            'existing_status': self.refusal_reason_id.name,
            'pending_approval_by': None,
            'upcoming_status': None,
            'state': 'rejected',
            'task_approval_notes': self.rejection_note
        }
        records = self.env['oa.machine.maintenance'].browse(self.id_machine_maintenance.id)
        records.write(vals)
