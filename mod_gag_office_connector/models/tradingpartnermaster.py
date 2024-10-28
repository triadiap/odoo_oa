# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class TradingPartnerMaster(models.Model):
    _name = "oa.trading.partner"
    _description = "Office Connector Trading Partner Master Data"

    name = fields.Char(string="Trading Partner Name",required=True,tracking=True)
    application_name = fields.Char(string="Apps Name",required=True,tracking=True)
    obj_to_connect = fields.Text(string="Description",tracking=True)
    vendor_name = fields.Many2one('res.partner',string="Vendor Name",tracking=True,required=True)
    start_date = fields.Datetime(string="Start Date",tracking=True,required=True)
    end_date = fields.Datetime(string="End Date",tracking=True,required=True)
    trading_partner_token = fields.Char(string='Access Token', tracking=True)

    def generate_trading_partner_token(self):
        import secrets
        self.trading_partner_token = secrets.token_hex(16)