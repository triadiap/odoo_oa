# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import datetime

class BudgetTransactionInput(models.Model):
    _name = "transaksi.anggaran"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Budget Transaction Information"

    name = fields.Char(string="Activity Name", required=True, tracking=True)
    deskripsi_transaksi = fields.Text(string="Notes", tracking=True)
    pillar_name = fields.Many2one('pillar.group', string="Pillar Name", required=True)
    program_code = fields.Many2one('detail.anggaran.perbulan', string="Program", required=True, tracking=True)
    kode_anggaran = fields.Many2one('informasi.perpillar', string="Budget Reference", required=True, tracking=True)
    year_budget = fields.Char(string="Fiscal Year",tracking=True)
    id_transaction_detail = fields.One2many('detail.trans.perbudget', 'detail_trans_id', string="Lines")
    document_payment_id = fields.One2many('detail.payment','transid',string='Payments')
    total_expense_display = fields.Char(string="Total Quantity", compute='_compute_total_activity_expense')
    deliverable = fields.Float(string='% Deliverable', required=True, tracking=True, default = 0.00)
    ribbon_text = fields.Char(string="Ribbon Text", compute="_compute_ribbon_text")
    total_payment_confirmation = fields.Char(string='Total Payment Confirmation', compute='_compute_total_payment_confirmation')
    # ------------------Ini Connect ke Module UAC ------------------------------------------#
    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', readonly=True,tracking=True)
    existing_status = fields.Char(string="Current Status", readonly=True, tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", readonly=True, tracking=True)
    button_visible = fields.Boolean(compute='_compute_button_visibility', store=False, sanitize=False)
    # -------------------------------------------------------------------------------------#
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approval_process', 'Approval Process'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancelled'),
        ('paid', 'Paid')
    ], default="draft", string="Status", tracking=True)
    hide_css = fields.Html(string='CSS', compute='_compute_btn_edit_activation', sanitize=False, store=False)

    @api.depends('state')
    def _compute_btn_edit_activation(self):
        for record in self:
            if record.state in ["approve","done","paid"]:
                record.hide_css = ('''
                                        <style>
                                            .o_form_button_edit {display: none !important;}
                                        </style>
                                        '''
                                   )
            else:
                record.hide_css = False
    def _compute_button_visibility(self):
        for record in self:
            # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.pending_approval_by.id == self.env.user.id)
            else:
                record.button_visible = False

    def action_approval_process(self):
        # UAC Configuration to raise document status as submitted for approval
        if not self.approval_route_id:
            raise ValidationError('Approval route is not defined.')
        next_step = self.approval_route_id.step_ids.sorted(key='sequence')[0]
        self.current_step_id = next_step
        self.state = 'approval_process'
        self.existing_status = 'Document submitted for approval'
        self.pending_approval_by = next_step.user_id
        self.upcoming_status = next_step
        self.message_post(body='Document submitted for approval.')
        # -----------------------------------------------------------------------
    def action_approve(self):
        if self.env.user != self.current_step_id.user_id:
            raise ValidationError('You do not have the required permissions to approve this document.')
        next_step = self.approval_route_id.get_next_step(self.current_step_id)
        if next_step:
            self.current_step_id = next_step
            self.existing_status = 'Document submitted for approval'
            self.pending_approval_by = next_step.user_id
            self.upcoming_status = next_step
        else:
            self.state = 'approve'
            self.existing_status = 'Document has fully approved'
            self.pending_approval_by = None
            self.upcoming_status = None
        self.message_post(body='Document approved.')

    @api.model
    def create(self,vals):
        # UAC Find the configured approval route for the current model for new document creation
        config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
        if config:
            vals['approval_route_id'] = config.approval_route_id.id
            anggaranid = self.env['informasi.perpillar'].browse(vals['kode_anggaran'])
            vals.update({
                'year_budget': anggaranid.tahun_anggaran
            })

        return super(BudgetTransactionInput, self).create(vals)

    def write(self,vals):
        kode_anggaran = vals.get('kode_anggaran')  # Safely get the value of 'kode_anggaran'
        if kode_anggaran:
            anggaranid = self.env['informasi.perpillar'].browse(kode_anggaran)
            if anggaranid.exists():  # Check if the record exists
                vals.update({
                    'year_budget': anggaranid.tahun_anggaran
                })
        return super(BudgetTransactionInput, self).write(vals)

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'
        self.delete_payment()
    def _compute_total_payment_confirmation(self):
        for record in self:
            total_transaksi_confirmed = sum(self.env['detail.payment'].search([('transid','=',record.id)]).mapped('val_payment'))
            record.total_payment_confirmation = f"Rp {float(total_transaksi_confirmed):,.2f}"
    def action_open_payments(self):
        print("Test")
    @api.depends('deliverable')
    def _compute_ribbon_text(self):
        for record in self:
            # Format the float value to two decimal places
            record.ribbon_text = "{:.2f}".format(record.deliverable)
    @api.onchange('kode_anggaran')
    def _onchange_field_b_id(self):
        """Update options in field_b_id based on the selected field_a_id."""
        if self.kode_anggaran:
            # Search for matching records in Model C
            matching_records = self.env['detail.anggaran.perbulan'].search([('anggaran_id', '=', self.kode_anggaran.id)])
            if matching_records:
                # Set domain to show matching records
                return {
                    'domain': {
                        'program_code': [('id', 'in', matching_records.ids)]
                    }
                }
            else:
                # No matching records found, clear field_b_id and set domain to empty
                self.program_code = False
                return {
                    'domain': {
                        'program_code': [('id', '=', False)]
                    }
                }
        else:
            # No value selected in field_a_id, clear field_b_id and set domain to empty
            self.program_code = False
            return {
                'domain': {
                    'program_code': [('id', '=', False)]
                }
            }

    @api.onchange('pillar_name')
    def _onchange_field_a_id(self):
        """Update options in field_b_id based on the selected field_a_id."""
        if self.pillar_name:
            # Search for matching records in Model C
            matching_records = self.env['informasi.perpillar'].search([('kode_pillar', '=', self.pillar_name.id)])
            if matching_records:
                # Set domain to show matching records
                return {
                    'domain': {
                        'kode_anggaran': [('id', 'in', matching_records.ids)]
                    }
                }
            else:
                # No matching records found, clear field_b_id and set domain to empty
                self.kode_anggaran = False
                return {
                    'domain': {
                        'kode_anggaran': [('id', '=', False)]
                    }
                }
        else:
            # No value selected in field_a_id, clear field_b_id and set domain to empty
            self.kode_anggaran = False
            return {
                'domain': {
                    'kode_anggaran': [('id', '=', False)]
                }
            }

    def delete_payment(self):
        payment_records = self.env['detail.payment'].search([('transid', '=', self.id)])
        if payment_records:
            # Deleting related records
            payment_records.unlink()

        return True

    def _compute_activity_expense_total(self):
        for record in self:
            jml_pengeluaran_total = sum(line.transaction_subtotal for line in record.id_transaction_detail)
            record.expense_grand_total = f"{jml_pengeluaran_total:.2f}"

    def _compute_total_activity_expense(self):
        for record in self:
            total_jml_pengeluaran = sum(line.transaction_subtotal for line in record.id_transaction_detail)
            record.total_expense_display = f"Rp {float(total_jml_pengeluaran):,.2f}"

    @api.onchange('kode_anggaran')
    def _onchange_kode_anggaran(self):
        if self.kode_anggaran:
            self.year_budget = self.kode_anggaran.tahun_anggaran
        else:
            self.year_budget = False
