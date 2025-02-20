from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import base64
import xlrd
class  PelaporanHSE(models.Model):
    _name = "gag.oa.hse.pelaporan.pekerja"
    _description = "Pelaporan jumlah pekerja per bulan"

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

    pelaporan_jamkerja = fields.One2many("gag.oa.hse.pelaporan.pekerja.jamkerja","pelaporan_id","jam Kerja")
    pelaporan_tenagakerja = fields.One2many("gag.oa.hse.pelaporan.pekerja.tenagakerja","pelaporan_id","tenaga Kerja")
    pelaporan_kopetensi = fields.One2many("gag.oa.hse.pelaporan.pekerja.kopetensi","pelaporan_id","kopetensi")
    pelaporan_alat = fields.One2many("gag.oa.hse.pelaporan.pekerja.alat","pelaporan_id","alat")
    pelaporan_bbm = fields.One2many("gag.oa.hse.pelaporan.pekerja.bbm","pelaporan_id","bbm")
    pelaporan_limbah_bbm = fields.One2many("gag.oa.hse.pelaporan.pekerja.limbah.bbm","pelaporan_id","Limbah BBM")
    pelaporan_limbah_b3 = fields.One2many("gag.oa.hse.pelaporan.pekerja.limbah.b3","pelaporan_id","Limbah B3")
    pelaporan_limbah_nonb3 = fields.One2many("gag.oa.hse.pelaporan.pekerja.limbah.nonb3","pelaporan_id","Limbah NON B3")

    total_pekerja = fields.Integer("Total Pekerja",compute="_calculate_total")
    total_jamkerja = fields.Integer("Total Jam Kerja",compute="_calculate_total")

    file = fields.Binary("File BBM")
    file_name = fields.Char(string="File Name", required=True)

    @api.onchange('file')
    def _onchange_file(self):
        """Automatically set the file name when a file is selected."""
        if self.file and self.file_name:
            # File name is automatically set during file upload
            self.file_name = self.file_name
        elif self.file:
            self.file_name = 'uploaded_file.xlsx'  # Default name if none is provided
        else:
            self.file_name = ''

    def _calculate_total(self):
        for rec in self:
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.hse.pelaporan.pekerja.jamkerja'].search([('pelaporan_id', '=',rec.id)]):
                tmpTotal1 += detail.jumlah
                tmpTotal2 += detail.jamkerja
            rec.total_pekerja = tmpTotal1
            rec.total_jamkerja = tmpTotal2

     

    def process_excel_file(self):
        if not self.file:
            raise UserError(_("Please upload an Excel file."))
        if not self.file_name:
            raise UserError(_("File name is missing."))


        # Decode the file
        file_content = base64.b64decode(self.file)

        # Open the workbook
        workbook = xlrd.open_workbook(file_contents=file_content)
        sheet = workbook.sheet_by_index(0)  # Assuming the first sheet

        # Iterate through rows and process data
        totalBBM = 0
        for deletedId in self.env['gag.oa.hse.pelaporan.pekerja.limbah.bbm'].search([('pelaporan_id', '=',self.id)]):
            deletedId.unlink()
        for row_index in range(5, sheet.nrows):  # Skip the header row
            if(sheet.cell_value(row_index, 8)!=""):
                totalBBM += float(sheet.cell_value(row_index, 8))  # Example: Column 1
                self.env['gag.oa.hse.pelaporan.pekerja.limbah.bbm'].create({
                    'pelaporan_id': self.id,
                    'sumber' : sheet.cell_value(row_index, 3),
                    'unit' : sheet.cell_value(row_index, 4),
                    'type': sheet.cell_value(row_index, 5),
                    'process': sheet.cell_value(row_index, 6),
                    'jenis_bbm': sheet.cell_value(row_index, 7),
                    'jumlah_pemakaian': float(sheet.cell_value(row_index, 8)),
                    'keterangan': sheet.cell_value(row_index, 9)
                })

                
        sheet = workbook.sheet_by_index(1)  # Assuming the first sheet
        for deletedId in self.env['gag.oa.hse.pelaporan.pekerja.limbah.b3'].search([('pelaporan_id', '=',self.id)]):
            deletedId.unlink()
        # Iterate through rows and process data
        for row_index in range(5, sheet.nrows):  # Skip the header row
            if(sheet.cell_value(row_index, 8)!=""):
                self.env['gag.oa.hse.pelaporan.pekerja.limbah.b3'].create({
                    'pelaporan_id': self.id,
                    'jenis' : sheet.cell_value(row_index, 3),
                    'sumber' : sheet.cell_value(row_index, 4),
                    'process': sheet.cell_value(row_index, 5),
                    'satuan': sheet.cell_value(row_index, 6),
                    'jumlah_pemakaian': sheet.cell_value(row_index, 7),
                    'jumlah_limbah': float(sheet.cell_value(row_index, 8)),
                    'jumlah_diserahkan': float(sheet.cell_value(row_index, 9)),
                    'keterangan': sheet.cell_value(row_index, 10)
                })
                
        for deletedId in self.env['gag.oa.hse.pelaporan.pekerja.limbah.nonb3'].search([('pelaporan_id', '=',self.id)]):
            deletedId.unlink()
        sheet = workbook.sheet_by_index(2)  # Assuming the first sheet
        # Iterate through rows and process data
        for row_index in range(5, sheet.nrows):  # Skip the header row
            if(sheet.cell_value(row_index, 8)!=""):
                self.env['gag.oa.hse.pelaporan.pekerja.limbah.nonb3'].create({
                    'pelaporan_id': self.id,
                    'jenis' : sheet.cell_value(row_index, 3),
                    'process': sheet.cell_value(row_index, 4),
                    'satuan': sheet.cell_value(row_index, 5),
                    'jumlah_pemakaian': sheet.cell_value(row_index, 6),
                    'jumlah_limbah': float(sheet.cell_value(row_index, 7)),
                    'jumlah_dimanfaatkan': float(sheet.cell_value(row_index, 8)),
                    'keterangan': sheet.cell_value(row_index, 9)
                })

        #self.env['gag.oa.hse.pelaporan.pekerja.bbm'].create({
        #    'pelaporan_id': self.id,
        #    'jumlah_bulan_lalu' : 0,
        #    'jumlah_penerimaan' : 0,
        #    'jenis_bbm': 'SOLAR',
        #    'jumlah_pemakaian': totalBBM
        #})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }       


