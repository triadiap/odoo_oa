from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import base64
import xlrd
import xlwt
from io import BytesIO
import xlutils.copy as copy


class  PelaporanSPIP(models.Model):
    _name = "gag.oa.hse.daftar.spip"
    _description = "DAFTAR SARANA, PRASARANA, INSTALASI DAN PERALATAN"

    name = fields.Char("Nama Laporan")    
    department = fields.Char("Nama Department / Bagian",required=True)
    area = fields.Char("Lokasi Area",required=True)
    tanggal = fields.Date("Tanggal Pembuatan",required=True)
    spip_detail = fields.One2many("gag.oa.hse.daftar.spip.detail","daftar_spip","Detail Alat")
    file_name = fields.Char("Template File Name")
    file = fields.Binary("Template File")
    file_final_name = fields.Char("Lampiran File Name")
    file_final = fields.Binary("Lampiran File")

    def generate_file(self):
        font_name = "name Century Gothic, height 220"
        for rec in self:
            filename= rec.name+'.xls'
            for data in self.env['gag.oa.hse.pelaporan.template'].search([('tipe','=','SPIP')]):
                file_content = base64.b64decode(data.file)
                # Open the workbook
                workbook_open = xlrd.open_workbook(file_contents=file_content,formatting_info=True)
                worksheet_open  = workbook_open.sheet_by_index(0)
                workbook = copy.copy(workbook_open)
                worksheet= workbook.get_sheet(0)

                Style1 = worksheet_open.cell_xf_index(9,8)

                xlwt.add_palette_colour("custom_orange", 0x21)
                workbook.set_colour_RGB(0x21, 255, 153, 0)

                worksheet.write(9,8,': '+rec.department,xlwt.easyxf('font: '+font_name+';borders : top medium;pattern: pattern solid, fore_colour custom_orange;align:vert centre'))
                worksheet.write(10,8,': '+rec.area,xlwt.easyxf('font: '+font_name+'; borders : top thin;pattern: pattern solid, fore_colour custom_orange;align:vert centre'))
                worksheet.write(9,14,'Tanggal Pembuatan : '+fields.Date.from_string(rec.tanggal).strftime('%d %B %Y'),xlwt.easyxf('font: '+font_name+';pattern: pattern solid, fore_colour custom_orange; border: top medium;align:vert centre'))

                worksheet.write_merge(13,13,4,11, rec.create_uid.name,xlwt.easyxf('font: '+font_name+'; borders:bottom thin;align: horiz centre'))
                idx = 19

                subIdx = 0
                for detail in rec.spip_detail.search([('type','=','Sarana'),('daftar_spip','=',rec.id)]):
                    if(subIdx == 0):
                        worksheet.write(idx,2, 'A',xlwt.easyxf('font: '+font_name+';borders: bottom thin, left medium;align : horiz centre'))
                        worksheet.write(idx,4, 'Sarana',xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                        subIdx+=1
                        idx+=1
                    worksheet.write(idx,2, 'A.'+str(subIdx),xlwt.easyxf('font: '+font_name+';borders: bottom thin, left medium;align : horiz centre'))
                    worksheet.write(idx,4, detail.deskripsi,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                    worksheet.write(idx,12, detail.nomor,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                    if(detail.kondisi == "Baik"):
                        worksheet.write_merge(idx,idx,16,18, "X",xlwt.easyxf('font: '+font_name+';borders: bottom thin, left thin;align : horiz centre'))
                    else:
                        worksheet.write_merge(idx,idx,19,21, "X",xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin;align : horiz centre'))
                    if(detail.keterangan != False):
                        worksheet.write_merge(idx,idx,22,25, detail.keterangan,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin,right thin'))
                    subIdx+=1
                    idx+=1

                subIdx = 0
                for detail in rec.spip_detail.search([('type','=','Prasarana'),('daftar_spip','=',rec.id)]):
                    if(subIdx == 0):
                        idx+=1
                        worksheet.write(idx,2, 'B',xlwt.easyxf('font: '+font_name+';borders: bottom thin, left medium;align : horiz centre'))
                        worksheet.write(idx,4, 'Prasarana',xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                        subIdx+=1
                        idx+=1
                    worksheet.write(idx,2, 'B.'+str(subIdx),xlwt.easyxf('font: '+font_name+';borders: bottom thin, left medium;align : horiz centre'))
                    worksheet.write(idx,4, detail.deskripsi,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                    worksheet.write(idx,12, detail.nomor,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                    if(detail.kondisi == "Baik"):
                        worksheet.write_merge(idx,idx,16,18, "X",xlwt.easyxf('font: '+font_name+';borders: bottom thin, left thin;align : horiz centre'))
                    else:
                        worksheet.write_merge(idx,idx,19,21, "X",xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin;align : horiz centre'))
                    if(detail.keterangan != False):
                        worksheet.write_merge(idx,idx,22,25, detail.keterangan,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin,right thin'))
                    subIdx+=1
                    idx+=1

                subIdx = 0
                for detail in rec.spip_detail.search([('type','=','Instalasi'),('daftar_spip','=',rec.id)]):
                    if(subIdx == 0):
                        idx+=1
                        worksheet.write(idx,2, 'C',xlwt.easyxf('font: '+font_name+';borders: bottom thin, left medium;align : horiz centre'))
                        worksheet.write(idx,4, 'Instalasi',xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                        subIdx+=1
                        idx+=1
                    worksheet.write(idx,2, 'C.'+str(subIdx),xlwt.easyxf('font: '+font_name+';borders: bottom thin, left medium;align : horiz centre'))
                    worksheet.write(idx,4, detail.deskripsi,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                    worksheet.write(idx,12, detail.nomor,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                    if(detail.kondisi == "Baik"):
                        worksheet.write_merge(idx,idx,16,18, "X",xlwt.easyxf('font: '+font_name+';borders: bottom thin, left thin;align : horiz centre'))
                    else:
                        worksheet.write_merge(idx,idx,19,21, "X",xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin;align : horiz centre'))
                    if(detail.keterangan != False):
                        worksheet.write_merge(idx,idx,22,25, detail.keterangan,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin,right thin'))
                    subIdx+=1
                    idx+=1

                subIdx = 0
                for detail in rec.spip_detail.search([('type','=','Peralatan'),('daftar_spip','=',rec.id)]):
                    if(subIdx == 0):
                        idx+=1
                        worksheet.write(idx,2, 'D',xlwt.easyxf('font: '+font_name+';borders: bottom thin, left medium;align : horiz centre'))
                        worksheet.write(idx,4, 'Peralatan',xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                        subIdx+=1
                        idx+=1
                    worksheet.write(idx,2, 'D.'+str(subIdx),xlwt.easyxf('font: '+font_name+';borders: bottom thin, left medium;align : horiz centre'))
                    worksheet.write(idx,4, detail.deskripsi,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                    worksheet.write(idx,12, detail.nomor,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                    if(detail.kondisi == "Baik"):
                        worksheet.write_merge(idx,idx,16,18, "X",xlwt.easyxf('font: '+font_name+';borders: bottom thin, left thin;align : horiz centre'))
                    else:
                        worksheet.write_merge(idx,idx,19,21, "X",xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin;align : horiz centre'))
                    if(detail.keterangan != False):
                        worksheet.write_merge(idx,idx,22,25, detail.keterangan,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin,right thin'))
                    subIdx+=1
                    idx+=1
                    
                fp = BytesIO()
                workbook.save(fp)
                rec.file = base64.encodestring(fp.getvalue())
                rec.file_name = filename
                fp.close()            
    
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
    nama_agent = fields.Char("Nama Yang Menginput",required=True)
    tanggal = fields.Date("Tanggal",required=True)
    alat_detail = fields.One2many("gag.oa.hse.pelaporan.alat.detail","pelaporan","Detail Alat")
    file_name = fields.Char("Template File Name")
    file = fields.Binary("Template File")
    file_final_name = fields.Char("Lampiran File Name")
    file_final = fields.Binary("Lampiran File")

    def generate_file(self):
        font_name = "name Century Gothic, height 220"
        for rec in self:
            filename= rec.name+'.xls'
            for data in self.env['gag.oa.hse.pelaporan.template'].search([('tipe','=','ALAT')]):
                file_content = base64.b64decode(data.file)
                # Open the workbook
                workbook_open = xlrd.open_workbook(file_contents=file_content,formatting_info=True)
                worksheet_open  = workbook_open.sheet_by_index(0)
                workbook = copy.copy(workbook_open)
                worksheet= workbook.get_sheet(0)

                Style1 = worksheet_open.cell_xf_index(9,8)

                xlwt.add_palette_colour("custom_orange", 0x21)
                workbook.set_colour_RGB(0x21, 255, 153, 0)

                worksheet.write(9,14,': '+rec.vendor.name,xlwt.easyxf('font: '+font_name+';borders : top medium;pattern: pattern solid, fore_colour custom_orange;align:vert centre'))

                worksheet.write_merge(13,13,4,11, rec.nama_agent ,xlwt.easyxf('font: '+font_name+'; borders:bottom thin;align: horiz centre'))
                idx = 20

                subIdx = 1
                for detail in rec.alat_detail.search([('pelaporan','=',rec.id)]):
                    worksheet.write(idx,2, ''+str(subIdx),xlwt.easyxf('font: '+font_name+';borders: bottom thin, left medium;align : horiz centre'))
                    worksheet.write(idx,4, detail.deskripsi,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                    worksheet.write(idx,12, detail.nomor,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin'))
                    if(detail.kondisi == "Baik"):
                        worksheet.write_merge(idx,idx,16,18, "X",xlwt.easyxf('font: '+font_name+';borders: bottom thin, left thin;align : horiz centre'))
                    else:
                        worksheet.write_merge(idx,idx,19,21, "X",xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin;align : horiz centre'))
                    if(detail.keterangan != False):
                        worksheet.write_merge(idx,idx,22,25, detail.keterangan,xlwt.easyxf('font: '+font_name+';borders: bottom thin,left thin,right thin'))
                    subIdx+=1
                    idx+=1
                    
                fp = BytesIO()
                workbook.save(fp)
                rec.file = base64.encodestring(fp.getvalue())
                rec.file_name = filename
                fp.close()            

class  PelaporanSPIPDetail(models.Model):
    _name = "gag.oa.hse.pelaporan.alat.detail"
    _description = "DAFTAR ALAT & PERALATAN"

    pelaporan = fields.Many2one("gag.oa.hse.pelaporan.alat","Pelaporan")
    deskripsi = fields.Char("Deskripsi",required =True)    
    nomor = fields.Char("Nomor Alat",required = True)    
    kondisi = fields.Selection([('Baik','Baik'),('Buruk','Buruk')],"Kondisi",required = True)
    keterangan = fields.Char("Keterangan")    
    

    

class PelaporanSPIPTemplate(models.Model):
    _name = "gag.oa.hse.pelaporan.template"
    _description = "Template SPIP"

    tipe = fields.Selection([('SPIP','SPIP'),('ALAT','ALAT')],"type",required = True)
    deskripsi = fields.Char("Deskripsi",required =True)  
    file = fields.Binary("File Template")