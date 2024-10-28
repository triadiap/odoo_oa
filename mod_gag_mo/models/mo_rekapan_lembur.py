from odoo import api, models, fields, _

class MoRekapanLembur(models.Model):
    _name = "mo.rekapan.lembur"
    _description = "Model for Rekapan Lembur module"

    periode_start = fields.Date(string="Tanggal", required=True)
    periode_end = fields.Date(string="Hingga", required=True)
    file = fields.Binary(string="Soft Copy Form Rekapan Lembur", required=True)