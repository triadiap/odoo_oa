from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import timedelta
import base64
import xlrd

class DailyProductionReport(models.Model):
    _name = "gag.oa.qc.daily.production"
    _description = "Daily Production"

    tanggal = fields.Date('Tanggal report', required=True)
    tanggal_update = fields.Date('Tanggal Update',compute='_calculate_tanggal_update')
    site = fields.Char('Site', required=True)
    file = fields.Binary('Attachment')
    file_upload = fields.Binary('Import File')
    file_name_upload = fields.Char('Import File Name')
    id_production = fields.One2many('gag.oa.qc.daily.production.detail', 'production_id', 'Production Detail')
    id_tongkang = fields.One2many('gag.oa.qc.daily.production.barging', 'production_id', 'List Tongkan')
    id_tongkang_sma = fields.One2many('gag.oa.qc.daily.production.barging.sma', 'production_id', 'List Tongkan')
    id_tongkang_mka = fields.One2many('gag.oa.qc.daily.production.barging.mka', 'production_id', 'List Tongkan')

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

    total_ni_li_mka = fields.Float("Tonnage",compute="_total_li_mka",digit=(0,2))
    total_ni_low_mka = fields.Float("Tonnage",compute="_total_low_mka",digit=(0,2))
    total_ni_hi_mka = fields.Float("Tonnage",compute="_total_hi_mka",digit=(0,2))

    total_co_li_mka = fields.Float("Tonnage",compute="_total_li_mka",digit=(0,2))
    total_co_low_mka = fields.Float("Tonnage",compute="_total_low_mka",digit=(0,2))
    total_co_hi_mka = fields.Float("Tonnage",compute="_total_hi_mka",digit=(0,2))

    total_fe_li_mka = fields.Float("Tonnage",compute="_total_li_mka",digit=(0,2))
    total_fe_low_mka = fields.Float("Tonnage",compute="_total_low_mka",digit=(0,2))
    total_fe_hi_mka = fields.Float("Tonnage",compute="_total_hi_mka",digit=(0,2))

    total_si_li_mka = fields.Float("Tonnage",compute="_total_li_mka",digit=(0,2))
    total_si_low_mka = fields.Float("Tonnage",compute="_total_low_mka",digit=(0,2))
    total_si_hi_mka = fields.Float("Tonnage",compute="_total_hi_mka",digit=(0,2))

    total_ca_li_mka = fields.Float("Tonnage",compute="_total_li_mka",digit=(0,2))
    total_ca_low_mka = fields.Float("Tonnage",compute="_total_low_mka",digit=(0,2))
    total_ca_hi_mka = fields.Float("Tonnage",compute="_total_hi_mka",digit=(0,2))

    total_mg_li_mka = fields.Float("Tonnage",compute="_total_li_mka",digit=(0,2))
    total_mg_low_mka = fields.Float("Tonnage",compute="_total_low_mka",digit=(0,2))
    total_mg_hi_mka = fields.Float("Tonnage",compute="_total_hi_mka",digit=(0,2))

    total_bc_li_mka = fields.Float("Tonnage",compute="_total_li_mka",digit=(0,2))
    total_bc_low_mka = fields.Float("Tonnage",compute="_total_low_mka",digit=(0,2))
    total_bc_hi_mka = fields.Float("Tonnage",compute="_total_hi_mka",digit=(0,2))

    total_tonnage_mka = fields.Float("Tonnage",compute="_total_mka",digit=(0,4))
    total_ni_mka = fields.Float("Tonnage",compute="_total_mka",digit=(0,2))
    total_co_mka = fields.Float("Tonnage",compute="_total_mka",digit=(0,2))
    total_fe_mka = fields.Float("Tonnage",compute="_total_mka",digit=(0,2))
    total_si_mka = fields.Float("Tonnage",compute="_total_mka",digit=(0,2))
    total_ca_mka = fields.Float("Tonnage",compute="_total_mka",digit=(0,2))
    total_mg_mka = fields.Float("Tonnage",compute="_total_mka",digit=(0,2))
    total_bc_mka = fields.Float("Tonnage",compute="_total_mka",digit=(0,2))
    
    total_tonnage_ready_mka = fields.Float("Total Rady To Barge MKA",compute="_total_mka",digit=(0,4))
    total_tonnage_ready_final_mka = fields.Float("Total Ready To Barge MKA Final",compute="_total_mka",digit=(0,4))

    # sma
    total_tonnage_li_sma = fields.Float("Tonnage",compute="_total_li_sma",digit=(0,4))
    total_tonnage_low_sma = fields.Float("Tonnage",compute="_total_low_sma",digit=(0,4))
    total_tonnage_hi_sma = fields.Float("Tonnage",compute="_total_hi_sma",digit=(0,4))


    total_ni_li_sma = fields.Float("Tonnage",compute="_total_li_sma",digit=(0,2))
    total_ni_low_sma = fields.Float("Tonnage",compute="_total_low_sma",digit=(0,2))
    total_ni_hi_sma = fields.Float("Tonnage",compute="_total_hi_sma",digit=(0,2))
    
    total_co_li_sma = fields.Float("Tonnage",compute="_total_li_sma",digit=(0,2))
    total_co_low_sma = fields.Float("Tonnage",compute="_total_low_sma",digit=(0,2))
    total_co_hi_sma = fields.Float("Tonnage",compute="_total_hi_sma",digit=(0,2))
    
    total_fe_li_sma = fields.Float("Tonnage",compute="_total_li_sma",digit=(0,2))
    total_fe_low_sma = fields.Float("Tonnage",compute="_total_low_sma",digit=(0,2))
    total_fe_hi_sma = fields.Float("Tonnage",compute="_total_hi_sma",digit=(0,2))
    
    total_si_li_sma = fields.Float("Tonnage",compute="_total_li_sma",digit=(0,2))
    total_si_low_sma = fields.Float("Tonnage",compute="_total_low_sma",digit=(0,2))
    total_si_hi_sma = fields.Float("Tonnage",compute="_total_hi_sma",digit=(0,2))
    
    total_ca_li_sma = fields.Float("Tonnage",compute="_total_li_sma",digit=(0,2))
    total_ca_low_sma = fields.Float("Tonnage",compute="_total_low_sma",digit=(0,2))
    total_ca_hi_sma = fields.Float("Tonnage",compute="_total_hi_sma",digit=(0,2))
    
    total_mg_li_sma = fields.Float("Tonnage",compute="_total_li_sma",digit=(0,2))
    total_mg_low_sma = fields.Float("Tonnage",compute="_total_low_sma",digit=(0,2))
    total_mg_hi_sma = fields.Float("Tonnage",compute="_total_hi_sma",digit=(0,2))
    
    total_bc_li_sma = fields.Float("Tonnage",compute="_total_li_sma",digit=(0,2))
    total_bc_low_sma = fields.Float("Tonnage",compute="_total_low_sma",digit=(0,2))
    total_bc_hi_sma = fields.Float("Tonnage",compute="_total_hi_sma",digit=(0,2))

    total_tonnage_sma = fields.Float("Tonnage",compute="_total_sma",digit=(0,4))    
    total_ni_sma = fields.Float("Tonnage",compute="_total_sma",digit=(0,2))
    total_co_sma = fields.Float("Tonnage",compute="_total_sma",digit=(0,2))
    total_fe_sma = fields.Float("Tonnage",compute="_total_sma",digit=(0,2))
    total_si_sma = fields.Float("Tonnage",compute="_total_sma",digit=(0,2))
    total_ca_sma = fields.Float("Tonnage",compute="_total_sma",digit=(0,2))
    total_mg_sma = fields.Float("Tonnage",compute="_total_sma",digit=(0,2))
    total_bc_sma = fields.Float("Tonnage",compute="_total_sma",digit=(0,2))

    total_tonnage_ready_sma = fields.Float("Total Rady To Barge SMA",compute="_total_sma",digit=(0,4))
    total_tonnage_ready_final_sma = fields.Float("Total Ready To Barge SMA Final",compute="_total_sma",digit=(0,4))

    waiting_essay_sma = fields.Float("Waiting Essay",compute="_total_waiting",digit=(0,4))
    waiting_essay_mka = fields.Float("Waiting Essay",compute="_total_waiting",digit=(0,4))
    
    def process_excel_file(self):
        if not self.file_upload:
            raise ValidationError(_("Please upload an Excel file."))
        if not self.file_name_upload:
            raise ValidationError(_("File name is missing."))


        # Decode the file
        file_content = base64.b64decode(self.file_upload)

        # Open the workbook
        workbook = xlrd.open_workbook(file_contents=file_content)
        sheet = workbook.sheet_by_index(0)  # Assuming the first sheet

        # Iterate through rows and process data
        for deletedId in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',self.id)]):
            deletedId.unlink()
        for row_index in range(4, sheet.nrows):  # Skip the header row
            if(sheet.cell_value(row_index, 2)!=""):
                self.env['gag.oa.qc.daily.production.detail'].create({
                    'production_id': self.id,
                    'pile' : sheet.cell_value(row_index, 2),
                    'asal_lokasi' : sheet.cell_value(row_index, 3),
                    'lokasi_dumping' : sheet.cell_value(row_index, 4),
                    'toonage' : float(sheet.cell_value(row_index, 5)),
                    'ni' : float(sheet.cell_value(row_index, 6)),
                    'co': float(sheet.cell_value(row_index, 7)),
                    'fe': float(sheet.cell_value(row_index, 8)),
                    'si': float(sheet.cell_value(row_index, 9)),
                    'ca': float(sheet.cell_value(row_index, 10)),
                    'mg': float(sheet.cell_value(row_index, 11)),
                    'sm': float(sheet.cell_value(row_index, 14))
                })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }       
    def _calculate_tanggal_update(self):
        for rec in self:
            if rec.tanggal:
                rec.tanggal_update = rec.tanggal+  timedelta(days=1)
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
            rec.total_tonnage_li = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5'),('ni','>','0')]).mapped('toonage')))

    def _total_tonnage_low(self):        
        for rec in self:
            rec.total_tonnage_low = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('ni','<','1.8')]).mapped('toonage')))

    def _total_tonnage_hi(self):        
        for rec in self:
            rec.total_tonnage_hi = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]).mapped('toonage')))


    def _total_ni(self):
        for rec in self:
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.ni*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            rec.total_ni= round(tmpTotal1/tmpTotal2,2)
    def _total_ni_li(self):
        for rec in self:
            rec.total_ni_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5'),('ni','>','0')]):
                tmpTotal1 += detail.ni*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_ni_li= round(tmpTotal1/tmpTotal2,2)
            
    def _total_ni_low(self):
        for rec in self:
            rec.total_ni_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.ni*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_ni_low= round(tmpTotal1/tmpTotal2,0)

    def _total_ni_hi(self):
        for rec in self:
            rec.total_ni_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.ni*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_ni_hi= round(tmpTotal1/tmpTotal2,0)

    def _total_co(self):
        for rec in self:
            rec.total_co = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.co*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_co= round(tmpTotal1/tmpTotal2,2)
    def _total_co_li(self):
        for rec in self:
            rec.total_co_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5'),('ni','>','0')]):
                tmpTotal1 += detail.co*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_co_li= round(tmpTotal1/tmpTotal2,2)
            
    def _total_co_low(self):
        for rec in self:
            rec.total_co_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.co*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_co_low= round(tmpTotal1/tmpTotal2,2)

    def _total_co_hi(self):
        for rec in self:
            rec.total_co_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.co*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_co_hi= round(tmpTotal1/tmpTotal2,2)

    def _total_fe(self):
        for rec in self:
            rec.total_fe = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.fe*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_fe= round(tmpTotal1/tmpTotal2,2)
    def _total_fe_li(self):
        for rec in self:
            rec.total_fe_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5'),('ni','>','0')]):
                tmpTotal1 += detail.fe*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_fe_li= round(tmpTotal1/tmpTotal2,2)
            
    def _total_fe_low(self):
        for rec in self:
            rec.total_fe_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.fe*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_fe_low= round(tmpTotal1/tmpTotal2,2)

    def _total_fe_hi(self):
        for rec in self:
            rec.total_fe_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.fe*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_fe_hi= round(tmpTotal1/tmpTotal2,2)

    def _total_si(self):
        for rec in self:
            rec.total_si =0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.si*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_si= round(tmpTotal1/tmpTotal2,2)
    def _total_si_li(self):
        for rec in self:
            rec.total_si_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5'),('ni','>','0')]):
                tmpTotal1 += detail.si*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_si_li= round(tmpTotal1/tmpTotal2,2)
            
    def _total_si_low(self):
        for rec in self:
            rec.total_si_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.si*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_si_low= round(tmpTotal1/tmpTotal2,2)

    def _total_si_hi(self):
        for rec in self:
            rec.total_si_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.si*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_si_hi= round(tmpTotal1/tmpTotal2,2)

    def _total_ca(self):
        for rec in self:
            rec.total_ca = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.ca*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_ca= round(tmpTotal1/tmpTotal2,2)
    def _total_ca_li(self):
        for rec in self:
            rec.total_ca_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5'),('ni','>','0')]):
                tmpTotal1 += detail.ca*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_ca_li= round(tmpTotal1/tmpTotal2,2)
            
    def _total_ca_low(self):
        for rec in self:
            rec.total_ca_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.ca*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_ca_low= round(tmpTotal1/tmpTotal2,2)

    def _total_ca_hi(self):
        for rec in self:
            rec.total_ca_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.ca*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_ca_hi= round(tmpTotal1/tmpTotal2,2)

    def _total_mg(self):
        for rec in self:
            rec.total_mg = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.mg*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_mg= round(tmpTotal1/tmpTotal2,2)
    def _total_mg_li(self):
        for rec in self:
            rec.total_mg_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5'),('ni','>','0')]):
                tmpTotal1 += detail.mg*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_mg_li= round(tmpTotal1/tmpTotal2,2)
            
    def _total_mg_low(self):
        for rec in self:
            rec.total_mg_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.mg*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_mg_low= round(tmpTotal1/tmpTotal2,2)

    def _total_mg_hi(self):
        for rec in self:
            rec.total_mg_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.mg*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_mg_hi= round(tmpTotal1/tmpTotal2,2)

    def _total_bc(self):
        for rec in self:
            rec.total_bc = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id)]):
                tmpTotal1 += detail.bc*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_bc= round(tmpTotal1/tmpTotal2,2)
    def _total_bc_li(self):
        for rec in self:
            rec.total_bc_li = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','<','1.5'),('ni','>','0')]):
                tmpTotal1 += detail.bc*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_bc_li= round(tmpTotal1/tmpTotal2,2)
            
    def _total_bc_low(self):
        for rec in self:
            rec.total_bc_low = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.5'),('ni','<','1.8')]):
                tmpTotal1 += detail.bc*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_bc_low= round(tmpTotal1/tmpTotal2,2)

    def _total_bc_hi(self):
        for rec in self:
            rec.total_bc_hi = 0
            tmpTotal1 = 0
            tmpTotal2 = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('production_id', '=',rec.id),('ni','>=','1.8')]):
                tmpTotal1 += detail.bc*detail.total_tonnage
                tmpTotal2 += detail.total_tonnage
            if(tmpTotal2 != 0):
                rec.total_bc_hi= round(tmpTotal1/tmpTotal2,2)

    # ini mka only

    def _total_li_mka(self):        
        for rec in self:
            rec.total_tonnage_li_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','<','1.5'),('ni','>','0'),('pile','like','MKA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage')))
            rec.total_ni_li_mka = 0
            rec.total_co_li_mka = 0
            rec.total_fe_li_mka = 0
            rec.total_si_li_mka = 0
            rec.total_ca_li_mka = 0
            rec.total_mg_li_mka = 0
            rec.total_bc_li_mka = 0
            tmpNI = 0
            tmpCO = 0
            tmpFE = 0
            tmpSI = 0
            tmpCA = 0
            tmpMG = 0
            tmpBC = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '=',rec.tanggal),('ni','<','1.5'),('ni','>','0'),('pile','like','MKA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]):
                tmpNI += detail.ni*detail.total_tonnage            
                tmpCO += detail.co*detail.total_tonnage        
                tmpFE += detail.fe*detail.total_tonnage
                tmpSI +=detail.si*detail.total_tonnage
                tmpCA +=detail.ca*detail.total_tonnage
                tmpMG +=detail.mg*detail.total_tonnage
                tmpBC +=detail.bc*detail.total_tonnage
            if(rec.total_tonnage_li_mka !=0):
                rec.total_ni_li_mka = round(tmpNI/rec.total_tonnage_li_mka,2)
                rec.total_co_li_mka = round(tmpCO/rec.total_tonnage_li_mka,2)
                rec.total_fe_li_mka = round(tmpFE/rec.total_tonnage_li_mka,2)
                rec.total_si_li_mka = round(tmpSI/rec.total_tonnage_li_mka,2)
                rec.total_ca_li_mka = round(tmpCA/rec.total_tonnage_li_mka,2)
                rec.total_mg_li_mka = round(tmpMG/rec.total_tonnage_li_mka,2)
                rec.total_bc_li_mka = round(tmpBC/rec.total_tonnage_li_mka,2)

    def _total_low_mka(self):        
        for rec in self:
            rec.total_tonnage_low_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.5'),('ni','<','1.8'),('pile','like','MKA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage')))
            rec.total_ni_low_mka = 0
            rec.total_co_low_mka = 0
            rec.total_fe_low_mka = 0
            rec.total_si_low_mka = 0
            rec.total_ca_low_mka = 0
            rec.total_mg_low_mka = 0
            rec.total_bc_low_mka = 0
            tmpNI = 0
            tmpCO = 0
            tmpFE = 0
            tmpSI = 0
            tmpCA = 0
            tmpMG = 0
            tmpBC = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.5'),('ni','<','1.8'),('pile','like','MKA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]):
                tmpNI += detail.ni*detail.total_tonnage            
                tmpCO +=  detail.co*detail.total_tonnage
                tmpFE += detail.fe*detail.total_tonnage
                tmpSI += detail.si*detail.total_tonnage
                tmpCA += detail.ca*detail.total_tonnage
                tmpMG += detail.mg*detail.total_tonnage
                tmpBC += detail.bc*detail.total_tonnage
            if(rec.total_tonnage_low_mka !=0):
                rec.total_ni_low_mka = round(tmpNI/rec.total_tonnage_low_mka,2)
                rec.total_co_low_mka = round(tmpCO/rec.total_tonnage_low_mka,2)
                rec.total_fe_low_mka = round(tmpFE/rec.total_tonnage_low_mka,2)
                rec.total_si_low_mka = round(tmpSI/rec.total_tonnage_low_mka,2)
                rec.total_ca_low_mka = round(tmpCA/rec.total_tonnage_low_mka,2)
                rec.total_mg_low_mka = round(tmpMG/rec.total_tonnage_low_mka,2)
                rec.total_bc_low_mka = round(tmpBC/rec.total_tonnage_low_mka,2)

    def _total_hi_mka(self):        
        for rec in self:
            rec.total_tonnage_hi_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.8'),('pile','like','MKA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage')))
            rec.total_ni_hi_mka = 0
            rec.total_co_hi_mka = 0
            rec.total_fe_hi_mka = 0
            rec.total_si_hi_mka = 0
            rec.total_ca_hi_mka = 0
            rec.total_mg_hi_mka = 0
            rec.total_bc_hi_mka = 0
            tmpNI = 0
            tmpCO = 0
            tmpFE = 0
            tmpSI = 0
            tmpCA = 0
            tmpMG = 0
            tmpBC = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.8'),('pile','like','MKA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]):
                tmpNI += detail.ni*detail.total_tonnage            
                tmpCO += detail.co*detail.total_tonnage
                tmpFE += detail.fe*detail.total_tonnage
                tmpSI += detail.si*detail.total_tonnage
                tmpCA += detail.ca*detail.total_tonnage
                tmpMG += detail.mg*detail.total_tonnage
                tmpBC += detail.bc*detail.total_tonnage
            if(rec.total_tonnage_hi_mka !=0):
                rec.total_ni_hi_mka = round(tmpNI/rec.total_tonnage_hi_mka,2)
                rec.total_co_hi_mka = round(tmpCO/rec.total_tonnage_hi_mka,2)
                rec.total_fe_hi_mka = round(tmpFE/rec.total_tonnage_hi_mka,2)
                rec.total_si_hi_mka = round(tmpSI/rec.total_tonnage_hi_mka,2)
                rec.total_ca_hi_mka = round(tmpCA/rec.total_tonnage_hi_mka,2)
                rec.total_mg_hi_mka = round(tmpMG/rec.total_tonnage_hi_mka,2)
                rec.total_bc_hi_mka = round(tmpBC/rec.total_tonnage_hi_mka,2)

    def _total_mka(self):        
        for rec in self:
            rec.total_tonnage_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('pile','like','MKA'),('ni','>','0'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage')))
            rec.total_tonnage_ready_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.5'),('pile','like','MKA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage')))
            rec.total_tonnage_ready_final_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.5'),('pile','like','MKA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage'))) - float(sum(self.env['gag.oa.qc.daily.production.barging'].search([('production_id', '=',rec.id),('contractor','like','MKA')]).mapped('loaded')))
            rec.total_ni_mka=0
            rec.total_co_mka = 0
            rec.total_fe_mka = 0
            rec.total_si_mka = 0
            rec.total_ca_mka = 0
            rec.total_mg_mka = 0
            rec.total_bc_mka = 0
            tmpNI = 0
            tmpCO = 0
            tmpFE = 0
            tmpSI = 0
            tmpCA = 0
            tmpMG = 0
            tmpBC = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('pile','like','MKA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]):
                tmpNI += detail.ni*detail.total_tonnage
                tmpCO += detail.co*detail.total_tonnage
                tmpFE += detail.fe * detail.total_tonnage
                tmpSI += detail.si * detail.total_tonnage
                tmpCA += detail.ca * detail.total_tonnage
                tmpMG += detail.mg * detail.total_tonnage
                tmpBC += detail.bc * detail.total_tonnage
            if(rec.total_tonnage_mka!=0):
                rec.total_ni_mka = round(tmpNI/rec.total_tonnage_mka,2)
                rec.total_co_mka = round(tmpCO/rec.total_tonnage_mka,2)
                rec.total_fe_mka = round(tmpFE/rec.total_tonnage_mka,2)
                rec.total_si_mka = round(tmpSI/rec.total_tonnage_mka,2)
                rec.total_ca_mka = round(tmpCA/rec.total_tonnage_mka,2)
                rec.total_mg_mka = round(tmpMG/rec.total_tonnage_mka,2)
                rec.total_bc_mka = round(tmpBC/rec.total_tonnage_mka,2)

    # ini SMA Only
    def _total_li_sma(self):        
        for rec in self:
            rec.total_tonnage_li_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','<','1.5'),('ni','>','0'),('pile','like','SMA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage')))
            rec.total_ni_li_sma = 0
            rec.total_co_li_sma = 0
            rec.total_fe_li_sma = 0
            rec.total_si_li_sma = 0
            rec.total_ca_li_sma = 0
            rec.total_mg_li_sma = 0
            rec.total_bc_li_sma = 0
            tmpNI = 0
            tmpCO = 0
            tmpFE = 0
            tmpSI = 0
            tmpCA = 0
            tmpMG = 0
            tmpBC = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','<','1.5'),('ni','>','0'),('pile','like','SMA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]):
                tmpNI += detail.ni*detail.total_tonnage            
                tmpCO += detail.co*detail.total_tonnage
                tmpFE += detail.fe*detail.total_tonnage
                tmpSI += detail.si*detail.total_tonnage
                tmpCA += detail.ca*detail.total_tonnage
                tmpMG += detail.mg*detail.total_tonnage
                tmpBC += detail.bc*detail.total_tonnage
            if(rec.total_tonnage_li_sma !=0):
                rec.total_ni_li_sma = round(tmpNI/rec.total_tonnage_li_sma,2)
                rec.total_co_li_sma = round(tmpCO/rec.total_tonnage_li_sma,2)
                rec.total_fe_li_sma = round(tmpFE/rec.total_tonnage_li_sma,2)
                rec.total_si_li_sma = round(tmpSI/rec.total_tonnage_li_sma,2)
                rec.total_ca_li_sma = round(tmpCA/rec.total_tonnage_li_sma,2)
                rec.total_mg_li_sma = round(tmpMG/rec.total_tonnage_li_sma,2)
                rec.total_bc_li_sma = round(tmpBC/rec.total_tonnage_li_sma,2)

    def _total_low_sma(self):        
        for rec in self:
            rec.total_tonnage_low_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.5'),('ni','<','1.8'),('pile','like','SMA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage')))
            rec.total_ni_low_sma = 0
            rec.total_co_low_sma = 0
            rec.total_fe_low_sma = 0
            rec.total_si_low_sma = 0
            rec.total_ca_low_sma = 0
            rec.total_mg_low_sma = 0
            rec.total_bc_low_sma = 0
            tmpNI = 0
            tmpCO = 0
            tmpFE = 0
            tmpSI = 0
            tmpCA = 0
            tmpMG = 0
            tmpBC = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.5'),('ni','<','1.8'),('pile','like','SMA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]):
                tmpNI += detail.ni*detail.total_tonnage            
                tmpCO += detail.co*detail.total_tonnage
                tmpFE += detail.fe * detail.total_tonnage
                tmpSI += detail.si*detail.total_tonnage
                tmpCA += detail.ca*detail.total_tonnage
                tmpMG += detail.ca*detail.total_tonnage
                tmpBC += detail.bc*detail.total_tonnage
            if(rec.total_tonnage_low_sma !=0):
                rec.total_ni_low_sma = round(tmpNI/rec.total_tonnage_low_sma,2)
                rec.total_co_low_sma = round(tmpCO/rec.total_tonnage_low_sma,2)
                rec.total_fe_low_sma = round(tmpFE/rec.total_tonnage_low_sma,2)
                rec.total_si_low_sma = round(tmpSI/rec.total_tonnage_low_sma,2)
                rec.total_ca_low_sma = round(tmpCA/rec.total_tonnage_low_sma,2)
                rec.total_mg_low_sma = round(tmpMG/rec.total_tonnage_low_sma,2)
                rec.total_bc_low_sma = round(tmpBC/rec.total_tonnage_low_sma,2)

    def _total_hi_sma(self):        
        for rec in self:
            rec.total_tonnage_hi_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.8'),('pile','like','SMA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage')))
            rec.total_ni_hi_sma = 0
            rec.total_co_hi_sma = 0
            rec.total_fe_hi_sma = 0
            rec.total_si_hi_sma = 0
            rec.total_ca_hi_sma = 0
            rec.total_mg_hi_sma = 0
            rec.total_bc_hi_sma = 0
            tmpNI = 0
            tmpCO = 0
            tmpFE = 0
            tmpSI = 0
            tmpCA = 0
            tmpMG = 0
            tmpBC = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.8'),('pile','like','SMA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]):
                tmpNI += detail.ni*detail.total_tonnage            
                tmpCO += detail.co*detail.total_tonnage
                tmpFE+= detail.fe* detail.total_tonnage
                tmpSI += detail.si*detail.total_tonnage
                tmpCA += detail.ca*detail.total_tonnage
                tmpMG += detail.mg*detail.total_tonnage
                tmpBC += detail.bc*detail.total_tonnage
            if(rec.total_tonnage_hi_sma !=0):
                rec.total_ni_hi_sma = round(tmpNI/rec.total_tonnage_hi_sma,2)
                rec.total_co_hi_sma = round(tmpCO/rec.total_tonnage_hi_sma,2)
                rec.total_fe_hi_sma = round(tmpFE/rec.total_tonnage_hi_sma,2)
                rec.total_si_hi_sma = round(tmpSI/rec.total_tonnage_hi_sma,2)
                rec.total_ca_hi_sma = round(tmpCA/rec.total_tonnage_hi_sma,2)
                rec.total_mg_hi_sma = round(tmpMG/rec.total_tonnage_hi_sma,2)
                rec.total_bc_hi_sma = round(tmpBC/rec.total_tonnage_hi_sma,2)
    
    def _total_sma(self):        
        for rec in self:
            rec.total_tonnage_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('pile','like','SMA'),('ni','>','0'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage')))
            rec.total_tonnage_ready_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.5'),('pile','like','SMA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage')))
            rec.total_tonnage_ready_final_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('ni','>=','1.5'),('pile','like','SMA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]).mapped('total_tonnage'))) - float(sum(self.env['gag.oa.qc.daily.production.barging'].search([('production_id', '=',rec.id),('contractor','like','SMA')]).mapped('loaded')))
            rec.total_ni_sma = 0
            rec.total_co_sma = 0
            rec.total_fe_sma = 0
            rec.total_si_sma = 0
            rec.total_ca_sma = 0
            rec.total_mg_sma = 0
            rec.total_bc_sma = 0
            tmpNI = 0
            tmpCO = 0
            tmpFE = 0
            tmpSI = 0
            tmpCA = 0
            tmpMG = 0
            tmpBC = 0
            for detail in self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('pile','like','SMA'),'|',('tanggal_barging','=',False),('tanggal_barging','>=',rec.tanggal)]):
                tmpNI += detail.ni*detail.total_tonnage
                tmpCO += detail.co*detail.total_tonnage
                tmpFE += detail.fe*detail.total_tonnage
                tmpSI += detail.si*detail.total_tonnage
                tmpCA += detail.ca*detail.total_tonnage
                tmpMG += detail.mg*detail.total_tonnage
                tmpBC += detail.bc*detail.total_tonnage
            if(rec.total_tonnage_sma!=0):
                rec.total_ni_sma = round(tmpNI/rec.total_tonnage_sma,2)
                rec.total_co_sma = round(tmpCO/rec.total_tonnage_sma,2)
                rec.total_fe_sma = round(tmpCO/rec.total_tonnage_sma,2)
                rec.total_si_sma = round(tmpSI/rec.total_tonnage_sma,2)
                rec.total_ca_sma = round(tmpCA/rec.total_tonnage_sma,2)
                rec.total_mg_sma = round(tmpMG/rec.total_tonnage_sma,2)
                rec.total_bc_sma = round(tmpBC/rec.total_tonnage_sma,2)

    def _total_waiting(self):
        for rec in self:     
            data_sma = self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('pile','like','SMA'),('ni','>',0)]).mapped('pile')
            data_mka = self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('pile','like','MKA'),('ni','>',0)]).mapped('pile')
            rec.waiting_essay_sma = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('pile','like','SMA'),('ni','=',0),('pile','not in',data_sma)]).mapped('toonage')))
            rec.waiting_essay_mka = float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('tanggal', '<=',rec.tanggal),('pile','like','MKA'),('ni','=',0),('pile','not in',data_mka)]).mapped('toonage')))



