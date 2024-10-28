# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class AirConditioningMaintenanceRequest(models.Model):
    _name = 'oa.acmaintenance.request'
    _inherit = ["mail.thread", "mail.activity.mixin","mail.tracking.value"]
    _description = 'Office Automation Air Conditioning Maintenance Request Form'

    name = fields.Char(string="Description", required = True, tracking=True)
    equipment_id = fields.Many2one('oa.master.equipment', string='Equipment Name')
    brand_model_type = fields.Char(string='Brand/Type/Year', tracking=True)
    serial_number = fields.Char(string='Serial Number', tracking=True)
    asset_number = fields.Char(string='Asset Number', tracking=True)
    pkt_number = fields.Char(string='PKT Number', tracking=True)
    kwh_equipment = fields.Char(string='Power (Kw)', tracking=True)
    request_id = fields.Char(string="Request ID", readonly=True, copy=False, default='New')
    location_id = fields.Many2one('msdata.location', required=True, tracking=True)
    request_note = fields.Text(string="Notes",tracking=True)
    date_to_action_need = fields.Date(string="Request Date", required=True, tracking=True)
    ac_technicians = fields.Many2many('res.users',string="Assigned Technicians",tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit_request', 'Submitted'),
        ('assigned', 'Technician Assignment'),
        ('work_in_progress', 'Work In Progress'),
        ('approval_process', 'Approval_Process'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancelled')
    ], default="draft", string="Status", tracking=True)
    action_priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], default='1', string="Priority Level", tracking=True)
    picture_before_1 = fields.Binary(string="Picture Before")
    picture_after_1 = fields.Binary(string="Picture After")
    job_confirmation_date = fields.Date(string="Task Confirmation Date")
    job_finalization_date = fields.Date(string="Task Finalization Date")
    # ------------------Ini Connect ke Module UAC ------------------------------------------#
    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step',tracking=True)
    existing_status = fields.Char(string="Current Status", tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", readonly=True, tracking=True)
    button_visible = fields.Boolean(compute='_compute_button_visibility', store=False)
    button_done_visible = fields.Boolean(compute='_compute_done_button_visibility',store=False)
    cancel_button_visibility = fields.Boolean(compute='_compute_cancel_button_visibility',store=False)
    text_input_activation = fields.Boolean(compute='_compute_text_input_activation',store=False)
    # -------------------------------------------------------------------------------------#
    tracking_value_ids = fields.One2many(
        'mail.tracking.value', string='Field Change History',
        compute='_compute_tracking_value_ids', store=False
    )

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.request_id} - {record.location_id.location_name} - {record.name}"
            result.append((record.id, name))  # or any other meaningful field
        return result
    def _compute_tracking_value_ids(self):
        for record in self:
            # Fetch all related messages
            messages = self.env['mail.message'].search([
                ('res_id', '=', record.id),
                ('model', '=', self._name)
            ])
            # Fetch all related tracking values
            tracking_values = self.env['mail.tracking.value'].search([
                ('mail_message_id', 'in', messages.ids)
            ])
            # Assign the related tracking values using the proper syntax
            if tracking_values:
                record.tracking_value_ids = [(6, 0, tracking_values.ids)]
            else:
                record.tracking_value_ids = [(5, 0, 0)]  # Clear the list if no values are found

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id:
            self.serial_number = self.equipment_id.serial_number
            self.asset_number = self.equipment_id.asset_number
            self.pkt_number = self.equipment_id.pkt_number
            self.kwh_equipment = self.equipment_id.equipment_capacity
            self.brand_model_type = f"{self.equipment_id.brand_name}/{self.equipment_id.equipment_model}/{self.equipment_id.manuf_year}"
        else:
            self.serial_number = None
            self.asset_number = None
            self.pkt_number = None
            self.kwh_equipment = None
            self.brand_model_type = None

    def request_set_as_done(self):
        self.state = 'done'
    def technician_confirmation_as_done(self):
        # UAC Configuration to raise document status as submitted for approval
        if not self.approval_route_id:
            raise ValidationError('Approval route is not defined.')
        next_step = self.approval_route_id.step_ids.sorted(key='sequence')[0]
        self.current_step_id = next_step
        self.state = 'approval_process'
        self.existing_status = 'Tasklist submitted for approval'
        self.pending_approval_by = next_step.user_id
        self.upcoming_status = next_step
        self.job_finalization_date = datetime.now()
    def submit_job_confirmation_process(self):
        self.job_confirmation_date = datetime.now()
        self.state='work_in_progress'
    def submit_technician_assignment(self):
        if not self.ac_technicians:
            raise ValidationError('Technicians must be assigned first')
        else:
            self.state = 'assigned'
    def submit_as_request(self):
        # UAC Find the configured approval route for the current model for new document creation
        config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
        if config:
            vals = {
                'approval_route_id' : config.approval_route_id.id,
                'state' : 'submit_request'
            }
            self.write(vals)
        else:
            raise ValidationError('No Approval Route Configured For These Process')

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
            if record.env.user == record.create_uid:
                if record.state == 'rejected' or record.state == 'submit_request':
                    record.cancel_button_visibility = True
                else:
                    record.cancel_button_visibility = False
            else:
                record.cancel_button_visibility = False
    def _compute_button_visibility(self):
        for record in self:
            # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.pending_approval_by.id == self.env.user.id)
            else:
                record.button_visible = False

    def action_draft(self):
        self.state = 'draft'
    @api.model
    def create(self, vals):
        if vals.get('request_id', 'New') == 'New':
            # Generate the sequence number
            sequence = self.env['ir.sequence'].next_by_code('oa.acmaintenance.request') or '00000'
            # Combine them into the final name
            vals['request_id'] = f'REQ-{sequence}'

        return super(AirConditioningMaintenanceRequest, self).create(vals)