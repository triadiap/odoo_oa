# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class SCMEvaluasiVendor(models.Model):
    _name = 'gag.oa.scm.evaluasi'
    _description = 'Office Automation Evaluasi Vendor'

    vendor_name = fields.Char(string="Vendor Name", required=True)
    jenis_barang = fields.Char(string="Jenis Barang / jasa", required=True)
    tahun  = fields.Char(string="Tahun", required=True)
    evaluasi_detail = fields.One2many('gag.oa.scm.evaluasi.detail', 'evaluasi_id', 'List Evaluasi')

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.vendor_name} ({record.tahun})"
            result.append((record.id, name))  # or any other meaningful field
        return result

class SCMEvaluasiVendorDetail(models.Model):    
    _name = 'gag.oa.scm.evaluasi.detail'
    _description = 'Office Automation Evaluasi Vendor Detail'

    evaluasi_id = fields.Many2one('gag.oa.scm.evaluasi','Evaluasi')
    tanggal = fields.Date(string="Tanggal Transaksi", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    jumlah = fields.Monetary(string="Jumlah Transaksi",currency_field='currency_id', required=True)
    nilai_harga = fields.Integer(string="Harga", required=True,default=1)
    nilai_pembayaran = fields.Integer(string="Pembayaran", required=True,default=1)
    nilai_kulatias_jasa = fields.Integer(string="Kulaitas Jasa", required=True,default=1)
    nilai_delivery_time = fields.Integer(string="Delivery Time", required=True,default=1)
    jumlah_nilai = fields.Integer(string="Jumlah Nilai", compute='_jumlah_nilai')
    ikr = fields.Float(string="IKR", compute='_jumlah_nilai')
    po = fields.Char(string="Ket. PO", required=True)


    @api.depends('nilai_harga','nilai_pembayaran','nilai_kulatias_jasa','nilai_delivery_time')
    def _jumlah_nilai(self):
        for rec in self :
            rec.jumlah_nilai = rec.nilai_harga+rec.nilai_pembayaran+rec.nilai_kulatias_jasa+rec.nilai_delivery_time
            rec.ikr = rec.jumlah_nilai/4
