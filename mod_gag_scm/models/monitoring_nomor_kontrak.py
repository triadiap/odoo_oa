from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import base64
import xlrd

class SCMMonotoringNomorLelang(models.Model):
    _name="gag.oa.scm.monitoring.nomor.lelang"
    _description = "Daftar nomor lelang"

    bantex = fields.Char('Arsip Divisi')
    nomor = fields.Char('Nomor',required=True)
    keterangan = fields.Char('Keterangan',required = True)
    currency_id = fields.Many2one('res.currency', string='Currency',default=lambda self: self.env.company.currency_id.id)
    harga = fields.Monetary(string="Harga",currency_field='currency_id', required=True)
    nomor_lanjutan = fields.Char('Nomor Kontrak / SPK',compute='_get_momor_lanjutan')

    def _get_momor_lanjutan(self):
        for rec in self:
            rec.nomor_lanjutan = ''
            for data in self.env['gag.oa.scm.monitoring.nomor.kontrak'].search([('nomor_lelang','=',rec.id)]):
                rec.nomor_lanjutan = data.nomor
            for data in self.env['gag.oa.scm.monitoring.nomor.spk'].search([('nomor_lelang','=',rec.id)]):
                rec.nomor_lanjutan = data.nomor

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.nomor}"
            result.append((record.id, name))  # or any other meaningful field
        return result

class SCMMonotoringNomorPemila(models.Model):
    _name="gag.oa.scm.monitoring.nomor.pemila"
    _description = "Daftar nomor pemilihan langsung"

    bantex = fields.Char('Arsip Divisi')
    nomor = fields.Char('Nomor',required=True)
    keterangan = fields.Char('Keterangan',required = True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    harga = fields.Monetary(string="Harga",currency_field='currency_id', required=True)
    nomor_lanjutan = fields.Char('Nomor Kontrak / SPK',compute='_get_momor_lanjutan')

    def _get_momor_lanjutan(self):
        for rec in self:
            rec.nomor_lanjutan = ''
            for data in self.env['gag.oa.scm.monitoring.nomor.kontrak'].search([('nomor_pemila','=',rec.id)]):
                rec.nomor_lanjutan = data.nomor
            for data in self.env['gag.oa.scm.monitoring.nomor.spk'].search([('nomor_pemila','=',rec.id)]):
                rec.nomor_lanjutan = data.nomor

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.nomor}"
            result.append((record.id, name))  # or any other meaningful field
        return result
    
    
class SCMMonotoringNomorKontrak(models.Model):
    _name="gag.oa.scm.monitoring.nomor.kontrak"
    _description = "Daftar nomor kontrak"

    bantex = fields.Char('Arsip Divisi')
    nomor_lelang = fields.Many2one('gag.oa.scm.monitoring.nomor.lelang','Nomor Lelang')
    nomor_pemila = fields.Many2one('gag.oa.scm.monitoring.nomor.pemila','Nomor Pemila')
    nomor = fields.Char('Nomor',required=True)
    keterangan = fields.Char('Keterangan')
    currency_id = fields.Many2one('res.currency', string='Currency')
    harga = fields.Monetary(string="Harga",currency_field='currency_id')
    tanggal = fields.Date(string="Tanggal ",required=True)

    @api.onchange('nomor_lelang')
    def _get_detail_data_lelang(self):
        for rec in self:
            if(rec.nomor_lelang != False):
                rec.keterangan = rec.nomor_lelang.keterangan
                rec.currency_id = rec.nomor_lelang.currency_id
                rec.harga = rec.nomor_lelang.harga
    @api.onchange('nomor_pemila')
    def _get_detail_data_pemila(self):
        for rec in self:
            if(rec.nomor_pemila != False):
                rec.keterangan = rec.nomor_pemila.keterangan
                rec.currency_id = rec.nomor_pemila.currency_id
                rec.harga = rec.nomor_pemila.harga

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.nomor}"
            result.append((record.id, name))  # or any other meaningful field
        return result
    
    
class SCMMonotoringNomorSPK(models.Model):
    _name="gag.oa.scm.monitoring.nomor.spk"
    _description = "Daftar nomor SPK"

    bantex = fields.Char('Arsip Divisi')
    nomor_lelang = fields.Many2one('gag.oa.scm.monitoring.nomor.lelang','Nomor Lelang')
    nomor_pemila = fields.Many2one('gag.oa.scm.monitoring.nomor.pemila','Nomor Pemila')
    nomor = fields.Char('Nomor',required=True)
    keterangan = fields.Char('Keterangan')
    currency_id = fields.Many2one('res.currency', string='Currency')
    harga = fields.Monetary(string="Harga",currency_field='currency_id')
    tanggal = fields.Date(string="Tanggal ",required=True)

    @api.onchange('nomor_lelang')
    def _get_detail_data_lelang(self):
        for rec in self:
            if(rec.nomor_lelang != False):
                rec.keterangan = rec.nomor_lelang.keterangan
                rec.currency_id = rec.nomor_lelang.currency_id
                rec.harga = rec.nomor_lelang.harga
    @api.onchange('nomor_pemila')
    def _get_detail_data_pemila(self):
        for rec in self:
            if(rec.nomor_pemila != False):
                rec.keterangan = rec.nomor_pemila.keterangan
                rec.currency_id = rec.nomor_pemila.currency_id
                rec.harga = rec.nomor_pemila.harga

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.nomor}"
            result.append((record.id, name))  # or any other meaningful field
        return result