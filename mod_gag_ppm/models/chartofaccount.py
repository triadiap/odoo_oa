# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class MasterChartOfAccount(models.Model):
    _name = "tabel.coa"
    _description = 'COA Master Data Table'

    kode_coa = fields.Char(string="Code", required=True, tracking=True)
    name = fields.Char(string="Account Name", required=True, tracking=True)
    coa_description = fields.Char(string="Description", tracking=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.kode_coa))  # or any other meaningful field
        return result