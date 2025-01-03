# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class MasterPillarGroup(models.Model):
    _name = "pillar.group"
    _description = "PPM Pillar Group"
    _order = "sequence"

    nama_pillar = fields.Char(string="Pillar Name", required=True)
    pillar_description = fields.Text(string="Description")
    pillar_prefix = fields.Char(string="Prefix Code", required=True)
    sequence = fields.Integer(string="Sequence")


    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.nama_pillar))  # or any other meaningful field
        return result
