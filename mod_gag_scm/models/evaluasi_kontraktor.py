from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import base64
import xlrd
class  SCMevaluasiKontraktor(models.Model):
    _name = "gag.oa.scm.evaluasi.kontraktor"
    _description = "EVALUASI KINERJA KONTRAKTOR"

    name = fields.Char("Nama Laporan")    
    vendor = fields.Many2one("res.partner","Nama Kontraktor",required=True)    
    nomor_kontrak = fields.Many2one('purchase.contract',string="Nomor Kontrak", required=True)
    mulai_kontrak = fields.Date(string="Mulai Kontrak", required=True,related="nomor_kontrak.comancement_date")
    selesai_kontrak = fields.Date(string="Selesai Kontrak",required=True,related="nomor_kontrak.completion_date")  
    perode_evaluasi = fields.Char("Periode Evaluasi")
    tanggal_evaluasi = fields.Date("Tanggal Evaluasi")
    catatan = fields.Char("Catatan Evaluasi")

    
    hasil_keselamatan = fields.One2many("gag.oa.scm.evaluasi.kontraktor.keselamatan","evaluasi","Keselamatan")
    hasil_lingkup = fields.One2many("gag.oa.scm.evaluasi.kontraktor.lingkup","evaluasi","Lingkup Kerja")
    hasil_pelaksanaan = fields.One2many("gag.oa.scm.evaluasi.kontraktor.pelaksanaan","evaluasi","Pelaksanaan")
    hasil_qualifikasi = fields.One2many("gag.oa.scm.evaluasi.kontraktor.qualifikasi","evaluasi","Qualifikasi")
    hasil_koordinasi = fields.One2many("gag.oa.scm.evaluasi.kontraktor.koordinasi","evaluasi","Koordinasi")
    hasil_hak = fields.One2many("gag.oa.scm.evaluasi.kontraktor.hak","evaluasi","Hak & Kewajiban")
    hasil_hasil = fields.One2many("gag.oa.scm.evaluasi.kontraktor.hasil","evaluasi","hasil Pekerjaan")

    rate_keselamatan =fields.Float("Keselamaatan",compute="_calculate_rate_keselamatan")
    rate_lingkup =fields.Float("Lingkup Kerja",compute="_calculate_rate_lingkup")
    rate_pelaksanaan =fields.Float("Pelaksaan",compute="_calculate_rate_pelaksanaan")
    rate_qualifikasi =fields.Float("Kualifikasi",compute="_calculate_rate_qualifikasi")
    rate_koordinasi =fields.Float("Koordinasi",compute="_calculate_rate_koordinasi")
    rate_hak =fields.Float("Hak dan Kewajiban",compute="_calculate_rate_hak")
    rate_hasil =fields.Float("Hasil Pekerjaan",compute="_calculate_rate_hasil")

    def _calculate_rate_keselamatan(self):        
        for rec in self:
            rec.rate_keselamatan = 0
            total1 = 0
            total2 = 0
            for detail in rec.env["gag.oa.scm.evaluasi.kontraktor.keselamatan"].search([('evaluasi','=',rec.id)]):
                total1 +=1
                total2 += float(detail.rate)
            if(total1!=0):
                rec.rate_keselamatan = total2/total1

    def _calculate_rate_lingkup(self):        
        for rec in self:
            rec.rate_lingkup = 0
            total1 = 0
            total2 = 0
            for detail in rec.env["gag.oa.scm.evaluasi.kontraktor.lingkup"].search([('evaluasi','=',rec.id)]):
                total1 +=1
                total2 += float(detail.rate)
            if(total1!=0):
                rec.rate_lingkup = total2/total1

    def _calculate_rate_pelaksanaan(self):        
        for rec in self:
            rec.rate_pelaksanaan = 0
            total1 = 0
            total2 = 0
            for detail in rec.env["gag.oa.scm.evaluasi.kontraktor.pelaksanaan"].search([('evaluasi','=',rec.id)]):
                total1 +=1
                total2 += float(detail.rate)
            if(total1!=0):
                rec.rate_pelaksanaan = total2/total1

    def _calculate_rate_qualifikasi(self):        
        for rec in self:
            rec.rate_qualifikasi = 0
            total1 = 0
            total2 = 0
            for detail in rec.env["gag.oa.scm.evaluasi.kontraktor.qualifikasi"].search([('evaluasi','=',rec.id)]):
                total1 +=1
                total2 += float(detail.rate)
            if(total1!=0):
                rec.rate_qualifikasi = total2/total1

    def _calculate_rate_koordinasi(self):        
        for rec in self:
            rec.rate_koordinasi = 0
            total1 = 0
            total2 = 0
            for detail in rec.env["gag.oa.scm.evaluasi.kontraktor.koordinasi"].search([('evaluasi','=',rec.id)]):
                total1 +=1
                total2 += float(detail.rate)
            if(total1!=0):
                rec.rate_koordinasi = total2/total1

    def _calculate_rate_hak(self):        
        for rec in self:
            rec.rate_hak = 0
            total1 = 0
            total2 = 0
            for detail in rec.env["gag.oa.scm.evaluasi.kontraktor.hak"].search([('evaluasi','=',rec.id)]):
                total1 +=1
                total2 += float(detail.rate)
            if(total1!=0):
                rec.rate_hak = total2/total1

    def _calculate_rate_hasil(self):        
        for rec in self:
            rec.rate_hasil = 0
            total1 = 0
            total2 = 0
            for detail in rec.env["gag.oa.scm.evaluasi.kontraktor.hasil"].search([('evaluasi','=',rec.id)]):
                total1 +=1
                total2 += float(detail.rate)
            if(total1!=0):
                rec.rate_hasil = total2/total1