class DailyProductionDetail(models.Model):    
    _name = "gag.oa.qc.daily.production.detail"
    _description = "Daily Production Detail"

    production_id = fields.Many2one('gag.oa.qc.daily.production', 'Parent')
    tanggal = fields.Date("Tanggal", related = 'production_id.tanggal')
    tanggal_barging = fields.Date("Tanggal barging")
    pile = fields.Char('Pile',required = True)
    asal_lokasi = fields.Char('Asal Lokasi',required = True)
    lokasi_dumping = fields.Char('Lokasi Dumping',required = True)
    toonage = fields.Float('Tonnage',digit=(0,4),required=True)
    total_tonnage = fields.Float('Total Tonnage',digit=(0,4),stored=True,compute='_calculate_total_tonnage')
    ni = fields.Float('Ni',digit=(0,2))
    co = fields.Float('Co',digit=(0,2))
    fe = fields.Float('Fe',digit=(0,2))
    si = fields.Float('Si',digit=(0,2))
    ca = fields.Float('Ca',digit=(0,2))
    mg = fields.Float('Mg',digit=(0,2))
    bc = fields.Float('Bc',digit=(0,2))
    sm = fields.Float('Sm',digit=(0,2))

    def name_get(self):
        result = []
        for record in self:
            name = f"({record.pile})"
            result.append((record.id, name))  # or any other meaningful field
        return result 
    
    def _calculate_total_tonnage(self):
        for rec in self:
            rec.total_tonnage =float(sum(self.env['gag.oa.qc.daily.production.detail'].search([('pile','=',rec.pile)]).mapped('toonage')))

