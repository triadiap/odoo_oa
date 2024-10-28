from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class DailyProductionReport(models.Model):
    _name = "gag.oa.qc.daily.production"
    _description = "Daily Production"

    tanggal = fields.Date('Tanggal report', required=True)
    site = fields.Char('Site', required=True)
    id_production = fields.One2many('gag.oa.qc.daily.production.detail', 'production_id', 'Production Detail')
    id_tongkang = fields.One2many('gag.oa.qc.daily.production.barging', 'production_id', 'List Tongkan')

    total_tonnage = fields.Float("Total Tonnage",compute="_total_tonnage",digit=(0,4))
    total_tonnage_li = fields.Float("Total Tonnage li",compute="_total_tonnage_li",digit=(0,4))
    total_tonnage_low = fields.Float("Total Tonnage Low",compute="_total_tonnage_low",digit=(0,4))
    total_tonnage_hi = fields.Float("Total Tonnage Hi",compute="_total_tonnage_hi",digit=(0,4))

    total_ni = fields.Float("Total Ni",compute="_total_ni",digit=(0,2))
    total_ni_li = fields.Float("Total Ni Li",compute="_total_ni_li",digit=(0,2))
    total_ni_low = fields.Float("Total Ni Low",compute="_total_ni_low",digit=(0,2))
    total_ni_hi = fields.Float("Total Ni Hi",compute="_total_ni_hi",digit=(0,2))

    total_co = fields.Float("Tonnage",compute="_total_co",digit=(0,2))
    total_co_li = fields.Float("Tonnage",compute="_total_co_li",digit=(0,2))
    total_co_low = fields.Float("Tonnage",compute="_total_co_low",digit=(0,2))
    total_co_hi = fields.Float("Tonnage",compute="_total_co_hi",digit=(0,2))

    total_fe = fields.Float("Tonnage",compute="_total_fe",digit=(0,2))
    total_fe_li = fields.Float("Tonnage",compute="_total_fe_li",digit=(0,2))
    total_fe_low = fields.Float("Tonnage",compute="_total_fe_low",digit=(0,2))
    total_fe_hi = fields.Float("Tonnage",compute="_total_fe_hi",digit=(0,2))

    total_si = fields.Float("Tonnage",compute="_total_si",digit=(0,2))
    total_si_li = fields.Float("Tonnage",compute="_total_si_li",digit=(0,2))
    total_si_low = fields.Float("Tonnage",compute="_total_si_low",digit=(0,2))
    total_si_hi = fields.Float("Tonnage",compute="_total_si_hi",digit=(0,2))

    total_ca = fields.Float("Tonnage",compute="_total_ca",digit=(0,2))
    total_ca_li = fields.Float("Tonnage",compute="_total_ca_li",digit=(0,2))
    total_ca_low = fields.Float("Tonnage",compute="_total_ca_low",digit=(0,2))
    total_ca_hi = fields.Float("Tonnage",compute="_total_ca_hi",digit=(0,2))

    total_mg = fields.Float("Tonnage",compute="_total_mg",digit=(0,2))
    total_mg_li = fields.Float("Tonnage",compute="_total_mg_li",digit=(0,2))
    total_mg_low = fields.Float("Tonnage",compute="_total_mg_low",digit=(0,2))
    total_mg_hi = fields.Float("Tonnage",compute="_total_mg_hi",digit=(0,2))

    total_bc = fields.Float("Tonnage",compute="_total_bc",digit=(0,2))
    total_bc_li = fields.Float("Tonnage",compute="_total_bc_li",digit=(0,2))
    total_bc_low = fields.Float("Tonnage",compute="_total_bc_low",digit=(0,2))
    total_bc_hi = fields.Float("Tonnage",compute="_total_bc_hi",digit=(0,2))

    # mka
    total_tonnage_li_mka = fields.Float("Tonnage",compute="_total_li_mka",digit=(0,4))
    total_tonnage_low_mka = fields.Float("Tonnage",compute="_total_low_mka",digit=(0,4))
    total_tonnage_hi_mka = fields.Float("Tonnage",compute="_total_hi_mka",digit=(0,4))
    total_tonnage_mka = fields.Float("Tonnage",compute="_total_mka",digit=(0,4))
    total_tonnage_ready_mka = fields.Float("Total Rady To Barge MKA",compute="_total_mka",digit=(0,4))
    total_tonnage_ready_final_mka = fields.Float("Total Ready To Barge MKA Final",compute="_total_mka",digit=(0,4))

    # sma
    total_tonnage_li_sma = fields.Float("Tonnage",compute="_total_li_sma",digit=(0,4))
    total_tonnage_low_sma = fields.Float("Tonnage",compute="_total_low_sma",digit=(0,4))
    total_tonnage_hi_sma = fields.Float("Tonnage",compute="_total_hi_sma",digit=(0,4))
    total_tonnage_sma = fields.Float("Tonnage",compute="_total_sma",digit=(0,4))
    total_tonnage_ready_sma = fields.Float("Total Rady To Barge SMA",compute="_total_sma",digit=(0,4))
    total_tonnage_ready_final_sma = fields.Float("Total Ready To Barge SMA Final",compute="_total_sma",digit=(0,4))

    def name_get(self):
        result = []
        for record in self:
            name = f"({record.site}) - {record.tanggal}"
            result.append((record.id, name))  # or any other meaningful field
        return result
    
    def _total_tonnage(self):        
        for rec in self:
            rec.total_tonnage = sum(line.toonage for line in rec.id_production)

    def _total_tonnage_li(self):        
        for rec in self:
            rec.total_tonnage_li = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5')]).mapped('toonage')))

    def _total_tonnage_low(self):        
        for rec in self:
            rec.total_tonnage_low = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>','1.5'),('ni','<','1.8')]).mapped('toonage')))

    def _total_tonnage_hi(self):        
        for rec in self:
            rec.total_tonnage_hi = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]).mapped('toonage')))


    def _total_ni(self):
        for rec in self:
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.ni*detail.toonage
                tmpTotal2 += detail.toonage
            rec.total_ni= tmpTotal1/tmpTotal2
    def _total_ni_li(self):
        for rec in self:
            rec.total_ni_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5')]):
                tmpTotal1 += detail.ni*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_ni_li= tmpTotal1/tmpTotal2
            
    def _total_ni_low(self):
        for rec in self:
            rec.total_ni_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.ni*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_ni_low= tmpTotal1/tmpTotal2

    def _total_ni_hi(self):
        for rec in self:
            rec.total_ni_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.ni*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_ni_hi= tmpTotal1/tmpTotal2

    def _total_co(self):
        for rec in self:
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.co*detail.toonage
                tmpTotal2 += detail.toonage
            rec.total_co= tmpTotal1/tmpTotal2
    def _total_co_li(self):
        for rec in self:
            rec.total_co_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5')]):
                tmpTotal1 += detail.co*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_co_li= tmpTotal1/tmpTotal2
            
    def _total_co_low(self):
        for rec in self:
            rec.total_co_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.co*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_co_low= tmpTotal1/tmpTotal2

    def _total_co_hi(self):
        for rec in self:
            rec.total_co_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.co*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_co_hi= tmpTotal1/tmpTotal2

    def _total_fe(self):
        for rec in self:
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.fe*detail.toonage
                tmpTotal2 += detail.toonage
            rec.total_fe= tmpTotal1/tmpTotal2
    def _total_fe_li(self):
        for rec in self:
            rec.total_fe_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5')]):
                tmpTotal1 += detail.fe*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_fe_li= tmpTotal1/tmpTotal2
            
    def _total_fe_low(self):
        for rec in self:
            rec.total_fe_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.fe*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_fe_low= tmpTotal1/tmpTotal2

    def _total_fe_hi(self):
        for rec in self:
            rec.total_fe_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.fe*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_fe_hi= tmpTotal1/tmpTotal2

    def _total_si(self):
        for rec in self:
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.si*detail.toonage
                tmpTotal2 += detail.toonage
            rec.total_si= tmpTotal1/tmpTotal2
    def _total_si_li(self):
        for rec in self:
            rec.total_si_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5')]):
                tmpTotal1 += detail.si*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_si_li= tmpTotal1/tmpTotal2
            
    def _total_si_low(self):
        for rec in self:
            rec.total_si_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.si*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_si_low= tmpTotal1/tmpTotal2

    def _total_si_hi(self):
        for rec in self:
            rec.total_si_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.si*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_si_hi= tmpTotal1/tmpTotal2

    def _total_ca(self):
        for rec in self:
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.ca*detail.toonage
                tmpTotal2 += detail.toonage
            rec.total_ca= tmpTotal1/tmpTotal2
    def _total_ca_li(self):
        for rec in self:
            rec.total_ca_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5')]):
                tmpTotal1 += detail.ca*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_ca_li= tmpTotal1/tmpTotal2
            
    def _total_ca_low(self):
        for rec in self:
            rec.total_ca_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.ca*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_ca_low= tmpTotal1/tmpTotal2

    def _total_ca_hi(self):
        for rec in self:
            rec.total_ca_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.ca*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_ca_hi= tmpTotal1/tmpTotal2

    def _total_mg(self):
        for rec in self:
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.mg*detail.toonage
                tmpTotal2 += detail.toonage
            rec.total_mg= tmpTotal1/tmpTotal2
    def _total_mg_li(self):
        for rec in self:
            rec.total_mg_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5')]):
                tmpTotal1 += detail.mg*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_mg_li= tmpTotal1/tmpTotal2
            
    def _total_mg_low(self):
        for rec in self:
            rec.total_mg_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.mg*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_mg_low= tmpTotal1/tmpTotal2

    def _total_mg_hi(self):
        for rec in self:
            rec.total_mg_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.mg*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_mg_hi= tmpTotal1/tmpTotal2

    def _total_bc(self):
        for rec in self:
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.bc*detail.toonage
                tmpTotal2 += detail.toonage
            rec.total_bc= tmpTotal1/tmpTotal2
    def _total_bc_li(self):
        for rec in self:
            rec.total_bc_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5')]):
                tmpTotal1 += detail.bc*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_bc_li= tmpTotal1/tmpTotal2
            
    def _total_bc_low(self):
        for rec in self:
            rec.total_bc_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.bc*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_bc_low= tmpTotal1/tmpTotal2

    def _total_bc_hi(self):
        for rec in self:
            rec.total_bc_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.bc*detail.toonage
                tmpTotal2 += detail.toonage
            if(tmpTotal2 != 0):
                rec.total_bc_hi= tmpTotal1/tmpTotal2
    # ini mka only

    def _total_li_mka(self):        
        for rec in self:
            rec.total_tonnage_li_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5'),('pile','like','MKA')]).mapped('toonage')))

    def _total_low_mka(self):        
        for rec in self:
            rec.total_tonnage_low_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('ni','<','1.8'),('pile','like','MKA')]).mapped('toonage')))

    def _total_hi_mka(self):        
        for rec in self:
            rec.total_tonnage_hi_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8'),('pile','like','MKA')]).mapped('toonage')))
    
    def _total_mka(self):        
        for rec in self:
            rec.total_tonnage_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('pile','like','MKA')]).mapped('toonage')))
            rec.total_tonnage_ready_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('pile','like','MKA')]).mapped('toonage')))
            rec.total_tonnage_ready_final_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('pile','like','MKA')]).mapped('toonage')))

    # ini SMA Only
    def _total_li_sma(self):        
        for rec in self:
            rec.total_tonnage_li_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5'),('pile','like','SMA')]).mapped('toonage')))

    def _total_low_sma(self):        
        for rec in self:
            rec.total_tonnage_low_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>','1.5'),('ni','<','1.8'),('pile','like','SMA')]).mapped('toonage')))

    def _total_hi_sma(self):        
        for rec in self:
            rec.total_tonnage_hi_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8'),('pile','like','SMA')]).mapped('toonage')))
    
    def _total_sma(self):        
        for rec in self:
            rec.total_tonnage_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('pile','like','SMA')]).mapped('toonage')))
            rec.total_tonnage_ready_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('pile','like','SMA')]).mapped('toonage')))
            rec.total_tonnage_ready_final_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('pile','like','SMA')]).mapped('toonage'))) - float(sum(self.env['gag.oa.qc.daily.production.barging'].search([('production_id', '=',rec.id),('contractor','like','SMA')]).mapped('loaded')))


