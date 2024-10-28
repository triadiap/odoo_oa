# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import datetime

class SetPointAvailibility(models.Model):
    _name = "oa.setpoint.availibility"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Set Point / Target Machine Availibility & Efficiency"

    name = fields.Many2one('oa.master.equipment',string="Machine Name",required=True,tracking=True)
    setpoint_readiness = fields.Integer(string="Siap",required=True,default=1.00, tracking=True)
    setpoint_production = fields.Integer(string="Prod(Min)",required=True,default=1.00,tracking=True)
    setpoint_backup = fields.Integer(string="Cad(Min)",required=True,default=1.00,Tracking=True)
    setpoint_repair = fields.Float(string="Rep (Max)",required=True,default=1.00,Tracking=True)
    setpoint_breakdown_repair = fields.Float(string="Breakdown Repair BD (Max)",required=True,default=1.00)
    setpoint_stand_by = fields.Float(string="Standby (Max)",required=True,default=1.00)
    setpoint_tsc = fields.Float(string="Tunggu Suku Cadang (TSC) (Max)",required=True,default=1.00)
    setpoint_bd = fields.Float(string="Breakdown (BD) (Max)",required=True,default=1.00)
    year_setpoint = fields.Selection(selection='_get_years', string='Year Of Target / Set Point', default=lambda self: str(datetime.now().year), tracking=True,required=True)
    setpoint_note = fields.Text(string="Notes")
    setpoint_ma = fields.Float(string="% Machine Availibility (MA) / Year",tracking=True,required=True,default=100.00)
    setpoint_we = fields.Float(string="% Work Efficiency (WE) / Year", tracking=True, required=True, default=100.00)

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
    def _get_years(self):
        current_year = datetime.now().year
        year_range = 10  # Number of years to generate
        years = [(str(year), str(year)) for year in range(current_year, current_year + year_range)]
        return years
