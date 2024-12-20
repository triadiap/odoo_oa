# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import datetime

class TransientMaintenanceApprovalWizard(models.TransientModel):
    _name = 'oa.machinemaintenance.approval'
    _description = 'OA Machine Maintenance Approval Wizard Model'

    id_machine_maintenance = fields.Many2one('oa.machine.maintenance', string='ID')
    approval_reason_id = fields.Many2one('oa.approval.reason', string='Approval Reason', required=True)
    approval_note = fields.Text(string="Remarks", required=True)
    approval_route_id = fields.Many2one('approval.route', string='Approval Route')
    current_step_id = fields.Many2one('approval.step', string='Current Step')
    existing_status = fields.Char(string="Current Status", tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", tracking=True)
    equip_id = fields.Many2one('oa.master.equipment', string='Equipment Name')
    maintenance_task_type = fields.Selection([
        ('top_over_haul', 'TOP OVER HAUL'),
        ('minor_over_haul', 'MINOR OVER HAUL'),
        ('general_over_haul', 'GENERAL OVER HAUL'),
        ('services', 'SERVICES'),
        ('greasing', 'GREASING'),
        ('body_repair', 'BODY REPAIR'),
        ('corrective_maintenance', 'CORRECTIVE MAINTENANCE'),
        ('breakdown_maintenance', 'BREAKDOWN MAINTENANCE')
    ], default="top_over_haul", string="Maintenance Type", tracking=True)
    sub_equipment = fields.Many2one('msdata.checkpoints', string='Sub Equipment')
    task_execution_date = fields.Datetime(string="Executed Date", tracking=True)
    maintenance_asset_group = fields.Many2one('point.group', string="Asset Group",tracking=True)

    @api.model
    def default_get(self, fields):
        res = super(TransientMaintenanceApprovalWizard, self).default_get(fields)
        if self._context.get('active_id'):
            model = self.env['oa.machine.maintenance'].browse(self._context.get('active_id'))
            res['id_machine_maintenance'] = model.id
            res['approval_route_id'] = model.approval_route_id
            res['current_step_id'] = model.current_step_id
            res['existing_status'] = model.existing_status
            res['upcoming_status'] = model.upcoming_status
            res['pending_approval_by'] = model.pending_approval_by
            res['equip_id'] = model.equip_id
            res['maintenance_task_type'] = model.maintenance_task_type
            res['sub_equipment'] = model.sub_equipment
            res['task_execution_date'] = model.task_execution_date
            res['maintenance_asset_group'] = model.maintenance_asset_group
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
                'upcoming_status':next_step,
                'task_approval_notes':self.approval_note
            }
            summary = f"Pending Approval By {next_step.user_id.name}"
            notes = f"Approval Requirement for {self.equip_id.name}"
            self.env['oa.machine.maintenance'].generate_schedule_activity(
                self.id_machine_maintenance.id,
                summary,
                notes,
                self.task_execution_date,
                next_step.user_id
            )
        else:
            vals = {
                'state':'approve',
                'existing_status' : self.approval_reason_id.name,
                'pending_approval_by': None,
                'upcoming_status' : None,
                'task_approval_notes': self.approval_note
            }

            self.env['oa.machine.maintenance'].generate_all_maintenance_task(
                    self.equip_id,
                    self.maintenance_task_type,
                    self.sub_equipment,
                    self.task_execution_date,
                    self.maintenance_asset_group
                )
        records = self.env['oa.machine.maintenance'].browse(self.id_machine_maintenance.id)
        records.write(vals)