class SCMevaluasiKontraktorKeselamatan(models.Model):
    _name = "gag.oa.scm.evaluasi.kontraktor.keselamatan"
    _description = "EVALUASI KINERJA KONTRAKTOR (Keselamatan)"

    evaluasi = fields.Many2one("gag.oa.scm.evaluasi.kontraktor")
    kriteria = fields.Char("Kriteria",required = True)
    uraian = fields.Char("Uraian",required = True)
    rate = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],required = True)

    
class SCMevaluasiKontraktorLingkup(models.Model):
    _name = "gag.oa.scm.evaluasi.kontraktor.lingkup"
    _description = "EVALUASI KINERJA KONTRAKTOR (Lingkup Kerja)"

    evaluasi = fields.Many2one("gag.oa.scm.evaluasi.kontraktor")
    kriteria = fields.Char("Kriteria",required = True)
    uraian = fields.Char("Uraian",required = True)
    rate = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],required = True)
    
class SCMevaluasiKontraktorPelaksanaan(models.Model):
    _name = "gag.oa.scm.evaluasi.kontraktor.pelaksanaan"
    _description = "EVALUASI KINERJA KONTRAKTOR (Pelaksanaan)"

    evaluasi = fields.Many2one("gag.oa.scm.evaluasi.kontraktor")
    kriteria = fields.Char("Kriteria",required = True)
    uraian = fields.Char("Uraian",required = True)
    rate = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],required = True)
    
class SCMevaluasiKontraktorQualifikasi(models.Model):
    _name = "gag.oa.scm.evaluasi.kontraktor.qualifikasi"
    _description = "EVALUASI KINERJA KONTRAKTOR (Qualifikasi)"

    evaluasi = fields.Many2one("gag.oa.scm.evaluasi.kontraktor")
    kriteria = fields.Char("Kriteria",required = True)
    uraian = fields.Char("Uraian",required = True)
    rate = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],required = True)
    
class SCMevaluasiKontraktorKoordinasi(models.Model):
    _name = "gag.oa.scm.evaluasi.kontraktor.koordinasi"
    _description = "EVALUASI KINERJA KONTRAKTOR (Koordinasi)"

    evaluasi = fields.Many2one("gag.oa.scm.evaluasi.kontraktor")
    kriteria = fields.Char("Kriteria",required = True)
    uraian = fields.Char("Uraian",required = True)
    rate = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],required = True)
    
    
class SCMevaluasiKontraktorHak(models.Model):
    _name = "gag.oa.scm.evaluasi.kontraktor.hak"
    _description = "EVALUASI KINERJA KONTRAKTOR (Hak dan Kewajiban)"

    evaluasi = fields.Many2one("gag.oa.scm.evaluasi.kontraktor")
    kriteria = fields.Char("Kriteria",required = True)
    uraian = fields.Char("Uraian",required = True)
    rate = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],required = True)
    
    
class SCMevaluasiKontraktorhasil(models.Model):
    _name = "gag.oa.scm.evaluasi.kontraktor.hasil"
    _description = "EVALUASI KINERJA KONTRAKTOR (Hasil)"

    evaluasi = fields.Many2one("gag.oa.scm.evaluasi.kontraktor")
    kriteria = fields.Char("Kriteria",required = True)
    uraian = fields.Char("Uraian",required = True)
    rate = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],required = True)