class DailyProductionDetail(models.Model):    
    _name = "gag.oa.qc.daily.production.detail"
    _description = "Daily Production Detail"

    production_id = fields.Many2one('gag.oa.qc.daily.production', 'Parent')
    pile = fields.Char('Pile',required = True)
    toonage = fields.Float('Tonnage',digit=(0,4))
    ni = fields.Float('Ni',digit=(0,2))
    co = fields.Float('Co',digit=(0,2))
    fe = fields.Float('Fe',digit=(0,2))
    si = fields.Float('Si',digit=(0,2))
    ca = fields.Float('Ca',digit=(0,2))
    mg = fields.Float('Mg',digit=(0,2))
    bc = fields.Float('Bc',digit=(0,2))

class DailyProductionbarging(models.Model):    
    _name = "gag.oa.qc.daily.production.barging"
    _description = "Daily Production Barging"

    production_id = fields.Many2one('gag.oa.qc.daily.production', 'Parent')
    tongkang_id = fields.Many2one('gag.oa.qc.barging.detail','Reference')

    no =fields.Integer('Number',related='tongkang_id.no')
    tongkang =fields.Char('Tongkang / LCT',related='tongkang_id.tongkang')
    contractor =fields.Char('Tongkang / LCT',related='tongkang_id.contractor')
    loaded = fields.Float('Loaded',related='tongkang_id.loaded')

class MonthlyProduction(models.Model):
    _name = "gag.oa.qc.monthly.production"
    _description = "Monthly Production"

    month = fields.Integer('Month', required=True)
    year = fields.Integer('Year', required=True)
    id_production = fields.One2many('gag.oa.qc.monthly.production_detail', 'production_id', 'Production Detail')

class MonthlyProductionDetail(models.Model):
    _name = "gag.oa.qc.monthly.production_detail"
    _description = "Monthly Production Detail"

    production_id = fields.Many2one('gag.oa.qc.monthly.production', 'Parent')
    production_detai_id = fields.Many2one('gag.oa.qc.daily.production.detail','Reference')