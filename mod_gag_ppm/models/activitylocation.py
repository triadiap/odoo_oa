# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class DaftarLokasi(models.Model):
    _name = "daftar.lokasi"
    _description = "Master Data Lokasi"


    name=fields.Char(string="Location Name", required=True)
    kode_lokasi = fields.Char(string="Location Code")
