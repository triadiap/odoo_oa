from odoo import api, models, fields, _

class MoIjinKeluar(models.Model):
    _name = "mo.ijinkeluar"

    pemohon = fields.Many2one("res.users", string="Pemohon", required=True)
    transportasi = fields.Char(string="Transportasi yang digunakan")
    jenis_keperluan = fields.Selection([
        ("Dinas", "Dinas"),
        ("Pribadi", "Pribadi"),
    ], string="Keperluan", required=True)
    file_attc = fields.Binary(string="Scan Dokumen")
    tujuan = fields.Text(string="Tujuan")
    tanggal_pergi = fields.Datetime(string="Tanggal & Jam Pergi", required=True)
    tanggal_pulang = fields.Datetime(string="Tanggal & Jam Pulang", required=True)
