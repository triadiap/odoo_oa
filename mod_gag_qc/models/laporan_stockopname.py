from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError
import base64
import xlrd

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
    

    file = fields.Binary("File Stock Opname")
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
        for deletedId in self.env['gag.oa.qc.stockopname.detail'].search([('stockopname_id', '=',self.id)]):
            deletedId.unlink()
        for row_index in range(2, sheet.nrows):  # Skip the header row
            if(sheet.cell_value(row_index, 2)!=""):
                self.env['gag.oa.qc.stockopname.detail'].create({
                    'stockopname_id': self.id,
                    'pile' : sheet.cell_value(row_index, 2),
                    'toonage' : float(sheet.cell_value(row_index, 3)),
                    'ni' : float(sheet.cell_value(row_index, 4)),
                    'co': float(sheet.cell_value(row_index, 5)),
                    'fe': float(sheet.cell_value(row_index, 6)),
                    'si': float(sheet.cell_value(row_index, 7)),
                    'ca': float(sheet.cell_value(row_index, 8)),
                    'mg': float(sheet.cell_value(row_index, 9)),
                    'bc': float(sheet.cell_value(row_index, 10))
                })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }       
            
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
