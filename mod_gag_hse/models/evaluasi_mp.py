from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HSEEvaluasimp(models.Model):
    _name = "gag.oa.hse.evaluasimp"
    _description = "HSE Evaluasi MP"

    nama_vendor = fields.Char('Nama Vendor', required=True)
    nomor = fields.Char('Nomor', required=True)
    kontrak_mulai = fields.Date('Mulai Kontrak', required=True)
    kontrak_selesai = fields.Date('Selesai Kontrak', required=True)
    bulan = fields.One2many("gag.oa.hse.evaluasimp.bulan","evalusi_id","Bulan")

class HSEEvaluasimpBulan(models.Model):
    _name = "gag.oa.hse.evaluasimp.bulan"
    _description = "HSE Evaluasi MP Bulan"

    evalusi_id = fields.Many2one("gag.oa.hse.evaluasimp","Evaluasi")
    bulan = fields.Char('Bulan', required=True)
    detail = fields.One2many("gag.oa.hse.evaluasimp.detail","evaluasi_bulan_id","Detail")

    def generate_data(self):
        #self.bulan = "Test"
        for data in self.env["gag.oa.hse.parameter"].search([('parameter','!=','')]):
            self.detail.create({'parameter_id':data.id,'evaluasi_bulan_id':self.id})

class HSEEvaluasiDetail(models.Model):
    _name = "gag.oa.hse.evaluasimp.detail"
    _description = "HSE Evaluasi MP Detail"

    evaluasi_bulan_id = fields.Many2one("gag.oa.hse.evaluasimp.bulan","Evaluasi Bulan")
    parameter_id = fields.Many2one("gag.oa.hse.parameter","Parameter")
    keterangan = fields.Char("Keterangan")