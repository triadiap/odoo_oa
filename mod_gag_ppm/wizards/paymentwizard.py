# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import datetime

class TransactionPayment(models.TransientModel):
    _name = 'transaction.payment.wizard'
    _description = 'Detail Transaction Payment'

    nama_transaksi = fields.Char(string='Name')
    related_field = fields.Many2one('transaksi.anggaran', string='Related Model')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.ref('base.IDR').id)
    payment_value = fields.Monetary(string='Outstanding Payment', help="Payment Value", currency_field='currency_id', required=True)
    sum_transaction = fields.Monetary(string='Transaction', help="Transaction Value", currency_field='currency_id', required=True)
    memo_payment = fields.Text(string='Memo')

    @api.model
    def default_get(self, fields):
        res = super(TransactionPayment, self).default_get(fields)
        if self._context.get('active_id'):
            model = self.env['transaksi.anggaran'].browse(self._context.get('active_id'))
            res['nama_transaksi'] = model.name
            res['related_field'] = model.id
            transactionperbudget = sum(self.env['detail.trans.perbudget'].search([('detail_trans_id','=',self._context.get('active_id'))]).mapped('transaction_subtotal'))
            totalpaymentperbudget = sum(self.env['detail.payment'].search([('transid','=',self._context.get('active_id'))]).mapped('val_payment'))
            res['sum_transaction'] = transactionperbudget
            res['payment_value'] = transactionperbudget - totalpaymentperbudget
        return res
    def action_confirm(self):
        # Retrieve the data from the wizard
        transid = self.related_field
        name = self.nama_transaksi
        val_payment = self.payment_value
        budget_trans = self.sum_transaction
        payment_memo = self.memo_payment
        # Create a record in the target model
        if isinstance(transid, models.Model):
            # Ensure it is not empty and get the ID of the first record
            if transid:
                transid_value = transid.id  # Get the ID of the record
            else:
                raise ValidationError("The provided 'transid' recordset is empty.")
        else:
            # If transid is supposed to be an ID, you can raise an error
            raise ValidationError("Expected 'transid' to be a recordset or a valid ID.")

            # Prepare the vals dictionary
        vals = {
            'transid': transid_value,  # Use the extracted ID
            'name': name,
            'val_payment': val_payment,
            'budget_trans': budget_trans,
            'payment_memo': payment_memo
        }

        # Create the new record in the detail.payment model
        self.env['detail.payment'].create(vals)

        transactionperbudget = sum(self.env['detail.trans.perbudget'].search(
            [('detail_trans_id', '=', self._context.get('active_id'))]).mapped('transaction_subtotal'))
        totalpaymentperbudget = sum(
            self.env['detail.payment'].search([('transid', '=', self._context.get('active_id'))]).mapped('val_payment'))
        percentagedeliverable = float((totalpaymentperbudget / transactionperbudget) * 100)

        if self._context.get('active_id'):
            get_transaksi_anggaran = self.env['transaksi.anggaran'].search([('id', '=', self._context.get('active_id'))])
            get_transaksi_anggaran.deliverable = percentagedeliverable
            if percentagedeliverable < float(100):
                get_transaksi_anggaran.state = 'done'
            else:
                get_transaksi_anggaran.state = 'paid'
        pass


