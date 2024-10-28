from odoo import api, models, fields, _

class MpdBeritaAcaraSerahTerimaPekerjaan(models.Model):
    _name = "mpd.ba.serah.terima.pekerjaan"
    _description = "Model for Berita Acara Serah Terima Pekerjaan"

    name = fields.Char(string="Nama Pekerjaan", required=True)
    pic = fields.Many2one("res.users", string="PIC", required=True)
    mitra = fields.Char(string="Mitra / Vendor", required=True)
    tanggal_bast = fields.Date(string="Tanggal BASTP", required=True)
    file = fields.Binary(string="Soft Copy BASTP", required=True)