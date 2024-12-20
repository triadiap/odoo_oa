from odoo import api, models, fields, _

class MoMinutesMeeting(models.Model):
    _name = "mo.minutes.meeting"
    _description = "Model for MO Minutes Meeting module"

    tanggal_waktu = fields.Datetime(string="Tanggal & Jam Meeting", required=True)
    tempat = fields.Char(string="Tempat / Venue", required=True)
    mom_writer = fields.Many2one("res.users", string="Ditulis oleh", default=lambda self:self.env.user.id)
    topik_rapat = fields.Char(string="Topik Rapat", required=True)
    peserta = fields.Char(string="Peserta", required=True)
    distribusi = fields.Char(string="Distribusi")
    sc_peserta = fields.Binary(string="Soft Copy Daftar Hadir Peserta")

    detail = fields.One2many("mo.minutes.meeting.detail", "id_detail", string="Pokok-Pokok Rapat")

    def name_get(self):
        result = []
        for record in self:
            display_name = f"{record.tanggal_waktu} - {record.tempat} - {record.topik_rapat}"  # Custom display
            result.append((record.id, display_name))
        return result

class MoMinutesMeetingDetail(models.Model):
    _name = "mo.minutes.meeting.detail"
    _description = "Model for MO Minutes Meeting detail"

    pokok_rapat = fields.Char(string="Pokok-Pokok Rapat", required=True)
    action_plan = fields.Char(string="Action Plan")

    id_detail = fields.Many2one("mo.minutes.meeting", string="ID Meeting")