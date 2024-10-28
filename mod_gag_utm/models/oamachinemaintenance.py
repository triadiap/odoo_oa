# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class OAMachineMaintenance(models.Model):
    _name="oa.machine.maintenance"
    _description="Office Automation Machine Maintenance Form"

    name = fields.Char(string="Task Description",required=True,tracking=True)
    id_maintenance_task = fields.Char(string="ID Task",required=True,copy=False, default='New')
    maintenance_task_type = fields.Many2one('oa.maintenancetype.master',string="Maintenance Type",required=True,tracking=True)
    equip_id = fields.Many2one('oa.master.equipment', string='Equipment Name',required=True,tracking=True)
    brand_model_type = fields.Char(string='Brand/Type/Year', tracking=True)
    serial_number = fields.Char(string='Serial Number', tracking=True)
    asset_number = fields.Char(string='Asset Number', tracking=True)
    pkt_number = fields.Char(string='PKT Number', tracking=True)
    kwh_equipment = fields.Char(string='Power (Kw)', tracking=True)
    maintenance_asset_group = fields.Many2one('point.group', string="Asset Group", required=True, tracking=True)
    sub_equipment = fields.Many2one('msdata.checkpoints', string='Sub Equipment')
    task_planning_date = fields.Date(string="Scheduled Date",required=True,tracking=True)
    task_execution_date = fields.Datetime(string="Executed Date",tracking=True)
    responsible_team = fields.Many2one('res.users',string="Responsible", tracking=True)
    time_duration = fields.Float(string="Maintenance Duration",tracking=True)
    task_internal_notes = fields.Text(string="Remarks",tracking=True)
    task_approval_notes = fields.Text(string="Approver Notes",tracking=True,readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Technician Assignment'),
        ('work_in_progress', 'Work In Progress'),
        ('approval_process', 'Approval_Process'),
        ('approve', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancelled')
    ], default="draft", string="Status", tracking=True)
    job_confirmation_date = fields.Datetime(string="Task Confirmation Date")
    # ------------------Ini Connect ke Module UAC ------------------------------------------#
    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', readonly=True, tracking=True)
    existing_status = fields.Char(string="Current Status", readonly=True, tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", readonly=True, tracking=True)
    button_visible = fields.Boolean(compute='_compute_button_visibility', store=False)
    button_done_visible = fields.Boolean(compute='_compute_done_button_visibility', store=False)
    cancel_button_visibility = fields.Boolean(compute='_compute_cancel_button_visibility', store=False)
    text_input_activation = fields.Boolean(compute='_compute_text_input_activation', store=False)

    # -------------------------------------------------------------------------------------#
    @api.depends('job_confirmation_date')
    def submit_job_as_done(self):
        for record in self:
            if record.env.user == record.responsible_team:
                current_datetime = fields.Datetime.now()
                record.time_duration = (current_datetime - record.job_confirmation_date).total_seconds()/3600.0
                record.task_execution_date = current_datetime
                record.state='approval_process'
                # UAC Configuration to raise document status as submitted for approval
                if not self.approval_route_id:
                    raise ValidationError('Approval route is not defined.')
                next_step = self.approval_route_id.step_ids.sorted(key='sequence')[0]
                self.current_step_id = next_step
                self.existing_status = 'Tasklist submitted for approval'
                self.pending_approval_by = next_step.user_id
                self.upcoming_status = next_step
            else:
                raise ValidationError('You are not authorized to confirm this task, responsible team only')
    def submit_job_confirmation_process(self):
        self.job_confirmation_date = datetime.now()
        self.state='work_in_progress'
    def submit_technician_assignment(self):
        if not self.responsible_team:
            raise ValidationError('Technicians must be assigned first')
        else:
            config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
            if config:
                vals = {
                    'approval_route_id': config.approval_route_id.id,
                    'state': 'assigned'
                }
                self.write(vals)
            else:
                raise ValidationError('No Approval Route Configured For These Process')
    def action_draft(self):
        self.state = 'draft'
        self.responsible_team = None
        self.job_confirmation_date = ""
        self.task_execution_date = ""

    def _compute_text_input_activation(self):
        for record in self:
            if record.env.user == record.create_uid:
                if record.state == 'submit_request':
                   record.text_input_activation = True
                else:
                    record.text_input_activation = False
            else:
                record.text_input_activation = False

    def _compute_done_button_visibility(self):
        for record in self:
            if record.env.user == record.create_uid:
                if record.state == 'approve':
                    record.button_done_visible = True
                else:
                    record.button_done_visible = False
            else:
                record.button_done_visible = False

    def _compute_cancel_button_visibility(self):
        for record in self:
            if record.state == 'rejected':
                 record.cancel_button_visibility = True
            else:
                record.cancel_button_visibility = False
    def _compute_button_visibility(self):
        for record in self:
            if record.pending_approval_by:
                record.button_visible = (record.pending_approval_by.id == self.env.user.id)
            else:
                record.button_visible = False

    @api.model
    def create(self, vals):
        if vals.get('id_maintenance_task', 'New') == 'New':
            # Get the current date and time
            current_date = datetime.now()
            # Extract the month,day,and year
            month_number = current_date.month
            day_number = current_date.day
            year = current_date.year
            # Generate the sequence number
            sequence = self.env['ir.sequence'].next_by_code('oa.acmaintenance.request') or '00000'
            # Combine them into the final name
            vals['id_maintenance_task'] = f'PTMC-{sequence}/{month_number}/{day_number}/{year}'

        return super(OAMachineMaintenance, self).create(vals)

    @api.onchange('equip_id')
    def _onchange_equipment_id(self):
        if self.equip_id:
            self.serial_number = self.equip_id.serial_number
            self.asset_number = self.equip_id.asset_number
            self.pkt_number = self.equip_id.pkt_number
            self.kwh_equipment = self.equip_id.equipment_capacity
            self.brand_model_type = f"{self.equip_id.brand_name}/{self.equip_id.equipment_model}/{self.equip_id.manuf_year}"
        else:
            self.serial_number = None
            self.asset_number = None
            self.pkt_number = None
            self.kwh_equipment = None
            self.brand_model_type = None

    @api.onchange('maintenance_asset_group')
    def _onchange_field_a_id(self):
        """Update options in field_b_id based on the selected field_a_id."""
        if self.maintenance_asset_group:
            # Search for matching records in Model C
            matching_records = self.env['msdata.checkpoints'].search([('group_id', '=', self.maintenance_asset_group.id)])
            if matching_records:
                # Set domain to show matching records
                return {
                    'domain': {
                        'sub_equipment': [('id', 'in', matching_records.ids)]
                    }
                }
            else:
                # No matching records found, clear field_b_id and set domain to empty
                self.sub_equipment = False
                return {
                    'domain': {
                        'sub_equipment': [('id', '=', False)]
                    }
                }
        else:
            # No value selected in field_a_id, clear field_b_id and set domain to empty
            self.sub_equipment = False
            return {
                'domain': {
                    'sub_equipment': [('id', '=', False)]
                }
            }
    def action_analytic_testing(self):
        # for record in self:
        #     print(record.equip_id.id)
        checkequipmentid = self.env['oa.master.equipment'].search([('id', '=', self.equip_id.id)])
        for result in checkequipmentid:
            related_maintenance_records = result.id_detail_maintenance
            if related_maintenance_records:
                for maintenance in related_maintenance_records:
                    print("Maintenance ID:", maintenance.id)
                    print("Maintenance Type:", maintenance.id_maintenance_type.name)
                    print("Sub Equipment:", maintenance.name.point_to_check) # Adjust the field name as necessary
                    print("Frequency:", maintenance.maintenance_freq)
                    print("% Unit Condition Min:", maintenance.percentage_condition_min)
                    print("% Unit Condition Max:", maintenance.percentage_condition_max)
            else:
                print('No Maintenance ID recorded')

        # import pdb;
        # pdb.set_trace()




