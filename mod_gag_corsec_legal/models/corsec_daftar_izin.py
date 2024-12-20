from odoo import api, models, fields, _

class CorsecDaftarIzin(models.Model):
    _name = "corsec.daftar.izin"
    _description = "Model for menu Daftar Izin"

    name = fields.Char(string="Nama Dokumen", required=True)
    nama_izin = fields.Char(string="Nama Izin", required=True)
    penerbit = fields.Char(string="Instansi Penerbit", required=True)
    tanggal = fields.Date(string="Tanggal Izin", required=True)
    no_izin = fields.Char(string="Nomor Izin", required=True)
    keterangan = fields.Text(string="Keterangan")
    jangka_waktu = fields.Char(string="Jangka Waktu")
    berakhir_pada = fields.Date(string="Berakhir Pada")
    status = fields.Selection([
        ("status_1", "Pembuatan SK Tim"),
        ("status_2", "Pemenuhan Data Administrasi"),
        ("status_3", "Persetujuan Manager"),
        ("status_4", "Persetujuan GM"),
        ("status_5", "Persetujuan Direksi"),
        ("status_6", "Proses Corsec & Legal"),
        ("status_7", "Pengiriman Kementrian Terkait"),
        ("status_8", "Revisi Kementrian"),
        ("status_9", "Pengajuan Ulang"),
        ("status_10", "Done"),
    ])
    lampiran = fields.Binary(string="Lampiran Soft Copy")

    list_syarat = fields.One2many("corsec.dokumen.persyaratan", "id_izin", string="Dokumen Persyaratan")

class PersyaratanDokumenIzin(models.Model):
    _name = "corsec.dokumen.persyaratan"
    _description = "Model for Daftar Dokumen Persyaratan Pengajuan Izin"

    name = fields.Char(string="Nama Dokumen", required=True)
    file = fields.Binary(string="Lampiran Dokumen", required=True)

    id_izin = fields.Many2one("corsec.daftar.izin", string="ID Izin")