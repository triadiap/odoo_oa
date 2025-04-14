from odoo import api, models, fields, _

class MoMasterLokasi(models.Model):
    _name = "mo.master.lokasi"
    _description = "MO Master Data Lokasi"

    name = fields.Char(string="Nama Lokasi", required=True)