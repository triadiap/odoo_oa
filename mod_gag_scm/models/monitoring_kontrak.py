from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import base64
import xlrd
class  SCMMonotoringKontrak(models.Model):
    _name = "gag.oa.scm.monitoring.kontrak"
    _description = "LIST KONTRAK"

    vendor_name = fields.Many2one("res.partner",string="Vendor Name", related = 'nomor_kontrak.partner_id')
    deskripsi = fields.Char("Description")
    currency_id = fields.Many2one('res.currency', string='Currency',related="nomor_kontrak.currency_id")
    nomor_kontrak = fields.Many2one('purchase.contract',string="Contract No", required=True)
    nilai_kontrak = fields.Monetary(string="Nilai Kontrak",currency_field='currency_id', required=True,related="nomor_kontrak.nilai_kontrak")
    tgl_kontrak = fields.Date(string="Contract date", required=True,related="nomor_kontrak.contract_release_date")
    mulai_kontrak = fields.Date(string="Start Date", required=True,related="nomor_kontrak.comancement_date")
    selesai_kontrak = fields.Date(string="End Date",required=True,related="nomor_kontrak.completion_date")  
    justification = fields.Date(string="Justifikasi")  
    status = fields.Selection([
        ('open','open'),
        ('closed','closed'),
        ],"Status") 
    status_lease = fields.Selection([
        ('lease','lease'),
        ('non lease','non lease'),
        ],"Lease/Non Lease") 
    jaminan_no = fields.Char(string="Nomor Jaminan Pelaksanaan")  
    jaminan_nama = fields.Char(string="Nama Penjamin")  
    jaminan_nilai = fields.Monetary(string="Nilai Jaminan",currency_field='currency_id')  