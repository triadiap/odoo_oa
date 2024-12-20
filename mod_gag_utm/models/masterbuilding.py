# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class BuildingMasterData(models.Model):
    _name = "msdata.building"
    _description = "Building Master Data Input"

    building_name = fields.Char(string="Building Name", required=True)
    building_description = fields.Char(string="Description")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.building_name))  # or any other meaningful field
        return result