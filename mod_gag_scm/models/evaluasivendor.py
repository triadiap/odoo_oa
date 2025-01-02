# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class SCMEvaluasiVendor(models.Model):
    _name = 'gag.oa.scm.evaluasi'
    _description = 'Office Automation Evaluasi Vendor'

    vendor_name = fields.Many2one("res.partner",string="Vendor Name", required=True)
    jenis_barang = fields.Char(string="Jenis Barang / jasa", required=True)
    tahun  = fields.Char(string="Tahun", required=True)
    evaluasi_detail = fields.One2many('gag.oa.scm.evaluasi.detail', 'evaluasi_id', 'List Evaluasi')

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.vendor_name.name} ({record.tahun})"
            result.append((record.id, name))  # or any other meaningful field
        return result

class SCMEvaluasiVendorDetail(models.Model):    
    _name = 'gag.oa.scm.evaluasi.detail'
    _description = 'Office Automation Evaluasi Vendor Detail'

    vendor_id = fields.Many2one("res.partner",string="Vendor Name",related = "evaluasi_id.vendor_name",store=True)
    po = fields.Many2one('purchase.order',string = 'NO PO',required=True, domain="[('purchase_type', '=', 'pembelian_langsung'),('partner_id','=',vendor_id)]")
    evaluasi_id = fields.Many2one('gag.oa.scm.evaluasi','Evaluasi')
    tanggal = fields.Datetime(string="Tanggal Transaksi", required=True,related="po.date_approve")
    currency_id = fields.Many2one('res.currency', string='Currency',related="po.currency_id")
    jumlah = fields.Monetary(string="Jumlah Transaksi",currency_field='currency_id', required=True, related="po.amount_total")
    nilai_harga = fields.Integer(string="Harga", required=True,default=1)
    nilai_pembayaran = fields.Integer(string="Pembayaran", required=True,default=1)
    nilai_kulatias_jasa = fields.Integer(string="Kualitas Jasa", required=True,default=1)
    nilai_delivery_time = fields.Integer(string="Delivery Time", required=True,default=1)
    jumlah_nilai = fields.Integer(string="Jumlah Nilai", compute='_jumlah_nilai',store=True)
    ikr = fields.Float(string="IKR", compute='_jumlah_nilai',store=True)


    @api.depends('nilai_harga','nilai_pembayaran','nilai_kulatias_jasa','nilai_delivery_time')
    def _jumlah_nilai(self):
        for rec in self :
            rec.jumlah_nilai = rec.nilai_harga+rec.nilai_pembayaran+rec.nilai_kulatias_jasa+rec.nilai_delivery_time
            rec.ikr = rec.jumlah_nilai/4




