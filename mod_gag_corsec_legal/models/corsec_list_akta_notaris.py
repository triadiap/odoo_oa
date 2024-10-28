from odoo import api, models, fields, _

class CorsecListAktaNotaris(models.Model):
    _name = "corsec.list.akta.notaris"
    _description = "Model for Corsec List Akta Notaris"

    nomor_akta = fields.Integer(string="No. Akta", required=True)
    tanggal_akta = fields.Date(string="Tanggal", required=True)
    no_sk_sp = fields.Char(string="No. SK / SP")
    tanggal_sk_sp = fields.Date(string="Tanggal SK / SP")
    notaris = fields.Char(string="Nama Notaris", required=True)
    keterangan = fields.Text(string="Keterangan")
    scan_copy = fields.Boolean(string="Ada Scan Copy")
    asli_akta = fields.Boolean(string="Akta Asli")
    asli_sk_sp = fields.Boolean(string="SK / SP Asli")
    jenis_akta = fields.Char(string="Jenis Akta", required=True)