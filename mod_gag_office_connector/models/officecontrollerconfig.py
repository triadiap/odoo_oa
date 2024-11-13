# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import secrets

class OfficeConnectorConfig(models.Model):
    _name = 'office.connector.config'
    _description = 'Office Connector Configuration'

    name = fields.Char(string='Name', required=True)
    token = fields.Char(string='Link ID',tracking=True)
    trading_partner_name = fields.Many2many('oa.trading.partner',string="Trading Partner", required=True,tracking=True)
    sync_model = fields.Many2one('ir.model', string='Model to Sync',required=True, help="Select the model that will use this approval route.",ondelete='cascade', tracking=True)
    sync_fields = fields.Many2many('ir.model.fields', string='Fields to Sync',
                                   domain="[('model_id', '=', sync_model)]")
    sync_rule = fields.Selection([
        ('1', 'Unlimited'),
        ('2', 'By Time Range'),
    ], string='Sync Rule', default='1')

    id_api_log = fields.One2many('oa.api.hit.logs','api_id',string="API Hit Logs")
    hide_css = fields.Html(string='CSS', compute='_compute_status_counts', sanitize=False, store=False)
    # Fields to store count of each status code
    count_200 = fields.Integer(compute='_compute_status_counts', string="200 OK Count")
    count_400 = fields.Integer(compute='_compute_status_counts', string="400 Error Count")
    count_401 = fields.Integer(compute='_compute_status_counts', string="400 Error Count")
    count_402 = fields.Integer(compute='_compute_status_counts', string="400 Error Count")
    count_403 = fields.Integer(compute='_compute_status_counts', string="400 Error Count")
    count_500 = fields.Integer(compute='_compute_status_counts', string="500 Error Count")
    btn_visible = fields.Boolean(compute='_compute_status_counts',store=False)
    @api.depends('id_api_log.status')
    def _compute_status_counts(self):
        for record in self:
            logs = record.id_api_log
            record.count_200 = logs.filtered(lambda l: l.status == 200).mapped('id').__len__()
            record.count_400 = logs.filtered(lambda l: l.status == 400).mapped('id').__len__()
            record.count_401 = logs.filtered(lambda l: l.status == 401).mapped('id').__len__()
            record.count_402 = logs.filtered(lambda l: l.status == 402).mapped('id').__len__()
            record.count_403 = logs.filtered(lambda l: l.status == 403).mapped('id').__len__()
            record.count_500 = logs.filtered(lambda l: l.status == 500).mapped('id').__len__()
            if record.count_200 > 0 or record.count_400 > 0 or record.count_500 > 0 or record.count_401 > 0 or record.count_402 > 0 or record.count_403 > 0:
                record.hide_css = ('''
                                   <style>
                                   .o_cp_action_menus {display: none !important;}
                                   </style>
                                   '''
                                   )
                record.btn_visible = True
            else:
                record.hide_css = False
                record.btn_visible = False

    @api.model
    def create(self,vals):
        # Ensure token is generated before saving the record
        record = super(OfficeConnectorConfig, self).create(vals)
        record.generate_token()
        return record
    def generate_token(self):
        # Loop to ensure the generated token is unique
        unique_token_found = False
        while not unique_token_found:
            # Generate a random token
            token = secrets.token_hex(16)
            # Check if the token already exists in the database
            existing_token = self.env['office.connector.config'].search([('token', '=', token)], limit=1)
            # If token is unique, assign it to the record
            if not existing_token:
                self.token = token
                unique_token_found = True
    @api.model
    def sync_data(self, rest_api_name, sync_fields, filters=None, limit=None, offset=0):
        domain = filters if filters else []
        records = self.env[rest_api_name].search(domain,limit=limit, offset=offset)

        # Fetch the values for the given sync fields
        result = records.read(sync_fields)
        return result

class APIHitlogs(models.Model):

    _name = "oa.api.hit.logs"
    _description = "Office Connector API Hit Logs"
    _order = 'timestamp desc'  # Default ordering by timestamp in descending order

    name = fields.Many2one("oa.trading.partner", string="Trading Partner")
    status = fields.Integer(string="Status")
    message = fields.Text(string="Message")
    token_number = fields.Char(string="Token")
    api_id = fields.Many2one('office.connector.config',string="API Name")
    timestamp = fields.Datetime(string="Timestamp",default=fields.Datetime.now)
    filters_applied = fields.Text(string="Filters Applied")
    record_limit = fields.Char(string="Limit")
    record_offset = fields.Char(string="Offset")
