from odoo import api, models, fields, _

class CorsecRisalahRapatDireksi(models.Model):
    _name = "corsec.risalah.rapat.komisaris"
    _description = "Model for CORSEC Risalah Rapat Komisaris"

    tanggal = fields.Date(string="Tanggal", required=True)
    jam_mulai = fields.Float(string="Jam Mulai", required=True)
    jam_selesai = fields.Float(string="Jam Selesai", required=True)
    tempat = fields.Char(string="Tempat", required=True)
    agenda = fields.Text(string="Agenda Rapat", required=True)
    lok_simpan = fields.Char(string="Lokasi Penyimpanan Dokumen")
    is_file_asli = fields.Boolean(string="Ada File Asli?")
    no_dokumen = fields.Char(string="No. Dokumen")
    jenis_dokumen = fields.Selection([
        ("risalah", "Risalah"),
        ("sirkuler", "Sirkuler"),
        ("pengantar", "Surat Pengantar"),
    ], string="Jenis Dokumen", required=True)
    status = fields.Selection([
        ("drafting", "Drafting oleh Sekretaris Dewan Komisaris"),
        ("review", "Review Corsec & Legal Senior Manager"),
        ("rev_dir_1", "Review Presdir"),
        ("rev_dir_2", "Review Direktur Operasi"),
        ("rev_dir_3", "Review Direktur HR"),
        ("rev_kom_1", "Review Dewan Komisaris"),
        ("paraf_1", "Paraf Legal"),
        ("paraf_2", "Paraf Sekretaris Dewan Komisaris"),
        ("sign_dir", "Tanda Tangan Direksi"),
        ("sign_kom", "Tanda Tangan Komisaris"),
    ], string="Status", required=True, default="drafting")

    list_dok = fields.One2many("corsec.risalah.rapat.komisaris.dok", "id_risalah", string="Dokumen")


class DokumenRisalahRapat(models.Model):
    _name = "corsec.risalah.rapat.komisaris.dok"
    _description = "Dokumen Risalah Rapat Komisaris"

    name = fields.Char(string="Nama Dokumen", required=True)
    file = fields.Binary(string="Soft File", required=True)

    id_risalah = fields.Many2one("corsec.risalah.rapat.komisaris", string="ID Risalah")