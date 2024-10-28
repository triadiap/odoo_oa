from odoo import api, models, fields, _

class MoInspeksiHarian(models.Model):
    _name = "mo.inspeksi.harian"
    _description = "Model for MO Inspeksi Harian module"

    inspektor = fields.Many2one("res.users", string="Nama Inspektor", required=True)
    tanggal = fields.Date(string="Tanggal Inspeksi", required=True)
    shift = fields.Selection([
        ("shift_1", "Shift 1"),
        ("shift_2", "Shift 2"),
    ], string="Shift", required=True)
    lokasi = fields.Selection([
        ("kantor", "Kantor / Mess GAG"),
        ("lapangan", "Lapangan"),
    ], string="Lokasi Site", required=True)

    s_lokasi = fields.Char(string="Lokasi")
    s_jam = fields.Char(string="Jam")
    s_keterangan = fields.Char(string="Nama")
    s_temuan = fields.Char(string="Temuan")

    p_lokasi = fields.Char(string="Lokasi")
    p_jam_mulai = fields.Float(string="Jam Mulai")
    p_jam_selesai = fields.Float(string="Jam Selesai")
    p_area = fields.Char(string="Area")
    p_keterangan = fields.Text(string="Keterangan")

    r_lokasi = fields.Char(string="Lokasi")
    r_jenis_rambu = fields.Char(string="Jenis Rambu")
    r_progres = fields.Selection([
        ("baru", "Pemasangan Baru"),
        ("perbaikan", "Perawatan / Perbaikan")
    ], string="Progres")
    r_keterangan = fields.Text(string="Keterangan")

    i_kategori = fields.Char(string="Kategori")
    i_lokasi = fields.Char(string="Lokasi Kejadian")
    i_korban_alat = fields.Char(string="Korban / Alat")
    i_kronologi = fields.Text(string="Kronologi")
    i_rekomendasi = fields.Text(string="Rekomendasi")

    area_list = fields.One2many("mo.inspeksi.harian.area", "id_inspeksi", string="Area Inspeksi")


class MoInspeksiHarianArea(models.Model):
    _name = "mo.inspeksi.harian.area"
    _description = "Model for MO Inspeksi Harian Area module"

    name = fields.Char(string="Nama Lokasi", required=True)
    jam_mulai = fields.Float(string="Jam Mulai", required=True)
    jam_selesai = fields.Float(string="Jam Selesai", required=True)

    id_inspeksi = fields.Many2one("mo.inspeksi.harian", string="ID Inspeksi")