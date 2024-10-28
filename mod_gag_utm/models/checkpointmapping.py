# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class MasterCheckPoints(models.Model):
    _name = "msdata.checkpoints"
    _description = "Checkpoint Master Data Mapping"

    point_to_check = fields.Char(string="Point To Check", required=True)
    ptc_description = fields.Text(string="Description")
    group_id =  fields.Many2one('point.group', string="Area Group", required=True, tracking=False)

    def name_get(self):
        result = []
        for record in self:
            category_name = record.group_id.group_name if record.group_id else 'No Group'
            name = f"({category_name}) - {record.point_to_check}"
            result.append((record.id, name))  # or any other meaningful field
        return result