class DetailBudgetTransaction(models.Model):
    _name = "detail.trans.perbudget"
    _description = "Detail of Transaction"

    detail_trans_id = fields.Many2one('transaksi.anggaran', string="Parent", ondelete='cascade')
    transaction_item = fields.Char(string="Item Name", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    transaction_amount = fields.Monetary(string='Price', help="Masukkan  Nilai Transaksi", currency_field='currency_id', required=True)
    transaction_qty =  fields.Float(string='Quantity', required=True, tracking=True, default = 1.00)
    transaction_subtotal = fields.Float(string='Subtotal', readonly=True, compute='_compute_subtotal', store=True)
    doc_reff_number = fields.Char(string="Document Reff No")
    file_field = fields.Binary(string="Document Proof (Upload Here)")
    file_name = fields.Char(string="File Name")  # Optional: To store the filename
    transaction_date = fields.Date(string='Transaction Date', required=True)
    kodeprogram = fields.Many2one(related="detail_trans_id.program_code", string="Program", store=True)
    namapillar = fields.Char(related="detail_trans_id.pillar_name.nama_pillar", string="Pillar Name", store=True)
    activity_name = fields.Char(related="detail_trans_id.name", string="Description", store=True)

    @api.depends('transaction_qty', 'transaction_amount')
    def _compute_subtotal(self):
        for line in self:
            line.transaction_subtotal = line.transaction_qty * line.transaction_amount


class BudgetExpenseMonthlyReport(models.Model):
    _name = 'budget.expense.monthly.report'
    _description = 'Monthly Budget and Expense Report'
    _auto = False

    id = fields.Integer('ID', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    month_number = fields.Char('Month Number')
    tahunanggaran = fields.Char('Budget Year')
    month_name = fields.Char('Month Name')
    total_budget = fields.Monetary('Total Budget Amount',currency_field='currency_id')
    total_expense = fields.Monetary('Total Expense Amount',currency_field='currency_id')

    def init(self):
        tools.drop_view_if_exists(self._cr, 'budget_expense_monthly_report')
        self._cr.execute("""
            CREATE OR REPLACE VIEW budget_expense_monthly_report AS (
                 SELECT
                    row_number() OVER () AS id,
                    m.month_number,
                    m.month_name,
                    COALESCE(b.total_budget, 0) AS total_budget,
                    COALESCE(t.total_expense, 0) AS total_expense,
					COALESCE(b.tahunanggaran, t.tahunanggaran,0) AS tahunanggaran
					
                FROM
                    (SELECT
                            1 AS month_number, '01-Jan' AS month_name
                        UNION ALL SELECT 2, '02-Feb'
                        UNION ALL SELECT 3, '03-Mar'
                        UNION ALL SELECT 4, '04-Apr'
                        UNION ALL SELECT 5, '05-May'
                        UNION ALL SELECT 6, '06-Jun'
                        UNION ALL SELECT 7, '07-Jul'
                        UNION ALL SELECT 8, '08-Aug'
                        UNION ALL SELECT 9, '09-Sep'
                        UNION ALL SELECT 10, '10-Oct'
                        UNION ALL SELECT 11, '11-Nov'
                        UNION ALL SELECT 12, '12-Dec') AS m
                LEFT JOIN (
                    SELECT
                        EXTRACT(MONTH FROM b.date_of_fiscal) AS month_number,
						EXTRACT(YEAR FROM b.date_of_fiscal) AS tahunanggaran,
                        SUM(b.nilai_anggaran) AS total_budget
                    FROM
                         detail_anggaran_perbulan b
                    GROUP BY
                        EXTRACT(MONTH FROM b.date_of_fiscal), EXTRACT(YEAR FROM b.date_of_fiscal)
                ) b ON m.month_number = b.month_number
                LEFT JOIN (
                    SELECT
                        EXTRACT(MONTH FROM t.transaction_date) AS month_number,
						EXTRACT(YEAR FROM t.transaction_date) AS tahunanggaran,
                        SUM(t.transaction_subtotal) AS total_expense
                    FROM
                        detail_trans_perbudget t
                    GROUP BY
                        EXTRACT(MONTH FROM t.transaction_date), EXTRACT(YEAR FROM t.transaction_date)
                ) t ON m.month_number = t.month_number
                WHERE COALESCE(b.tahunanggaran, t.tahunanggaran, 0) <> 0
                ORDER BY
                    COALESCE(b.tahunanggaran, t.tahunanggaran), m.month_number
            )
        """)
class ExpenseAmountPerPillar(models.Model):
    _name = 'expense.report.perpillar'
    _description = 'Expense Amount Per Pillar Per Year'
    _auto = False

    pillarname = fields.Char(string='Pillar Name')
    fiscal_year = fields.Char(string='Fiscal Year')
    currency_id = fields.Many2one('res.currency',  string='Currency', default=lambda self: self.env.company.currency_id)
    jmlsubtotal = fields.Monetary(string='Total Expenses',currency_field='currency_id')
    seq_number = fields.Integer(string="Sequence Number")
    chart_label = fields.Char(string="Chart Label")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.pillarname))  # or any other meaningful field
        return result
    def init(self):
        tools.drop_view_if_exists(self._cr, 'expense_report_perpillar')
        self._cr.execute("""
                CREATE OR REPLACE VIEW expense_report_perpillar AS (
                   SELECT 
                     ROW_NUMBER() OVER (ORDER BY p.sequence) AS id,
                     p.nama_pillar AS pillarname,
                     SUM(COALESCE(d.transaction_subtotal,0)) AS jmlsubtotal,
                     p.sequence AS seq_number,
                     COALESCE(i.tahun_anggaran, CAST(EXTRACT(YEAR FROM CURRENT_DATE) AS VARCHAR)) AS fiscal_year,
                     ROW_NUMBER() OVER (ORDER BY p.sequence)  || ' - ' || p.nama_pillar AS chart_label,
                     d.currency_id
                     
                    FROM pillar_group p
                    LEFT JOIN detail_trans_perbudget d ON p.nama_pillar = d.namapillar
                    LEFT JOIN informasi_perpillar i ON p.id = i.kode_pillar
                    GROUP BY p.nama_pillar,  p.sequence, i.tahun_anggaran, d.currency_id
                    HAVING SUM(COALESCE(d.transaction_subtotal, 0)) > 0
                    ORDER BY p.sequence ASC
                )
        """)
