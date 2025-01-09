from odoo import api, models, fields, _

class HcSuratPerintahPembelianLangsung(models.Model):
    _name = "hc.surat.perintah.pembelian.langsung"
    _description = "Model for SPPL module"

    tanggal = fields.Date(string="Tanggal", required=True)
    jam = fields.Float(string="Jam Waktu Pembelian", required=True)
    nama_kios = fields.Char(string="Nama Kios Pengambilan", required=True)
    nama_barang = fields.Char(string="Nama Barang", required=True)
    keterangan = fields.Text(string="Keterangan Pemerintah Atasan")
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.user.company_id.currency_id.id
    )
    nominal = fields.Monetary(string="Nominal Pembelian")
    file = fields.Binary(string="Soft Copy SPPLK", required=True)
    state = fields.Selection([
        ("pending", "Pending"),
        ("submitted", "Submitted"),
    ], string="Status Submit", default="pending", readonly=True)

    def name_get(self):
        result = []
        for record in self:
            display_name = f"{record.tanggal} - {record.nama_kios}"  # Custom display
            result.append((record.id, display_name))
        return result