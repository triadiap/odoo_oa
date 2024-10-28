from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HSEPemeriksaanPeralatan(models.Model):
    _name = "gag.oa.hse.pemeriksaan.peralatan"
    _description = "PEMERIKSAAN PERALATAN SARANA LV"

    name = fields.Char('Name',required=True)
    tanggal = fields.Date('Tanggal', required=True)
    shift = fields.Selection([('1','Shift 1'),('2','Shift 2')],'Shift',required=True)
    no_lambung = fields.Char('No Lambung / Unit', required=True)
    km_hm = fields.Char('KM', required=True)
    pemeriksaan_line_ids = fields.One2many('gag.oa.hse.pemeriksaan.peralatan.line','id_sarana','Pemeriksaan Line', required=True)
    kerusakan_lain = fields.Text('Kerusakan Lain')

    
    def generate_data(self):
        #self.bulan = "Test"
        for data in self.env["gag.oa.hse.parameter.peralatan"].search([('pemeriksaan','!=','')]):
            self.pemeriksaan_line_ids.create({'parameter_id':data.id,'id_sarana':self.id})


class HSEPemeriksaanPeralatanLine(models.Model):
    _name = "gag.oa.hse.pemeriksaan.peralatan.line"
    _description = "PEMERIKSAAN PERALATAN SARANA LV LINE"

    id_sarana = fields.Many2one("gag.oa.hse.pemeriksaan.peralatan","Parent")
    parameter_id = fields.Many2one("gag.oa.hse.parameter.peralatan","Pemeriksaan")
    pemeriksaan_no = fields.Char("No",related="parameter_id.no")
    kode = fields.Char("Kode",compute='_get_kode',store = True)
    hasil = fields.Boolean("Hasil")
    keterangan = fields.Char("Keterangan")

    @api.depends('parameter_id')
    def _get_kode(self):
        for rec in self:
            rec.kode = dict(rec.parameter_id._fields['kode'].selection).get(rec.parameter_id.kode)