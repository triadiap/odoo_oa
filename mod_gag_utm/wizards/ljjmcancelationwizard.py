# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import datetime

class TransientLjjmCancelation(models.TransientModel):
    _name = 'ljjm.cancelation.wizard'
    _description = 'LJJM Report Cancelation Wizard'

    id_ljjm = fields.Many2one('oa.equipment.maintenance', string='Related ID')
    refusal_reason_id = fields.Many2one( 'oa.refusal.reason',  string='Rejection Reason',required=True)
    rejection_note = fields.Text(string = "Remarks", required=True)
    approval_route_id = fields.Many2one('approval.route', string='Approval Route')
    current_step_id = fields.Many2one('approval.step', string='Current Step')
    existing_status = fields.Char(string="Current Status", tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", tracking=True)

    @api.model
    def default_get(self, fields):
        res = super(TransientLjjmCancelation, self).default_get(fields)
        if self._context.get('active_id'):
            model = self.env['oa.equipment.maintenance'].browse(self._context.get('active_id'))
            res['id_ljjm'] = model.id
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
            'state': 'rejected'
        }
        records = self.env['oa.equipment.maintenance'].browse(self.id_ljjm.id)
        records.write(vals)



