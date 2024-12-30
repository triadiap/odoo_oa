from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class BargingReport(models.Model):
    _name = "gag.oa.qc.barging"
    _description = "Data Barging"

    commence_load = fields.Date('Commence Load', required=True)
    complete_load = fields.Date('Complete Load')
    tonnage = fields.Integer('Tonnage')
    contractor = fields.Selection([('SMA','SMA'),('MKA','MKA')],String = "Contactor")
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
    barging_plan =fields.Many2one('gag.oa.qc.barging.plan','Plan',domain="[('tanggal','=',commence_load)]")
    tongkang =fields.Char('Tongkang / LCT',related="barging_plan.tongkang")
    tanggal =fields.Date('Tanggal')
    commence_load = fields.Date('Tanggal Loading',related = "barging_id.commence_load")
    barging_id = fields.Many2one('gag.oa.qc.barging', 'Parent')
    plant = fields.Float("Plant (wmt)",digits=(0,2),related="barging_plan.tonnage")
    loaded = fields.Float("Loaded (wmt)",digits=(0,2))
    cummulative = fields.Float("Cumm. (wmt)", compute="_calculate_progress",digits=(0,2))
    balance = fields.Float("Balance (wmt)",compute="_calculate_progress",digits=(0,2))
    progress = fields.Float("Progress",compute="_calculate_progress",digits=(0,2))
    contractor = fields.Selection([('SMA','SMA'),('MKA','MKA')],String = "Contactor",related='barging_id.contractor')

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
        for detail in self.env['gag.oa.qc.daily.production'].search([('tanggal', '=',vals['commence_load'])]):
            self.env['gag.oa.qc.daily.production.barging'].create({'production_id':detail.id,'tongkang_id':rec.id})
            if(rec.contractor == "SMA"):
                self.env['gag.oa.qc.daily.production.barging.sma'].create({'production_id':detail.id,'tongkang_id':rec.id})
            if(rec.contractor == "MKA"):
                self.env['gag.oa.qc.daily.production.barging.mka'].create({'production_id':detail.id,'tongkang_id':rec.id})
        return rec

    def write(self, vals):
        rec = super(ListTongkang, self).write(vals)
        for deletedId in self.env['gag.oa.qc.daily.production.barging'].search([('tongkang_id', '=',self.id)]):
            deletedId.unlink()
        for deletedId in self.env['gag.oa.qc.daily.production.barging.sma'].search([('tongkang_id', '=',self.id)]):
            deletedId.unlink()
        for deletedId in self.env['gag.oa.qc.daily.production.barging.mka'].search([('tongkang_id', '=',self.id)]):
            deletedId.unlink()

        for detail in self.env['gag.oa.qc.daily.production'].search([('tanggal', '=',self.commence_load)]):
            self.env['gag.oa.qc.daily.production.barging'].create({'production_id':detail.id,'tongkang_id':self.id})

        if(self.contractor == "SMA"):
            for detail in self.env['gag.oa.qc.daily.production'].search([('tanggal', '=',self.commence_load)]):
                self.env['gag.oa.qc.daily.production.barging.sma'].create({'production_id':detail.id,'tongkang_id':self.id})
        if(self.contractor == "MKA"):
            for detail in self.env['gag.oa.qc.daily.production'].search([('tanggal', '=',self.commence_load)]):
                self.env['gag.oa.qc.daily.production.barging.mka'].create({'production_id':detail.id,'tongkang_id':self.id})
        return rec

class BargingPlan(models.Model):
    _name = "gag.oa.qc.barging.plan"
    _description = "Rencana pengapalan harian"

    site = fields.Char("Site",required = True)    
    partner = fields.Selection([('SMA','SMA'),('MKA','MKA')],String = "Contactor",required = True)
    tanggal = fields.Date("Tanggal",required = True)
    tongkang = fields.Char("Tongkang / LCT",required = True)
    target_ni = fields.Float("Target Ni",digit=(0,2),required = True)
    target = fields.Float("Target Tonnage",digit=(0,4))
    barging_plan_detail_id = fields.One2many("gag.oa.qc.barging.plan.detail","barging_plan","Detail")

    
    ni = fields.Float("Total Ni",digit=(0,2),compute="_calculate_target")
    tonnage = fields.Float("Total Tonnage",digit=(0,2),compute="_calculate_target")
    sisa_ni = fields.Float("Kurang Ni",digit=(0,2),compute="_calculate_target")
    sisa_tonnage = fields.Float("Kurang Tonnage",digit=(0,4),compute="_calculate_target")

    def name_get(self):
        result = []
        for record in self:
            name = f"({record.partner}) - {record.tanggal}"
            result.append((record.id, name))  # or any other meaningful field
        return result

    def _calculate_target(self):
        for rec in self:
            rec.tonnage = float(sum(self.env['gag.oa.qc.barging.plan.detail'].search([('barging_plan', '=',rec.id)]).mapped('toonage')))            
            rec.sisa_tonnage = rec.target-rec.tonnage
            tmpTotal1 = 0
            tmpTotal2 = 0
            rec.ni  =0
            rec.sisa_ni = 0
            for detail in self.env['gag.oa.qc.barging.plan.detail'].search([('barging_plan', '=',rec.id)]):
                tmpTotal1 += detail.ni*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2!=0):
                rec.ni= tmpTotal1/tmpTotal2
                rec.sisa_ni = ((rec.target_ni* rec.target) - (rec.ni*rec.tonnage))/rec.sisa_tonnage

class BargingPlanDetail(models.Model):
    _name = "gag.oa.qc.barging.plan.detail"
    _description = "Detail rencana pengapalan harian"

    barging_plan = fields.Many2one("gag.oa.qc.barging.plan","Barging Plan")
    stokpile_id = fields.Many2one("gag.oa.qc.daily.production.detail","UMT")
    toonage = fields.Float('Tonnage',digit=(0,4),related="stokpile_id.toonage")
    ni = fields.Float('Ni',digit=(0,2), related="stokpile_id.ni")
    co = fields.Float('Co',digit=(0,2), related="stokpile_id.co")
    fe = fields.Float('Fe',digit=(0,2), related="stokpile_id.fe")
    si = fields.Float('Si',digit=(0,2), related="stokpile_id.si")
    ca = fields.Float('Ca',digit=(0,2), related="stokpile_id.ca")
    mg = fields.Float('Mg',digit=(0,2), related="stokpile_id.mg")
    bc = fields.Float('Bc',digit=(0,2), related="stokpile_id.bc")

    @api.model
    def create(self, vals):        
        rec = super(BargingPlanDetail, self).create(vals)
        rec.stokpile_id.tanggal_barging = rec.barging_plan.tanggal
        return rec

    def write(self, vals):
        rec = super(BargingPlanDetail, self).write(vals)
        rec.stokpile_id.tanggal_barging = rec.barging_plan.tanggal
        return rec
