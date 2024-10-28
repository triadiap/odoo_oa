# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class MasterStatusKegiatan(models.Model):
    _name = "status.kegiatan"
    _description = "Status Kegiatan Pengembangan & Pemberdayaan Masyarakat"

    nama_status = fields.Char(string="Status Name", required=True)
    deskripsi_status = fields.Text(string="Description")
    prosentase = fields.Char(string="Percentage (%)", required=True)

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.nama_status} - ({record.prosentase} %)"
            result.append((record.id, name))  # or any other meaningful field
        return result