class PelaporanHSEJamKerja(models.Model):
    _name = "gag.oa.hse.pelaporan.pekerja.jamkerja"
    _description = "Pelaporan jumlah pekerja per bulan (Jam Kerja)"

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
    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.pekerja","Pelaporan")
    keterangan = fields.Selection([
        ('Operasional', 'Operasional'),
        ('Administrasi', 'Administrasi'),
        ('Pengawas', 'Pengawas'),
        ],String = "Keterangan",required = True)
    jumlah = fields.Integer("Jumlah",required = True)
    jamkerja = fields.Integer("Jam Kerja",required = True)


class PelaporanHSETenagaKerja(models.Model):
    _name = "gag.oa.hse.pelaporan.pekerja.tenagakerja"
    _description = "Pelaporan jumlah pekerja per bulan (Tenaga Kerja)"

    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.pekerja","Pelaporan")
    keterangan = fields.Char("Keterangan",required = True)
    jumlah = fields.Integer("Jumlah",required = True)
    
class PelaporanHSETKopetensi(models.Model):
    _name = "gag.oa.hse.pelaporan.pekerja.kopetensi"
    _description = "Pelaporan jumlah pekerja per bulan (Kopetensi)"

    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.pekerja","Pelaporan")
    keterangan = fields.Char("Keterangan",required = True)
    jumlah = fields.Integer("Jumlah",required = True)

class PelaporanHSETAlat(models.Model):
    _name = "gag.oa.hse.pelaporan.pekerja.alat"
    _description = "Pelaporan jumlah pekerja per bulan (Alat)"

    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.pekerja","Pelaporan")
    keterangan = fields.Char("Keterangan",required = True)
    jumlah = fields.Integer("Jumlah",required = True)
    
