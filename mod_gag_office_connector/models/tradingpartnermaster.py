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
    count_api_use = fields.Integer(compute='_compute_use_counts', string="API Used")
    btn_visible = fields.Boolean(compute='_compute_use_counts', store=False)
    hide_css = fields.Html(string='CSS', compute='_compute_use_counts', sanitize=False, store=False)
    def generate_trading_partner_token(self):
        import secrets
        self.trading_partner_token = secrets.token_hex(16)

    def _compute_use_counts(self):
        for rec in self:
            rec.count_api_use = self.env['oa.api.hit.logs'].search_count([('name','=',rec.id)])
            if rec.count_api_use > 0:
                rec.hide_css =  ('''
                                   <style>
                                   .o_cp_action_menus {display: none !important;}
                                   </style>
                                   '''
                                   )
                rec.btn_visible = True
            else:
                rec.hide_css = False
                rec.btn_visible = False



