from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
class  PelaporanSPIP(models.Model):
    _name = "gag.oa.hse.daftar.spip"
    _description = "DAFTAR SARANA, PRASARANA, INSTALASI DAN PERALATAN"

    name = fields.Char("Nama Laporan")    
    department = fields.Char("Nama Department / Bagian",required=True)
    area = fields.Char("Lokasi Area",required=True)
    tanggal = fields.Date("Tanggal Pembuatan",required=True)
    spip_detail = fields.One2many("gag.oa.hse.daftar.spip.detail","daftar_spip","Detail Alat")
    file = fields.Binary("Lampiran File")
    
class  PelaporanSPIPDetail(models.Model):
    _name = "gag.oa.hse.daftar.spip.detail"
    _description = "DAFTAR SARANA, PRASARANA, INSTALASI DAN PERALATAN DETAIL"

    type = fields.Selection([
        ('Sarana','Sarana'),
        ('Prasarana','Prasarana'),
        ('Instalasi','Instalasi'),
        ('Peralatan','Peralatan')
        ],"Tipe")
    daftar_spip = fields.Many2one("gag.oa.hse.daftar.spip","Daftar SPIP")
    deskripsi = fields.Char("Deskripsi",required =True)    
    nomor = fields.Char("Nomor Alat",required = True)    
    kondisi = fields.Selection([('Baik','Baik'),('Buruk','Buruk')],"Kondisi",required = True)
    keterangan = fields.Char("Keterangan")    
    
class  PelaporanAlatKerja(models.Model):
    _name = "gag.oa.hse.pelaporan.alat"
    _description = "DAFTAR ALAT & PERALATAN"

    name = fields.Char("Nama Laporan")    
    vendor = fields.Many2one("res.partner","Nama Perusahaan",required=True)
    nama_agent = fields.Char("Nama Agen Kontraktor",required=True)
    tanggal = fields.Date("Tanggal",required=True)
    file = fields.Binary("Lampiran File")
    alat_detail = fields.One2many("gag.oa.hse.pelaporan.alat.detail","pelaporan","Detail Alat")

class  PelaporanSPIPDetail(models.Model):
    _name = "gag.oa.hse.pelaporan.alat.detail"
    _description = "DAFTAR ALAT & PERALATAN"

    pelaporan = fields.Many2one("gag.oa.hse.pelaporan.alat","Pelaporan")
    deskripsi = fields.Char("Deskripsi",required =True)    
    nomor = fields.Char("Nomor Alat",required = True)    
    kondisi = fields.Selection([('Baik','Baik'),('Buruk','Buruk')],"Kondisi",required = True)
    keterangan = fields.Char("Keterangan")    
    