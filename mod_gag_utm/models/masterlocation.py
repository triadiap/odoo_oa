# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class LocationMasterData(models.Model):

    _name = "msdata.location"
    _description = "Location Master Data Input"

    location_name = fields.Char(string="Location Name", required=True)
    location_description = fields.Char(string="Description")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.location_name))  # or any other meaningful field
        return result
