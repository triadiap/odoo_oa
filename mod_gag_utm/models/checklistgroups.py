# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class ChecklistGroup(models.Model):
    _name = "point.group"
    _description = "Building Checklist Item Groups"

    group_name = fields.Char(string="Group Name", required=True)
    desc_group = fields.Text(string="Group Description")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.group_name))  # or any other meaningful field
        return result