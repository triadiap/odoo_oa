from odoo import api, fields, models, _

class MoSafetyTalk(models.Model):
    _name = "mo.safety.talk"
    _description = "Model for MO Safety Talk module"

    waktu_tanggal = fields.Datetime(string="Waktu / Tanggal", required=True)
    divisi = fields.Char(string="Divisi", required=True)
    tema = fields.Text(string="Tema")
    items = fields.One2many("mo.safety.talk.item", "id_items", string="Jumlah Pekerja")

class MoSafetyTalk(models.Model):
    _name = "mo.safety.talk.item"
    _description = "Model for MO Safety Talk Item"

    name = fields.Char(string="Nama", required=True)
    tidur = fields.Selection([
        ("ya", "Ya"),
        ("tidak", "Tidak"),
    ], string="Tidur lebih dari 5 Jam ?", required=True)
    obat = fields.Selection([
        ("ya", "Ya"),
        ("tidak", "Tidak"),
    ], string="Tidak mengkonsumsi obat ?", required=True)
    sehat = fields.Selection([
        ("ya", "Ya"),
        ("tidak", "Tidak"),
    ], string="Merasa sehat dan siap bekerja ?", required=True)
    masalah = fields.Selection([
        ("ya", "Ya"),
        ("tidak", "Tidak"),
    ], string="Tidak sedang dalam masalah (pribadi / pekerjaan) ?", required=True)

    id_items = fields.Many2one("mo.safety.talk", string="ID")