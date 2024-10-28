from odoo import api, models, fields, _

class CorsecDaftarBodBoc(models.Model):
    _name = "corsec.daftar.bod.boc"
    _description = "Model for Daftar BOD BOC in Corsec & Legal Module"

    name = fields.Char(string="Nama", required=True)
    jabatan = fields.Char(string="Jabatan", required=True)
    jangka_waktu = fields.Char(string="Jangka Waktu", required=True)
    no_akta = fields.Char(string="No. Akta", required=True)
    tanggal_akta = fields.Date(string="Tanggal Akta", required=True)
    waktu_pengangkatan = fields.Date(string="Waktu Pengangkatan", required=True)
    berakhir = fields.Char(string="Berakhir Pada", required=True)
    keterangan = fields.Text(string="Keterangan")