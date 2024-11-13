from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HSEPemeriksaanIALK3(models.Model):
    _name = "gag.oa.hse.ialk3"
    _description = "IDENTIFIKASI BAHAYA-ASPEK LINGKUNGAN, PENILAIAN DAN PENGENDALIAN RESIKO-DAMPAK LINGKUNGAN"

    name = fields.Char('Name',required=True)
    tanggal = fields.Date('Tanggal', required=True)
    satker = fields.Char("Satker",requred=True);
    pemeriksaan_line_ids = fields.One2many('gag.oa.hse.ialk3.line','id_sarana','Pemeriksaan Line', required=True)


class HSEPemeriksaanPIALK3Line(models.Model):
    _name = "gag.oa.hse.ialk3.line"
    _description = "IDENTIFIKASI BAHAYA-ASPEK LINGKUNGAN, PENILAIAN DAN PENGENDALIAN RESIKO-DAMPAK LINGKUNGAN LINE"

    id_sarana = fields.Many2one("gag.oa.hse.ialk3","Parent")
    aktifitas = fields.Char("AKTIFITAS /MATERIAL / FASILITAS",required=True)
    faktor = fields.Char("FAKTOR - BAHAYA - ASPEK LINGKUNGAN")
    resiko = fields.Char("RESIKO - DAMPAK LINGKUNGAN AKTUAL & POTENSIAL")
    kondisi = fields.Selection([
        ('r','R'),
        ('nr','NR'),
        ('e','E'),
    ],"KONDISI")
    pengendalian = fields.Char("PENGENDALIAN DAMPAK-RESIKO YANG ADA SEKARANG")
    keparahan = fields.Char("KEPARAHAN")
    kemungkinan = fields.Char("KEMUNGKINAN")
    keseringan = fields.Char("KESERINGAN")
    tingkat = fields.Char("TINGKAT RESIKO DAMPAK")
    peraturan = fields.Char("PERATURAN PERUNDANGAN TERKAIT")
    status_signifikasi = fields.Selection([
        ('p','P'),
        ('TP','TP')
    ],"STATUS SIGNIFIKAN (P/TP)")
    rencana_pengendalian = fields.Char("RENCANA PENGENDALIAN DAMPAK-RESIKO TAMBAHAN")
    pertimbangan_a = fields.Boolean("A")
    pertimbangan_b = fields.Boolean("B")
    pertimbangan_c = fields.Boolean("C")
    pertimbangan_d = fields.Boolean("D")
    keterangan = fields.Char("KETERANGAN")
    custom_css = fields.Html(string='CSS', sanitize=False, default=lambda self: '<style> .o_form_label{ width:300px; }</style>', store=False)