class PelaporanHSETBBM(models.Model):
    _name = "gag.oa.hse.pelaporan.pekerja.bbm"
    _description = "Pelaporan jumlah pekerja per bulan (Bahan Bakar Cair)"

    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.pekerja","Pelaporan")
    jenis_bbm = fields.Selection([
        ('SOLAR', 'SOLAR'),
        ('PREMIUM', 'PREMIUM'),
        ('MINYAK PELUMAS', 'MINYAK PELUMAS'),
        ],String = "Jenis BBM",required = True)
    jumlah_bulan_lalu = fields.Integer("Sisa bulan lalu",required = True)
    jumlah_penerimaan = fields.Integer("Jumlah penerimaan",required = True)
    jumlah = fields.Integer("Jumlah",required = True,compute = "_calculate_jumlah")
    jumlah_pemakaian = fields.Integer("Pemakaian",required = True)
    jumlah_sisa_bulan_ini = fields.Integer("Sisa bulan ini",required = True,compute = "_calculate_sisa")


    @api.depends('jumlah_bulan_lalu','jumlah_penerimaan')
    def _calculate_jumlah(self):
        for rec in self:
            rec.jumlah = rec.jumlah_bulan_lalu + rec.jumlah_penerimaan

    @api.depends('jumlah','jumlah_pemakaian')
    def _calculate_sisa(self):
        for rec in self:
            rec.jumlah_sisa_bulan_ini = rec.jumlah - rec.jumlah_pemakaian

class PelaporanHSELimbahBBM(models.Model):
    _name = "gag.oa.hse.pelaporan.pekerja.limbah.bbm"
    _description = "Pelaporan limbah (Penggunaan BBM)"

    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.pekerja","Pelaporan")
    vendor = fields.Char("Nama Vendor",related = "pelaporan_id.vendor.name",store=True)
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
        ],"Bulan",related = "pelaporan_id.month",store=True)
    year = fields.Char("Tahun",related = "pelaporan_id.year",store=True)
    sumber = fields.Char('Sumber Emisi',required = True)
    unit = fields.Char('Deskripsi Unit',required = True)
    type = fields.Char('Tipe Unit',required = True)
    process = fields.Char('Unit Process',required = True)
    jenis_bbm = fields.Char('Jenis Bahan Bakar',required = True)
    jumlah_pemakaian = fields.Integer("Jumlah Pemakaian",required = True)
    keterangan = fields.Char('Keterangan')

class PelaporanHSELimbahB3(models.Model):
    _name = "gag.oa.hse.pelaporan.pekerja.limbah.b3"
    _description = "Pelaporan limbah (NERACA LIMBAH B3)"

    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.pekerja","Pelaporan")
    vendor = fields.Char("Nama Vendor",related = "pelaporan_id.vendor.name",store=True)
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
        ],"Bulan",related = "pelaporan_id.month",store=True)
    year = fields.Char("Tahun",related = "pelaporan_id.year",store=True)
    jenis = fields.Char('Jenis Limbah',required = True)
    sumber = fields.Char('Sumber Unit',required = True)
    process = fields.Char('Unit Process',required = True)
    satuan = fields.Char('Satuan',required = True)
    jumlah_pemakaian = fields.Integer("Jumlah Pemakaian",required = True)
    jumlah_limbah = fields.Integer("Jumlah limbah yang dihasilkan ",required = True)
    jumlah_diserahkan = fields.Integer("Jumlah yang diserahkan",required = True)
    keterangan = fields.Char('Keterangan')


class PelaporanHSELimbahNonB3(models.Model):
    _name = "gag.oa.hse.pelaporan.pekerja.limbah.nonb3"
    _description = "Pelaporan limbah (NERACA LIMBAH NON B3)"

    pelaporan_id = fields.Many2one("gag.oa.hse.pelaporan.pekerja","Pelaporan")
    vendor = fields.Char("Nama Vendor",related = "pelaporan_id.vendor.name",store=True)
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
        ],"Bulan",related = "pelaporan_id.month",store=True)
    year = fields.Char("Tahun",related = "pelaporan_id.year",store=True)
    jenis = fields.Char('Jenis Limbah',required = True)
    process = fields.Char('Unit Process',required = True)
    satuan = fields.Char('Satuan',required = True)
    jumlah_pemakaian = fields.Integer("Jumlah Pemakaian",required = True)
    jumlah_limbah = fields.Integer("Jumlah limbah yang dihasilkan ",required = True)
    jumlah_dimanfaatkan = fields.Integer("Jumlah yang dimanfaatkan",required = True)
    keterangan = fields.Char('Keterangan')
