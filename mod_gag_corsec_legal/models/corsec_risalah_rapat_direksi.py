from odoo import api, models, fields, _

class CorsecRisalahRapatDireksi(models.Model):
    _name = "corsec.risalah.rapat.direksi"
    _description = "Model for CORSEC Risalah Rapat Direksi"

    tanggal = fields.Date(string="Tanggal", required=True)
    jam_mulai = fields.Float(string="Jam Mulai", required=True)
    jam_selesai = fields.Float(string="Jam Selesai", required=True)
    tempat = fields.Char(string="Tempat", required=True)
    agenda = fields.Text(string="Agenda Rapat", required=True)
    file = fields.Binary(string="Soft Copy Dokumen Risalah Rapat Direksi", required=True)