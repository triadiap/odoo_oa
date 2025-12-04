# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import timedelta

class ReportingType(models.Model):
    _name = 'oa.reporting.type'
    _description = 'Auto Reporting Type Master Data'

    name = fields.Char(string="Document Type")
