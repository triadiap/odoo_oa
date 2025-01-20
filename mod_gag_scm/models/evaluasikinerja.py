from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import base64
import xlrd
class  SCMevaluasiKinerja(models.Model):
    _name = "gag.oa.scm.evaluasi.kinerja"
    _description = "EVALUASI KINERJA MITRA VENDOR MANAGEMENT"

    name = fields.Char("Nama Laporan")    
    vendor = fields.Many2one("res.partner","Nama Kontraktor",required=True)    
    periode_start = fields.Date("Periode Awal",required=True)    
    periode_end = fields.Date("Periode Akhir",required=True)    

    data_motivasi = fields.One2many('gag.oa.scm.evaluasi.kinerja.motivasi','evaluasi_id','Motivasi dan Keinginan menjadi Mitra Kerja')
    data_harga = fields.One2many('gag.oa.scm.evaluasi.kinerja.harga','evaluasi_id','Harga')
    data_pengiriman = fields.One2many('gag.oa.scm.evaluasi.kinerja.pengiriman','evaluasi_id','Kinerja Pengiriman')
    data_kualitas = fields.One2many('gag.oa.scm.evaluasi.kinerja.kualitas','evaluasi_id','Kualitas Pekerjaan')
    data_sanksi = fields.One2many('gag.oa.scm.evaluasi.kinerja.sanksi','evaluasi_id','Sanksi dan Teguran')

    nilai_pengadaan = fields.Float('KINERJA PENGADAAN (Bobot 25%)',compute='_calculate_nilai')
    nilai_pengerjaan = fields.Float('KINERJA PENYELESAIAN PO / KONTRAK (Bobot 75%)',compute='_calculate_nilai')
    nilai_sanksi = fields.Float('Sanksi dan Teguran (Bersifat Pengurang)',compute='_calculate_nilai')
    nilai_akhir = fields.Float('Total Score',compute='_calculate_nilai')

    def _calculate_nilai(self):
        for rec in self:
            rec.nilai_pengadaan = 0
            rec.nilai_pengerjaan = 0
            rec.nilai_sanksi = 0
            rec.nilai_akhir = 0

            totalValue = 0
            totalData = 0
            for data in self.env["gag.oa.scm.evaluasi.kinerja.motivasi"].search([('evaluasi_id','=',rec.id)]):
                totalValue+=float(data.nilai)
                totalData+=1
            for data in self.env["gag.oa.scm.evaluasi.kinerja.harga"].search([('evaluasi_id','=',rec.id)]):
                totalValue+=float(data.nilai)
                totalData+=1
            if(totalData > 0):
                rec.nilai_pengadaan = totalValue/totalData

            totalValue = 0
            totalData = 0
            for data in self.env["gag.oa.scm.evaluasi.kinerja.pengiriman"].search([('evaluasi_id','=',rec.id)]):
                totalValue+=float(data.nilai)
                totalData+=1
            for data in self.env["gag.oa.scm.evaluasi.kinerja.kualitas"].search([('evaluasi_id','=',rec.id)]):
                totalValue+=float(data.nilai)
                totalData+=1
            if(totalData > 0):
                rec.nilai_pengerjaan = totalValue/totalData

            totalValue = 0
            totalData = 0
            for data in self.env["gag.oa.scm.evaluasi.kinerja.sanksi"].search([('evaluasi_id','=',rec.id)]):
                totalValue+=float(data.nilai)
                totalData+=1
            if(totalData > 0):
                rec.nilai_sanksi = totalValue/totalData

            rec.nilai_akhir = (rec.nilai_pengadaan*0.25)+(rec.nilai_pengerjaan*0.75)-rec.nilai_sanksi

class SCMEvaluasiKinerjaMotivasi(models.Model):
    _name = "gag.oa.scm.evaluasi.kinerja.motivasi"
    _description = "EVALUASI KINERJA MITRA VENDOR MANAGEMENT (Motivasi)"

    evaluasi_id = fields.Many2one('gag.oa.scm.evaluasi.kinerja','Evaluasi')
    kriteria = fields.Char('Kriteria Kinerja')
    status = fields.Selection([
        ('ya','Ya'),
        ('tidak','Tidak'),
        ],'Status')
    frekuensi = fields.Integer('Frequency')
    nilai = fields.Integer('Score')
    flag = fields.Char('Flag')
    keterangan = fields.Char('Keterangan Pendukung')


class SCMEvaluasiKinerjaHarga(models.Model):
    _name = "gag.oa.scm.evaluasi.kinerja.harga"
    _description = "EVALUASI KINERJA MITRA VENDOR MANAGEMENT (Harga)"

    evaluasi_id = fields.Many2one('gag.oa.scm.evaluasi.kinerja','Evaluasi')
    kriteria = fields.Char('Kriteria Kinerja')
    status = fields.Selection([
        ('ya','Ya'),
        ('tidak','Tidak'),
        ],'Status')
    frekuensi = fields.Integer('Frequency')
    nilai = fields.Integer('Score')
    flag = fields.Char('Flag')
    keterangan = fields.Char('Keterangan Pendukung')


class SCMEvaluasiKinerjaPengiriman(models.Model):
    _name = "gag.oa.scm.evaluasi.kinerja.pengiriman"
    _description = "EVALUASI KINERJA MITRA VENDOR MANAGEMENT (Pengiriman)"

    evaluasi_id = fields.Many2one('gag.oa.scm.evaluasi.kinerja','Evaluasi')
    kriteria = fields.Char('Kriteria Kinerja')
    status = fields.Selection([
        ('ya','Ya'),
        ('tidak','Tidak'),
        ],'Status')
    frekuensi = fields.Integer('Frequency')
    nilai = fields.Integer('Score')
    flag = fields.Char('Flag')
    keterangan = fields.Char('Keterangan Pendukung')


class SCMEvaluasiKinerjaKualitas(models.Model):
    _name = "gag.oa.scm.evaluasi.kinerja.kualitas"
    _description = "EVALUASI KINERJA MITRA VENDOR MANAGEMENT (Kualitas)"

    evaluasi_id = fields.Many2one('gag.oa.scm.evaluasi.kinerja','Evaluasi')
    kriteria = fields.Char('Kriteria Kinerja')
    status = fields.Selection([
        ('ya','Ya'),
        ('tidak','Tidak'),
        ],'Status')
    frekuensi = fields.Integer('Frequency')
    nilai = fields.Integer('Score')
    flag = fields.Char('Flag')
    keterangan = fields.Char('Keterangan Pendukung')

class SCMEvaluasiKinerjaSanksi(models.Model):
    _name = "gag.oa.scm.evaluasi.kinerja.sanksi"
    _description = "EVALUASI KINERJA MITRA VENDOR MANAGEMENT (Sanksi)"

    evaluasi_id = fields.Many2one('gag.oa.scm.evaluasi.kinerja','Evaluasi')
    kriteria = fields.Char('Jenis Sanksi / Surat Peringatan')
    status = fields.Selection([
        ('ya','Ya'),
        ('tidak','Tidak'),
        ],'Status')
    frekuensi = fields.Integer('Frequency')
    nilai_value = fields.Char('Score Pengurang')
    nilai = fields.Integer('Total Score')
    keterangan = fields.Char('Keterangan Pendukung')

