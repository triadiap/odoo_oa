# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class MasterKategoriKegiatan(models.Model):
    _name = "kategori.kegiatan"
    _description = "Kategori Kegiatan Pengembangan & Pemberdayaan Masyarakat"

    nama_kategori = fields.Char(string="Category", required=True)
    deskripsi_kategori = fields.Text(string="Description")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.nama_kategori))  # or any other meaningful field
        return result