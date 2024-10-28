# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class GetMasterVendor(models.Model):
    _name = "oa.master.vendor"
    _description = "Vendor Master Data For Office Automation"

    name = fields.Char(string='Vendor Name')
    description = fields.Text(string="Description")
