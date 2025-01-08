# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import datetime

class DetailPaymentProcess(models.Model):
    _name ='detail.payment'
    _description = "Save Detail Transient Payment as Permanent Data"

    transid = fields.Many2one('transaksi.anggaran', string='Related Model')
    name = fields.Char(string='Name of Transaction')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.ref('base.IDR').id)
    val_payment = fields.Monetary(string='Payment Amount', help="Payment Value", currency_field='currency_id', required=True)
    budget_trans = fields.Monetary(string='Outstanding Balance', help="Outstanding Balance", currency_field='currency_id', required=True)
    payment_memo = fields.Text(string='Memo')