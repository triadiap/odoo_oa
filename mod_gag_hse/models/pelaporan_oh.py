from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
class  PelaporanOH(models.Model):
    _name = "gag.oa.hse.pelaporan.kesehatan"
    _description = "Pelaporan jumlah kesehatan per bulan"

    name = fields.Char("Nama Laporan")    
    vendor = fields.Many2one("res.partner","Nama Kontraktor",required=True)
    month = fields.Selection([
        ('1', 'Januari'),
        ('2', 'Februari'),
        ('3', 'Maret'),
        ('4', 'April'),
        ('5', 'Mei'),
        ('6', 'Juni'),
        ('7', 'Juli'),
        ('8', 'Agustus'),
        ('9', 'September'),
        ('10', 'Oktober'),
        ('11', 'November'),
        ('12', 'Desember'),
        ],string = "Bulan",required = True)
    year = fields.Char("Tahun",required = True)

    pelaporan_sakit = fields.One2many("gag.oa.hse.pelaporan.kesehatan.sakit","pelaporan_id","Jumlah pekerja yang sakit karena penyakit  bukan karena kecelakaan")
    pelaporan_absen = fields.One2many("gag.oa.hse.pelaporan.kesehatan.absen","pelaporan_id","Jumlah absensi karena sakit, tidak termasuk kecelakaan (jumlah hari hilang karena sakit)")
    pelaporan_spell = fields.One2many("gag.oa.hse.pelaporan.kesehatan.spell","pelaporan_id","Jumlah Spell")
    pelaporan_sakit_kerja = fields.One2many("gag.oa.hse.pelaporan.kesehatan.sakitkerja","pelaporan_id","Jumlah kasus Penyakit Akibat Kerja")
    pelaporan_penyakit = fields.One2many("gag.oa.hse.pelaporan.kesehatan.penyakit","pelaporan_id","10 penyakit tertinggi")


    total_sakit = fields.Integer("Jumlah Pekerja Sakit",compute="_calculate_total")
    total_absen = fields.Integer("Jumlah Absen Sakit",compute="_calculate_total")
    total_sakitkerja = fields.Integer("Total Kasus PAK",compute="_calculate_total")
    total_spell = fields.Integer("Total Spell",compute="_calculate_total")

    def _calculate_total(self):
        for rec in self:
            tmpTotal1 = 0
            tmpTotal2 = 0
            tmpTotal3 = 0
            tmpTotal4 = 0
            for detail in self.env['gag.oa.hse.pelaporan.kesehatan.sakit'].search([('pelaporan_id', '=',rec.id)]):
                tmpTotal1 += detail.jumlah
            rec.total_sakit = tmpTotal1
            for detail in self.env['gag.oa.hse.pelaporan.kesehatan.absen'].search([('pelaporan_id', '=',rec.id)]):
                tmpTotal2 += detail.jumlah
            rec.total_absen = tmpTotal2
            for detail in self.env['gag.oa.hse.pelaporan.kesehatan.sakitkerja'].search([('pelaporan_id', '=',rec.id)]):
                tmpTotal3 += detail.jumlah
            rec.total_sakitkerja = tmpTotal3
            for detail in self.env['gag.oa.hse.pelaporan.kesehatan.spell'].search([('pelaporan_id', '=',rec.id)]):
                tmpTotal4 += detail.jumlah
            rec.total_spell = tmpTotal4



class PelaporanOHSakit(models.Model):
    _name = "gag.oa.hse.pelaporan.kesehatan.sakit"
    _description = "Pelaporan jumlah kesehatan per bulan (Sakit)"



    vendor = fields.Char("Nama Vendor",related = "pelaporan_id.vendor.name")
    month = fields.Selection([
        ('1', 'Januari'),
        ('2', 'Februari'),
        ('3', 'Maret'),
        ('4', 'April'),
        ('5', 'Mei'),
        ('6', 'Juni'),
        ('7', 'Juli'),
        ('8', 'Agustus'),
        ('9', 'September'),
        ('10', 'Oktober'),
        ('11', 'November'),
        ('12', 'Desember'),
        ],"Bulan",related = "pelaporan_id.month")
    year = fields.Char("Tahun",related = "pelaporan_id.year")
    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.kesehatan","Pelaporan")
    satuan_kerja = fields.Char("Satuan Kerja",required = True)
    jumlah = fields.Integer("Jumlah",required = True)

    
