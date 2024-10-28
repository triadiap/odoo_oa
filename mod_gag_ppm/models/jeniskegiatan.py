# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class MasterJenisKegiatan(models.Model):
    _name ="jenis.kegiatan"
    _description = "Jenis Kegiatan Pengembangan & Pemberdayaan Masyarakat"

    nama_jenis = fields.Char(string="Activity Type", required=True)
    deskripsi_jenis = fields.Text(string="Description")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.nama_jenis))  # or any other meaningful field
        return result
