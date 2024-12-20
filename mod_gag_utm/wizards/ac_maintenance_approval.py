# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class TransientACMaintenanceApproval(models.TransientModel):
    _name = 'oa.acmaintenanceapproval.wizard'
    _description = 'Electricity Consumption Approval Wizard'

    id_ac_maintenance = fields.Many2one('oa.acmaintenance.request', string='Maintenance Request', required=True)
    approval_reason_id = fields.Many2one('oa.approval.reason', string='Approval Reason', required=True)
    approval_note = fields.Text(string="Remarks", required=True)
    approval_route_id = fields.Many2one('approval.route', string='Approval Route')
    current_step_id = fields.Many2one('approval.step', string='Current Step')
    existing_status = fields.Char(string="Current Status", tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", tracking=True)
    equipment_id = fields.Many2one('oa.master.equipment', string='Nama Equipment')
    job_finalization_date = fields.Date(string="Tanggal Selesai Pekerjaan")

    @api.model
    def default_get(self, fields):
        """
        Prefill the wizard fields based on the active record context.
        """
        res = super(TransientACMaintenanceApproval, self).default_get(fields)
        if self._context.get('active_id'):
            model = self.env['oa.acmaintenance.request'].browse(self._context.get('active_id'))
            if not model:
                raise ValidationError('The associated maintenance request does not exist.')
            res.update({
                'id_ac_maintenance': model.id,
                'approval_route_id': model.approval_route_id.id,
                'current_step_id': model.current_step_id.id,
                'existing_status': model.existing_status,
                'upcoming_status': model.upcoming_status.id if model.upcoming_status else False,
                'pending_approval_by': model.pending_approval_by.id if model.pending_approval_by else False,
                'equipment_id':model.equipment_id if model.equipment_id else False,
                'job_finalization_date':model.job_finalization_date if model.job_finalization_date else None
            })
        return res

    def action_confirm(self):
        """
        Confirm the approval process, updating the maintenance request with the next step or approval status.
        """
        # Ensure the current step is valid
        if not self.current_step_id:
            raise ValidationError('The current step is not defined.')

        # Ensure the user has permission to approve
        if self.env.user != self.current_step_id.user_id:
            raise ValidationError('You do not have the required permissions to approve this task.')

        # Get the next step from the approval route
        next_step = self.approval_route_id.get_next_step(self.current_step_id)
        vals = {}

        if next_step:
            # Update for the next approval step
            vals.update({
                'current_step_id': next_step.id,
                'existing_status': self.approval_reason_id.name,
                'pending_approval_by': next_step.user_id.id,
                'upcoming_status': next_step.id,
            })
            summary = f"Need Approval For REQ-{self.id_ac_maintenance.request_id} - {self.id_ac_maintenance.equipment_id.name} / {self.id_ac_maintenance.location_id.location_name}"
            notes = f"Approval For {self.id_ac_maintenance.equipment_id.name}"
            self.env['oa.acmaintenance.request'].acmaintenance_schedule_activity(
                self.id_ac_maintenance.id,
                summary,
                notes,
                self.id_ac_maintenance.date_to_action_need,
                next_step.user_id
            )
        else:
            # Finalize approval process
            vals.update({
                'state': 'approve',
                'existing_status': self.approval_reason_id.name,
                'pending_approval_by': None,
                'upcoming_status': None,
            })

            self.env['oa.acmaintenance.request'].next_maintenance_schedule_generated(
                self.equipment_id,
                self.job_finalization_date
            )

        # Update the maintenance request
        records = self.env['oa.acmaintenance.request'].browse(self.id_ac_maintenance.id)
        records.write(vals)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