class PelaporanOHAbsen(models.Model):
    _name = "gag.oa.hse.pelaporan.kesehatan.absen"
    _description = "Pelaporan jumlah kesehatan per bulan (Absen)"



    vendor = fields.Char("Nama Vendor",related = "pelaporan_id.vendor.name")
    month = fields.Selection([
        ('1', 'Januari'),
        ('2', 'Februari'),
        ('3', 'Maret'),
        ('4', 'April'),
        ('5', 'Mei'),
        ('6', 'Juni'),
        ('7', 'Juli'),
        ('8', 'Agustus'),
        ('9', 'September'),
        ('10', 'Oktober'),
        ('11', 'November'),
        ('12', 'Desember'),
        ],"Bulan",related = "pelaporan_id.month")
    year = fields.Char("Tahun",related = "pelaporan_id.year")
    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.kesehatan","Pelaporan")
    satuan_kerja = fields.Char("Satuan Kerja",required = True)
    jumlah = fields.Integer("Jumlah",required = True)
    
class PelaporanOHSakitSpell(models.Model):
    _name = "gag.oa.hse.pelaporan.kesehatan.spell"
    _description = "Pelaporan jumlah kesehatan per bulan (Spell)"



    vendor = fields.Char("Nama Vendor",related = "pelaporan_id.vendor.name")
    month = fields.Selection([
        ('1', 'Januari'),
        ('2', 'Februari'),
        ('3', 'Maret'),
        ('4', 'April'),
        ('5', 'Mei'),
        ('6', 'Juni'),
        ('7', 'Juli'),
        ('8', 'Agustus'),
        ('9', 'September'),
        ('10', 'Oktober'),
        ('11', 'November'),
        ('12', 'Desember'),
        ],"Bulan",related = "pelaporan_id.month")
    year = fields.Char("Tahun",related = "pelaporan_id.year")
    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.kesehatan","Pelaporan")
    satuan_kerja = fields.Char("Satuan Kerja",required = True)
    jumlah = fields.Integer("Jumlah",required = True)
    
class PelaporanOHSakitKerja(models.Model):
    _name = "gag.oa.hse.pelaporan.kesehatan.sakitkerja"
    _description = "Pelaporan jumlah kesehatan per bulan (Sakit Kerja)"



    vendor = fields.Char("Nama Vendor",related = "pelaporan_id.vendor.name")
    month = fields.Selection([
        ('1', 'Januari'),
        ('2', 'Februari'),
        ('3', 'Maret'),
        ('4', 'April'),
        ('5', 'Mei'),
        ('6', 'Juni'),
        ('7', 'Juli'),
        ('8', 'Agustus'),
        ('9', 'September'),
        ('10', 'Oktober'),
        ('11', 'November'),
        ('12', 'Desember'),
        ],"Bulan",related = "pelaporan_id.month")
    year = fields.Char("Tahun",related = "pelaporan_id.year")
    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.kesehatan","Pelaporan")
    satuan_kerja = fields.Char("Satuan Kerja",required = True)
    jumlah = fields.Integer("Jumlah",required = True)

class PelaporanOHPenyakit(models.Model):
    _name = "gag.oa.hse.pelaporan.kesehatan.penyakit"
    _description = "Pelaporan jumlah kesehatan per bulan (Sakit Kerja)"

    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.kesehatan","Pelaporan")
    nama = fields.Char("Nama Penyakit",required = True)
    lokasi_kerja = fields.Char("Lokasi Kerja",required = True)
    rawat_jalan = fields.Boolean("Rawat Jalan")
    rawat_inap = fields.Boolean("Rawat Inap")
    lama = fields.Integer("Lama Pengobatan")
    currency_id = fields.Many2one('res.currency', string='Currency')
    biaya = fields.Monetary("Biaya",currency_field='currency_id', required=True,)