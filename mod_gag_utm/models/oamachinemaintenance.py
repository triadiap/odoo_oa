# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime,timedelta

class OAMachineMaintenance(models.Model):
    _name="oa.machine.maintenance"
    _inherit = ["mail.thread", "mail.activity.mixin", "mail.tracking.value"]
    _description="Office Automation Machine Maintenance Form"

    name = fields.Char(string="Task Description",required=True,tracking=True)
    id_maintenance_task = fields.Char(string="ID Task",required=True,copy=False, default='New')
    maintenance_task_type = fields.Selection([
        ('top_over_haul', 'TOP OVER HAUL'),
        ('minor_over_haul', 'MINOR OVER HAUL'),
        ('general_over_haul', 'GENERAL OVER HAUL'),
        ('services', 'SERVICES'),
        ('greasing', 'GREASING'),
        ('body_repair', 'BODY REPAIR'),
        ('corrective_maintenance', 'CORRECTIVE MAINTENANCE'),
        ('breakdown_maintenance', 'BREAKDOWN MAINTENANCE')
    ], default="top_over_haul", string="Maintenance Type", tracking=True,required=True)
    equip_id = fields.Many2one('oa.master.equipment', string='Equipment Name',required=True,tracking=True)
    brand_model_type = fields.Char(string='Brand/Type/Year', tracking=True,readonly=True)
    serial_number = fields.Char(string='Serial Number', tracking=True,readonly=True)
    asset_number = fields.Char(string='Asset Number', tracking=True,readonly=True)
    pkt_number = fields.Char(string='PKT Number', tracking=True,readonly=True)
    kwh_equipment = fields.Char(string='Power (Kw)', tracking=True,readonly=True)
    maintenance_asset_group = fields.Many2one('point.group', string="Asset Group", required=True, tracking=True)
    sub_equipment = fields.Many2one('msdata.checkpoints', string='Sub Equipment',required=True,tracking=True)
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
            sequence = self.env['ir.sequence'].next_by_code('oa.machine.maintenance') or '00000'
            # Combine them into the final name
            vals['id_maintenance_task'] = f'PMTC-{sequence}/{month_number}/{day_number}/{year}'
            # Add logic for dependent fields based on equip_id
        if vals.get('equip_id'):
                equip_id = self.env['oa.master.equipment'].browse(vals['equip_id'])
                vals.update({
                    'serial_number': equip_id.serial_number,
                    'asset_number': equip_id.asset_number,
                    'pkt_number': equip_id.pkt_number,
                    'kwh_equipment': equip_id.equipment_capacity,
                    'brand_model_type': f"{equip_id.brand_name}/{equip_id.equipment_model}/{equip_id.manuf_year}",
                })
        else:
            vals.update({
                    'serial_number': None,
                    'asset_number': None,
                    'pkt_number': None,
                    'kwh_equipment': None,
                    'brand_model_type': None,
                })

        return super(OAMachineMaintenance, self).create(vals)

    def write(self,vals):
        for record in self:
            if 'equip_id' in vals or record.equip_id:
                equip_id = record.equip_id if 'equip_id' not in vals else self.env['oa.master.equipment'].browse(
                    vals['equip_id'])
                vals.update({
                    'serial_number': equip_id.serial_number if equip_id else None,
                    'asset_number': equip_id.asset_number if equip_id else None,
                    'pkt_number': equip_id.pkt_number if equip_id else None,
                    'kwh_equipment': equip_id.equipment_capacity if equip_id else None,
                    'brand_model_type': f"{equip_id.brand_name}/{equip_id.equipment_model}/{equip_id.manuf_year}" if equip_id else None,
                })
        return super(OAMachineMaintenance, self).write(vals)

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

    def maintenance_analytic(self,equip_id, maintenance_task_type, sub_equipment, task_execution_date,maintenance_asset_group):
        checkequipmentid = self.env['oa.master.equipment'].search([('id', '=', equip_id.id)])
        for result in checkequipmentid:
            related_maintenance_records = result.id_detail_maintenance
            if related_maintenance_records:
                for maintenance in related_maintenance_records:
                    if maintenance.id_maintenance_type == maintenance_task_type and sub_equipment.id == maintenance.name.id :
                        # Fetch the latest maintenance record once
                        latest_maintenance = self.env['oa.equipment.maintenance'].search(
                            [('equipment_id.id', '=', equip_id.id)],
                            limit=1,
                            order='cumulative_hour desc'
                        )
                        # Fetch the second latest maintenance record
                        second_latest_maintenance = self.env['oa.equipment.maintenance'].search(
                            [('equipment_id', '=', equip_id.id)],
                            limit=1,
                            offset=1,  # Skip the first record
                            order='cumulative_hour desc'
                        )
                        if latest_maintenance:
                            second_cumulative_hour = second_latest_maintenance.cumulative_hour if second_latest_maintenance else 0
                            daily_operation_hours = latest_maintenance.operation_hour - second_cumulative_hour
                            current_cumulative_hours = latest_maintenance.cumulative_hour
                            operation_percentage = latest_maintenance.work_efficiency

                            if current_cumulative_hours > maintenance.maintenance_freq:
                                # Calculate the remaining hours until the next maintenance
                                remaining_hours = maintenance.maintenance_freq - (current_cumulative_hours % maintenance.maintenance_freq)
                                # Adjust the daily operation hours based on the operation percentage
                                effective_daily_hours = daily_operation_hours * (operation_percentage / 100)
                                # Calculate the days to the next maintenance
                                if effective_daily_hours > 0:
                                    days_to_next_maintenance = remaining_hours / effective_daily_hours
                                    next_date = task_execution_date + timedelta(days=days_to_next_maintenance)
                                    current_date = datetime.now()
                                    # Extract the month,day,and year
                                    month_number = current_date.month
                                    day_number = current_date.day
                                    year = current_date.year
                                    # Generate the sequence number
                                    sequence = self.env['ir.sequence'].next_by_code('oa.machine.maintenance') or '00000'
                                    id_maintenance_task = f'PMTC-{sequence}/{month_number}/{day_number}/{year}'
                                    check_similar_schedule = self.env['oa.machine.maintenance'].search([('name', '=', f"{maintenance_task_type.upper()} - {equip_id.name}"),('task_planning_date','=',next_date),('equip_id','=',equip_id.id),('sub_equipment','=',sub_equipment.id)])
                                    if not check_similar_schedule:
                                        self.create({
                                            'name':f"{maintenance_task_type.upper()} - {equip_id.name}",
                                            'id_maintenance_task' : id_maintenance_task,
                                            'maintenance_asset_group': maintenance_asset_group.id,
                                            'maintenance_task_type' : maintenance_task_type,
                                            'equip_id':equip_id.id,
                                            'task_planning_date':next_date,
                                            'sub_equipment':sub_equipment.id,
                                            'serial_number': equip_id.serial_number,
                                            'asset_number': equip_id.asset_number,
                                            'pkt_number': equip_id.pkt_number,
                                            'kwh_equipment': equip_id.equipment_capacity,
                                            'brand_model_type': f"{equip_id.brand_name}/{equip_id.equipment_model}/{equip_id.manuf_year}"
                                        })
                                    else:
                                        raise ValidationError("Scheduled Maintenance Already Exist")
            else:
                raise ValidationError("No Maintenance ID recorded")





