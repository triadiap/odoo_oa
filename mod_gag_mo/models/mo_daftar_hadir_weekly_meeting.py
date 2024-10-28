from odoo import api, models, fields, _

class MoDaftarHadirWeeklyMeeting(models.Model):
    _name = "mo.absensi.weekly.meeting"
    _description = "Model for absensi weekly meeting"

    tema = fields.Char(string="Tema Rapat", required=True)
    tanggal = fields.Date(string="Tanggal", required=True)
    jumlah_peserta = fields.Integer(string="Jumlah Peserta")
    bukti = fields.Binary(string="Bukti Daftar Hadir", required=True)