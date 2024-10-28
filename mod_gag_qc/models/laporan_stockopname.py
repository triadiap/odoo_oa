from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class StockOpname(models.Model):
    _name = "gag.oa.qc.stockopname"
    _description = "Stock Opname"

    name = fields.Char("name",compute="_compute_name")
    year = fields.Selection(selection='_get_years', string='Year', default=lambda self: str(datetime.now().year), tracking=True)
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
    ], string="Month", required=True, default='1', tracking=True)
    id_stockopname = fields.One2many('gag.oa.qc.stockopname.detail', 'stockopname_id', 'Stock Detail')

    @api.depends('month','year')
    def _compute_name(self):
        for record in self:
            record.name = f"{dict(record._fields['month'].selection).get(record.month)} {record.year}"
    def name_get(self):
        result = []
        for record in self:
            name = f"{dict(record._fields['month'].selection).get(record.month)} {record.year}"
            result.append((record.id, name))  # or any other meaningful field
        return result
    
    def _get_years(self):
        current_year = datetime.now().year-2
        year_range = 10  # Number of years to generate
        years = [(str(year), str(year)) for year in range(current_year, current_year + year_range)]
        return years
class StockopnameDetail(models.Model):    
    _name = "gag.oa.qc.stockopname.detail"
    _description = "Stock Opname Detail"

    stockopname_id = fields.Many2one('gag.oa.qc.stockopname', 'Parent')
    pile = fields.Char('Pile',required = True)
    toonage = fields.Float('Tonnage')
    ni = fields.Float('Ni',digit=(0,2))
    co = fields.Float('Co',digit=(0,2))
    fe = fields.Float('Fe',digit=(0,2))
    si = fields.Float('Si',digit=(0,2))
    ca = fields.Float('Ca',digit=(0,2))
    mg = fields.Float('Mg',digit=(0,2))
    bc = fields.Float('Bc',digit=(0,2))
