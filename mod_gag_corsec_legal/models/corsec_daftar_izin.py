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