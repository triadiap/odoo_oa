from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HSEParameter(models.Model):
    _name = "gag.oa.hse.parameter"
    _description = "Parameter Sesuai Ruang Lingkup"

    parameter = fields.Char('Parameter', required=True)

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.parameter}"
            result.append((record.id, name))  # or any other meaningful field
        return result

class HSEPemeriksaanSarana(models.Model):
    _name = "gag.oa.hse.parameter.sarana"
    _description = "Parameter Checklist Sarana"

    kategori = fields.Selection([
        ('A', 'Sarana & Unit'),
        ('B', 'Sarana'),
        ('C', 'Unit'),
    ], string="Kategori", required=True, default='A', tracking=True)
    no = fields.Char('Nomer', required=True)
    pemeriksaan = fields.Char('Pemeriksaan', required=True)

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.pemeriksaan}"
            result.append((record.id, name))  # or any other meaningful field
        return result   
     
class HSEPemeriksaanPeralatan(models.Model):
    _name = "gag.oa.hse.parameter.peralatan"
    _description = "Parameter Checklist Peralatan"

    no = fields.Char('Nomer', required=True)
    pemeriksaan = fields.Char('Pemeriksaan', required=True)
    kode = fields.Selection([
        ('1', 'X'),
        ('2', 'XX'),
        ('3', 'XXX'),
    ], string="Kategori", required=False, default='1', tracking=True)

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.pemeriksaan}"
            result.append((record.id, name))  # or any other meaningful field
        return result    