class ExpenseAmountPerProgram(models.Model):
    _name = 'expense.report.perprogram'
    _description = 'Expense Amount Per Program'
    _auto = False

    program_code = fields.Integer(string="Program Code")
    label_grafik = fields.Text(string="Program Name")
    tahun_budget = fields.Char(string="Tahun Budget")
    nama_pillar = fields.Char(string="Nama Pillar")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    total_transaction = fields.Monetary(string='Total Transaction', currency_field='currency_id')
    total_payment = fields.Monetary(string='Total Payment', currency_field='currency_id')

    def init(self):
        tools.drop_view_if_exists(self._cr, 'expense_report_perprogram')
        self._cr.execute("""
             CREATE OR REPLACE VIEW expense_report_perprogram AS (
                    SELECT 
                        row_number() OVER () AS id,
                        x.namapillar || ' - ' || x.keterangan_budget AS label_grafik,
                        d.kodeprogram AS program_code,
                        x.tahun_budget AS tahun_budget,
                        x.namapillar AS nama_pillar,
                        x.currency_id,
                        COALESCE(d.transaction_subtotal,0) AS total_transaction,
                        COALESCE(SUM(y.val_payment),0) AS total_payment
                    FROM detail_trans_perbudget d
                    LEFT JOIN detail_anggaran_perbulan x ON d.kodeprogram = x.id
                    LEFT JOIN detail_payment y ON d.detail_trans_id  = y.transid
                    GROUP BY d.kodeprogram,x.keterangan_budget,COALESCE(d.transaction_subtotal,0),x.tahun_budget,x.namapillar,x.currency_id
             )
        """)
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.label_grafik))  # or any other meaningful field
        return result















