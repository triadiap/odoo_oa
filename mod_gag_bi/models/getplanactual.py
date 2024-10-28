# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class GetPlanActualProduction(models.Model):
    _name = "bi.planactual.production"
    _description = "Vendor Master Data For Office Automation"

    vendor_id = fields.Integer(string='Vendor ID')
    production_date = fields.Date(string='Production Date')
    qty_plan = fields.Float(string="Quantity Of Plan")
    qty_actual = fields.Float(string="Quantity Of Actual")
