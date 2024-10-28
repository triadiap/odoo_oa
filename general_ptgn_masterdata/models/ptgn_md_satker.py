from odoo import api, fields, models, _

class PtgnMdSatker(models.Model):
    _name = "ptgn.md.satker"

    _description = "Master Data Satuan Kerja (Satker)"

    kode_satker = fields.Char(string="Kode Satker", required="True")
    name = fields.Char(string="Nama Satker", required="True")
    singkatan = fields.Char(string="Singkatan", required="True")
    tipe_satker = fields.Selection([
        ("Internal", "Internal"),
        ("Eksternal", "Eksternal"),
    ], string="Tipe Satker", default="Internal", required="True")