from odoo import api, models, fields, _

class HcSuratPerintahPembelianLangsung(models.Model):
    _name = "hc.surat.perintah.pembelian.langsung"
    _description = "Model for SPPL module"

    tanggal = fields.Date(string="Tanggal", required=True)
    jam = fields.Float(string="Jam Waktu Pembelian", required=True)
    nama_kios = fields.Char(string="Nama Kios Pengambilan", required=True)
    keterangan = fields.Text(string="Keterangan Pemerintah Atasan")
    nominal = fields.Float(string="Nominal Pembelian")
    file = fields.Binary(string="Soft Copy SPPLK", required=True)