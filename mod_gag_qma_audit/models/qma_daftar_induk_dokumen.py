from odoo import api, models, fields, _

class QmaDaftarIndukDokumen(models.Model):
    _name = "qma.daftar.induk.dokumen"
    _description = "Model for QMA Daftar Induk Dokumen"

    jenis_dokumen = fields.Many2one("qma.master.jenis.dokumen", string="Jenis Dokumen", required=True)
    name = fields.Char(string="Judul Dokumen", required=True)
    satker = fields.Many2one("hr.department", string="Satker", required=True)
    status_sop = fields.Many2one("qma.master.status.sop", string="Status SOP", required=True)
    matriks_rkab = fields.Char(string="Matriks RKAB")
    no_dok_lama = fields.Char(string="No. Dokumen Lama")
    no_dok_penyesuaian = fields.Char(string="No. Dokumen Penyesuaian")
    status_pengajuan = fields.Selection([
        ("done", "Done"),
        ("kadaluarsa", "Kadaluarsa"),
        ("perubahan", "Perubahan"),
        ("review", "Review"),
        ("usulan", "Usulan"),
    ], string="Status Pengajuan", required=True, default="usulan")
    rev_0 = fields.Date(string="Revisi 0", required=True)
    status_dok = fields.Selection([
        ("aktif", "Aktif"),
        ("kadaluarsa", "Kadaluarsa"),
    ], string="Status Dokumen", required=True, default="aktif")
    file = fields.Binary(string="Soft Copy Dokumen")

    rev_list = fields.One2many("qma.daftar.induk.dokumen.rev", "id_did", string="Revision History")

class QmaDaftarIndukDokumenRev(models.Model):
    _name = "qma.daftar.induk.dokumen.rev"
    _description = "QMA Daftar Induk Dokumen Revision History"

    name = fields.Char(string="Revision", required=True)
    date = fields.Date(string="Date", required=True)

    id_did = fields.Many2one("qma.daftar.induk.dokumen", string="ID DID")