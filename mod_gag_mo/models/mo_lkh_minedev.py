from odoo import api, models, fields, _

class MoLkhMinedev(models.Model):
    _name = "mo.minedev.lkh"
    _description = "LKH Mining Development"

    tanggal = fields.Date(string="Tanggal", required=True)
    shift = fields.Selection([
        ("1", "Shift 1"),
        ("2", "Shift 2"),
    ], string="Shift", default="1", required=True)
    catatan_pengamatan = fields.Text(string="Catatan")
    info_kegiatan = fields.Text(string="Informasi Kegiatan Harian")
    lkh_items = fields.One2many("mo.minedev.lkhitem", "id_lkh", string="Obyek Dipantau")
    unit_items = fields.One2many("mo.minedev.alatberat", "id_lkh", string="Informasi Alat Berat")

class MoLkhMinedevItems(models.Model):
    _name = "mo.minedev.lkhitem"
    _description = "LKH Mining Development Items"

    obyek_pengamatan = fields.Selection([
        ("IMKASU", "IMKASU"),
        ("5000", "5000"),
        ("FM", "FM"),
        ("AM", "AM"),
        ("EFO", "EFO"),
        ("STA 600", "STA 600"),
        ("DUBAI BARAT", "DUBAI BARAT"),
    ], string="Objek Pengamatan", required=True)
    kondisi_tanggul = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
    ], string="Kondisi Tanggul", required=True)
    saluran_air = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
    ], string="Saluran Air", required=True)
    isi_kolam = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
    ], string="Isi Kolam", required=True)
    id_lkh = fields.Many2one("mo.minedev.lkh", string="LKH Reference")

class MoLkhMinedevAlatBerat(models.Model):
    _name = "mo.minedev.alatberat"
    _description = "LKH Mining Development Items"

    alat_berat = fields.Selection([
        ("Excavator", "Excavator"),
        ("Alat Angkut", "Alat Angkut"),
        ("Dozer", "Dozer"),
        ("Vibro", "Vibro"),
        ("Motor Grader", "Motor Grader"),
    ], string="Alat Berat", required=True)

    unit_1 = fields.Char(string="Unit 1")
    unit_2 = fields.Char(string="Unit 2")
    unit_3 = fields.Char(string="Unit 3")
    unit_4 = fields.Char(string="Unit 4")
    unit_5 = fields.Char(string="Unit 5")
    unit_6 = fields.Char(string="Unit 6")
    mitra = fields.Char(string="Mitra")

    id_lkh = fields.Many2one("mo.minedev.lkh", string="LKH Reference")