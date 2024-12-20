from odoo import api, models, fields, _

class CorsecListAktaNotaris(models.Model):
    _name = "corsec.list.akta.notaris"
    _description = "Model for Corsec List Akta Notaris"

    nomor_akta = fields.Char(string="No. Akta", required=True)
    tanggal_akta = fields.Date(string="Tanggal", required=True)
    notaris = fields.Char(string="Nama Notaris", required=True)
    keterangan = fields.Text(string="Keterangan")
    scan_copy = fields.Boolean(string="Ada Scan Copy")
    file_scan = fields.Binary(string="Lampiran Soft Copy")
    asli_akta = fields.Boolean(string="Akta Asli")
    lok_simpan = fields.Char(string="Tempat Arsip")
    jenis_akta = fields.Char(string="Jenis Akta", required=True)

    list_sk_sp = fields.One2many("corsec.list.sksp", "id_akta", string="List SK - SP")

class CorsecListAktaSkSp(models.Model):
    _name = "corsec.list.sksp"
    _description = "Model for list SK-SP for Akta Notaris"

    jenis = fields.Selection([
        ("sk", "SK"),
        ("sp", "SP"),
    ], string="Jenis", required=True)
    no_surat = fields.Char(string="No. Surat", required=True)
    tanggal = fields.Date(string="Tanggal", required=True)
    file = fields.Binary(string="Lampiran Surat")
    asli = fields.Boolean(string="Ada File Asli?")
    lok_simpan = fields.Char(string="Lokasi Simpan")

    id_akta = fields.Many2one("corsec.list.akta.notaris", string="ID Akta")