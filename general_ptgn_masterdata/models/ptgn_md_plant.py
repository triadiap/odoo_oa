from odoo import api, fields, models, _

class PtgnMdPlant(models.Model):
    _name = "ptgn.md.plant"

    _description = "Master Data Plant"

    plant_id = fields.Char(string="Kode Plant", required="True")
    name = fields.Char(string="Nama Plant", required="True")
    tipe_satker = fields.Selection([
        ("MINE", "Area Tambang"),
        ("OFFICE", "Area Kantor"),
    ], string="Tipe Plant", default="MINE", required="True")