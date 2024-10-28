# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import datetime

class EquipmentMaintenance(models.Model):
    _name = 'oa.equipment.maintenance'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Equipment Maintenance Management'

    ljjm_id = fields.Char(string='Report ID', readonly=True, copy=False, default='New',tracking=True)
    equipment_id = fields.Many2one('oa.master.equipment',string='Equipment Name',required=True,tracking=True)
    brand_model_type = fields.Char(string='Brand/Type/Year', tracking=True)
    serial_number = fields.Char(string='Serial Number', tracking=True)
    asset_number = fields.Char(string='Asset Number',tracking=True)
    pkt_number = fields.Char(string='PKT Number',tracking=True)
    kwh_equipment = fields.Char(string='Power (Kw)',tracking=True)
    operator_name = fields.Many2one('res.users',tracking=True)
    operator_sign_date = fields.Datetime(string='Operator Sign Date',tracking=True)
    supervisor_name = fields.Many2one('res.users',tracking=True)
    supervisor_sign_date = fields.Datetime(string='Supervisor Sign Date',tracking=True)
    team_leader_name = fields.Many2one('res.users', tracking=True)
    team_leader_sign_date = fields.Datetime(string='Team Leader / Manager Sign Date', tracking=True)
    section_name = fields.Char(string='Section / Division',tracking=True)
    report_date = fields.Date(string='Date',tracking=True, required=True,default=fields.Date.context_today)
    cumulative_hour = fields.Float(string='Cumulative Hour (B)',tracking=True,required=True)
    plan_hour = fields.Float(string='Plan Hour (C)',tracking=True,default=12.00,required=True)
    operation_hour = fields.Float(string='Operation Hour (D)',tracking=True)
    service_hour = fields.Float(string='Service Hour (E)',tracking=True)
    standby_hour = fields.Float(string='Standby Hour (F)',tracking=True)
    total_operation_time = fields.Float(string='Total Operation Time (G)',tracking=True,compute='_compute_total_operation',store=True)
    tsc_mek = fields.Float(string='Tsc / Mek (H)',tracking=True)
    time_to_repair = fields.Float(string='Repair Time (J)',tracking=True)
    total_breakdown_time = fields.Float(string='Total Breakdown Hour (K)',tracking=True,compute='_compute_total_breakdown_hour',store=True)
    machine_availibility = fields.Float(string='% Machine Availibility (L)',tracking=True,compute='_compute_machine_availibility',store=True)
    work_efficiency = fields.Float(string='% Working Efficiency (M)', tracking=True,compute='_compute_working_efficiency', store=True)
    machine_oil_usage = fields.Float(string='Machine Oil (N)',tracking=True)
    filter_oil_usage = fields.Float(string='Filter Oil (P)',tracking=True)
    fuel_filter_usage = fields.Float(string='Fuel Filter (Q)', tracking=True)
    ff_separator_usage = fields.Float(string='FF Separator (R)', tracking=True)
    el_air_cleaner_usage = fields.Float(string='EL. Air Cleaner (S)',tracking=True)
    grease_usage = fields.Float(string='Grease (T)',tracking=True)
    fuel_usage = fields.Float(string='Fuel / BBM (U)',tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approval_process', 'Approval Process'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancelled')
    ], default="draft", string="Status", tracking=True)
    # ------------------Ini Connect ke Module UAC ------------------------------------------#
    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', readonly=True,tracking=True)
    existing_status = fields.Char(string="Current Status", readonly=True, tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", readonly=True, tracking=True)
    button_visible = fields.Boolean(compute='_compute_button_visibility', store=False)
    # -------------------------------------------------------------------------------------#
    tracking_value_ids = fields.One2many(
        'mail.tracking.value', string='Field Change History',
        compute='_compute_tracking_value_ids', store=False
    )

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
    def name_get(self):
        result = []
        for record in self:
            name = f"({record.ljjm_id}) - {record.equipment_id.name}"
            result.append((record.id, name))  # or any other meaningful field
        return result
    def _compute_button_visibility(self):
        for record in self:
                # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.pending_approval_by.id == self.env.user.id)
            else:
                record.button_visible = False
        # -----------------------------------------------------------------------
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


    @api.depends('plan_hour','operation_hour', 'service_hour','standby_hour')
    def _compute_total_operation(self):
        for rec in self:
            if rec.plan_hour < rec.operation_hour or rec.plan_hour < rec.service_hour or rec.plan_hour < rec.standby_hour:
                raise ValidationError('Value cannot be more than plan hour, check your inputs !')
            else:
                rec.total_operation_time = float(rec.operation_hour  + rec.service_hour + rec.standby_hour)

    @api.depends('plan_hour','tsc_mek','time_to_repair')
    def _compute_total_breakdown_hour(self):
        for rec in self:
            if rec.plan_hour < rec.tsc_mek or rec.plan_hour < rec.time_to_repair:
                raise ValidationError('Value cannot be more than plan hour, check your inputs !')
            else:
                rec.total_breakdown_time = float(rec.tsc_mek + rec.time_to_repair)
    @api.depends('plan_hour','total_breakdown_time')
    def _compute_machine_availibility(self):
        for rec in self:
            if rec.plan_hour < rec.total_breakdown_time:
                raise ValidationError('Value cannot be more than plan hour, check your inputs !')
            else:
                rec.machine_availibility = float((rec.plan_hour - rec.total_breakdown_time) /rec.plan_hour * 100)

    @api.depends('plan_hour','operation_hour','service_hour')
    def _compute_working_efficiency(self):
        for rec in self:
            if rec.plan_hour < rec.operation_hour or rec.plan_hour < rec.service_hour:
                raise ValidationError('Value cannot be more than plan hour, check your inputs !')
            else:
                rec.work_efficiency = float((rec.operation_hour + rec.service_hour) /rec.plan_hour * 100)

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'
        self.operator_name = None
        self.operator_sign_date = None
        self.supervisor_name = None
        self.supervisor_sign_date = None
        self.team_leader_name = None
        self.team_leader_sign_date = None

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get('ljjm_id', 'New') == 'New':
            # Generate the sequence number
            sequence = self.env['ir.sequence'].next_by_code('oa.equipment.maintenance') or '00000'
            # Combine them into the final name
            vals['ljjm_id'] = f'LJJM-{sequence}'
            vals['serial_number'] = self.equipment_id.serial_number
            vals['pkt_number'] = self.equipment_id.pkt_number
            vals ['kwh_equipment']= self.equipment_id.equipment_capacity
            vals ['brand_model_type'] = f"{self.equipment_id.brand_name}/{self.equipment_id.equipment_model}/{self.equipment_id.manuf_year}"
            # UAC Find the configured approval route for the current model for new document creation
        config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
        if config:
            vals['approval_route_id'] = config.approval_route_id.id

        return super(EquipmentMaintenance, self).create(vals)

    def action_open_budgets(self):
        print("Test")

    def action_approval_process(self):
        # UAC Configuration to raise document status as submitted for approval
        if not self.approval_route_id:
            raise ValidationError('Approval route is not defined.')
        next_step = self.approval_route_id.step_ids.sorted(key='sequence')[0]
        self.current_step_id = next_step
        self.state = 'approval_process'
        self.existing_status = 'Document Submitted By Operator'
        self.pending_approval_by = next_step.user_id
        self.upcoming_status = next_step
        self.operator_name = self.env.user.id
        self.operator_sign_date = fields.Datetime.now()
        # -----------------------------------------------------------------------
class ReportMaWe(models.Model):
    _name = 'oa.report.mawe'
    _description = " Monthly %MA and % WE Utility and Maintenance Report"
    _auto = False

    equipmentid = fields.Many2one('oa.master.equipment',string="Machine ID")
    equipment_info = fields.Char(string='Machine Name')
    reportdate = fields.Date(string="Report Date")
    planhour = fields.Float(string="Plan Hour")
    cumulativehour = fields.Float(string="Cumulative Hour")
    machineavailibility = fields.Float(string="Machine Availibility")
    efficiency = fields.Float(string="Efficiency")
    percent_ma = fields.Float(string="% Machine Availibility")
    percent_we = fields.Float(string="% Work Efficiency")

    def init(self):
        tools.drop_view_if_exists(self._cr,'oa_report_mawe')
        self._cr.execute("""
            CREATE OR REPLACE VIEW oa_report_mawe AS(
                SELECT
                    row_number() OVER() as id,  -- A unique id for each row
                    m.equipment_id AS equipmentid,
                    CONCAT(i.name, ' - ', i.serial_number) AS equipment_info,
                    m.report_date AS reportdate,
                    m.plan_hour AS planhour,
                    m.cumulative_hour AS cumulativehour,
                    m.machine_availibility AS machineavailibility,
                    m.work_efficiency AS efficiency,
                    (plan_hour  - total_breakdown_time) / SUM(plan_hour) OVER (PARTITION BY equipment_id) * 100 AS percent_ma,
                    (operation_hour + service_hour) / SUM(plan_hour) OVER (PARTITION BY equipment_id) * 100 AS percent_we
                FROM 
                    oa_equipment_maintenance m
                JOIN
                    oa_master_equipment i ON m.equipment_id = i.id
                )
        """)








