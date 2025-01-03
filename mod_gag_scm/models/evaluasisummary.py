# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class SCMEvaluasiSummary(models.Model):
    _name = 'gag.oa.scm.evaluasi.summary'
    _description = 'Office Automation Evaluasi Vendor Summary'

    tahun  = fields.Char(string="Tahun", required=True)
    vendor_name = fields.Many2one("res.partner",string="Vendor Name", required=True)
    nama_pengadaan = fields.Char(string="Nama Pengadaan", required=True)
    alamat = fields.Char(string="Alamat", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency',related="nomor_kontrak.currency_id")
    nomor_kontrak = fields.Many2one('purchase.contract',string="Nomor Kontrak", required=True)
    nilai_kontrak = fields.Monetary(string="Nilai Kontrak",currency_field='currency_id', required=True,related="nomor_kontrak.nilai_kontrak")
    npwp = fields.Char(string="NPWP", required=True)    
    mulai_kontrak = fields.Date(string="Mulai Kontrak", required=True,related="nomor_kontrak.comancement_date")
    selesai_kontrak = fields.Date(string="Selesai Kontrak",required=True,related="nomor_kontrak.completion_date")    
    detail_pembayaran = fields.One2many('gag.oa.scm.evaluasi.summary.detail','evaluasi_id')
    sisa_pembayaran = fields.Monetary(string="Sisa Pembayaran",currency_field='currency_id', compute="_sisa_pembayaran",stored="true")

    def _sisa_pembayaran(self):
        for rec in self:
            terbayar = 0
            if rec.detail_pembayaran.search([('evaluasi_id','=',rec.id),('terbayar','=','true')]):
                terbayar = sum(rec.detail_pembayaran.search([('evaluasi_id','=',rec.id),('terbayar','=','true')]).mapped('jumlah'))
            rec.sisa_pembayaran = rec.nilai_kontrak - terbayar

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.vendor_name} ({record.tahun})"
            result.append((record.id, name))  # or any other meaningful field
        return result


class SCMEvaluasiSummaryDetail(models.Model):
    _name = 'gag.oa.scm.evaluasi.summary.detail'
    _description = 'Office Automation Evaluasi Vendor Summary Detail'

    evaluasi_id = fields.Many2one('gag.oa.scm.evaluasi.summary','Evaluasi')
    currency_id = fields.Many2one('res.currency', string='Currency')
    jumlah = fields.Monetary(string="Jumlah Transaksi",currency_field='currency_id', required=True)
    terbayar = fields.Boolean(String = "Status Terbayar")
    tanggal_terbayar = fields.Date(String = "Tanggal Terbayar")
    file = fields.Binary(String = "Attachment")