class DailyProductionbarging(models.Model):    
    _name = "gag.oa.qc.daily.production.barging"
    _description = "Daily Production Barging"

    production_id = fields.Many2one('gag.oa.qc.daily.production', 'Parent')
    tongkang_id = fields.Many2one('gag.oa.qc.barging.detail','Reference')

    no =fields.Integer('Number',related='tongkang_id.no')
    tongkang =fields.Char('Tongkang / LCT',related='tongkang_id.tongkang')
    contractor =fields.Selection([('SMA','SMA'),('MKA','MKA')],String = "Contactor",related='tongkang_id.contractor')
    loaded = fields.Float('Loaded',related='tongkang_id.loaded')

class DailyProductionbargingSMA(models.Model):    
    _name = "gag.oa.qc.daily.production.barging.sma"
    _description = "Daily Production Barging"

    production_id = fields.Many2one('gag.oa.qc.daily.production', 'Parent')
    tongkang_id = fields.Many2one('gag.oa.qc.barging.detail','Reference')

    no =fields.Integer('Number',related='tongkang_id.no')
    tongkang =fields.Char('Tongkang / LCT',related='tongkang_id.tongkang')
    contractor =fields.Selection([('SMA','SMA'),('MKA','MKA')],String = "Contactor",related='tongkang_id.contractor')
    loaded = fields.Float('Loaded',related='tongkang_id.loaded')

class DailyProductionbargingMKA(models.Model):    
    _name = "gag.oa.qc.daily.production.barging.mka"
    _description = "Daily Production Barging"

    production_id = fields.Many2one('gag.oa.qc.daily.production', 'Parent')
    tongkang_id = fields.Many2one('gag.oa.qc.barging.detail','Reference')

    no =fields.Integer('Number',related='tongkang_id.no')
    tongkang =fields.Char('Tongkang / LCT',related='tongkang_id.tongkang')
    contractor =fields.Selection([('SMA','SMA'),('MKA','MKA')],String = "Contactor",related='tongkang_id.contractor')
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