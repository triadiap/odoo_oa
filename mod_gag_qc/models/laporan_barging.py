from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class BargingReport(models.Model):
    _name = "gag.oa.qc.barging"
    _description = "Data Barging"

    commence_load = fields.Date('Commence Load', required=True)
    complete_load = fields.Date('Complete Load')
    tonnage = fields.Integer('Tonnage')
    contractor_id = fields.Many2one('res.partner', tracking=True,
        check_company=True,
        string='Partner', change_default=True, ondelete='restrict')
    contractor = fields.Char('Contractor',related='contractor_id.display_name')
    buyer = fields.Char("Buyer & Tujuan")
    status = fields.Selection([
        ('loading', 'Loading'),
        ('sod', 'SOD'),
        ('complete', 'Complete')
    ], default="loading", string="Status", tracking=True)
    id_barging = fields.One2many('gag.oa.qc.barging.detail', 'barging_id', 'List Tongkang')

    test_css = fields.Html(string='CSS', sanitize=False, compute='_compute_css', store=False)

    def name_get(self):
        result = []
        for record in self:
            name = f"({record.contractor}) - {record.commence_load}"
            result.append((record.id, name))  # or any other meaningful field
        return result

    @api.depends('status')
    def _compute_css(self):
        for record in self:
            # You can modify the below below condition
            if record.status == 'complete':
                record.test_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                record.test_css = False

class ListTongkang(models.Model):
    _name = "gag.oa.qc.barging.detail"
    _description = "Data Tongkang"

    no =fields.Integer('Number')
    tongkang =fields.Char('Tongkang / LCT')
    tanggal =fields.Date('Tanggal')
    barging_id = fields.Many2one('gag.oa.qc.barging', 'Parent')
    plant = fields.Float("Plant (wmt)",digits=(0,2))
    loaded = fields.Float("Loaded (wmt)",digits=(0,2))
    cummulative = fields.Float("Cumm. (wmt)", compute="_calculate_progress",digits=(0,2))
    balance = fields.Float("Balance (wmt)",compute="_calculate_progress",digits=(0,2))
    progress = fields.Float("Progress",compute="_calculate_progress",digits=(0,2))
    contractor = fields.Char("Kontraktor",related='barging_id.contractor')

    def _calculate_progress(self):
        for rec in self:
            rec.cummulative = rec.loaded
            rec.balance = rec.plant - rec.cummulative
            if rec.plant > 0:
                rec.progress = (rec.loaded/rec.plant)*100
            else:
                rec.progress = 0
    
    @api.model
    def create(self, vals):        
        rec = super(ListTongkang, self).create(vals)
        for detail in self.env['gag.oa.qc.daily.production'].search([('tanggal', '=',vals['tanggal'])]):
            self.env['gag.oa.qc.daily.production.barging'].create({'production_id':detail.id,'tongkang_id':rec.id})
        return rec

    def write(self, vals):
        rec = super(ListTongkang, self).write(vals)
        for deletedId in self.env['gag.oa.qc.daily.production.barging'].search([('tongkang_id', '=',self.id)]):
            deletedId.unlink()
        for detail in self.env['gag.oa.qc.daily.production'].search([('tanggal', '=',self.tanggal)]):
            self.env['gag.oa.qc.daily.production.barging'].create({'production_id':detail.id,'tongkang_id':self.id})
        return rec
