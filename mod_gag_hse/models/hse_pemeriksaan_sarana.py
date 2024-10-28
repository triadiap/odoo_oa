from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HSEPemeriksaanSarana(models.Model):
    _name = "gag.oa.hse.pemeriksaan.sarana"
    _description = "FORM PEMERIKSAAN KELAYAKAN SARANA"

    name = fields.Char('Name',required=True)
    tanggal = fields.Date('Tanggal', required=True)
    jenis = fields.Char('Jenis Sarana / Unit', required=True)
    no_lambung = fields.Char('No Lambung / Unit', required=True)
    km_hm = fields.Char('KM / HM', required=True)
    no_pol = fields.Char('NO Polisi / HM', required=True)
    nama_kontraktor = fields.Char('Nama Kontraktor', required=True)
    pemeriksaan_line_ids = fields.One2many('gag.oa.hse.pemeriksaan.sarana.line','id_sarana','Pemeriksaan Line', required=True)
    hasil = fields.Selection([('1','Layak Untuk Digunakan'),('2','Layak Digunakan Dengan Catatan'),('3','Tidak Layak Untuk Digunakan')],'Hasil',required=True)
    catatan = fields.Text('Catatan')

    
    def generate_data(self):
        #self.bulan = "Test"
        for data in self.env["gag.oa.hse.parameter.sarana"].search([('pemeriksaan','!=','')]):
            self.pemeriksaan_line_ids.create({'parameter_id':data.id,'id_sarana':self.id})


class HSEPemeriksaanSaranaLine(models.Model):
    _name = "gag.oa.hse.pemeriksaan.sarana.line"
    _description = "FORM PEMERIKSAAN KELAYAKAN SARANA LINE"

    id_sarana = fields.Many2one("gag.oa.hse.pemeriksaan.sarana","Parent")
    parameter_id = fields.Many2one("gag.oa.hse.parameter.sarana","Pemeriksaan")
    pemeriksaan_no = fields.Char("No",related="parameter_id.no")
    kategori = fields.Char("Kategori",compute='_get_kategori',store = True)
    hasil = fields.Boolean("Hasil")

    @api.depends('parameter_id')
    def _get_kategori(self):
        for rec in self:
            rec.kategori = dict(rec.parameter_id._fields['kategori'].selection).get(rec.parameter_id.kategori)