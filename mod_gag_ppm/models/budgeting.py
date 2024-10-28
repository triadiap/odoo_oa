# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class InputDataBudgeting(models.Model):

    _name="informasi.perpillar"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description="Data Informasi Responsibility Budget Per Pillar"


    name = fields.Char(string="Budget Name", required=True, tracking=True)
    kode_pillar = fields.Many2one('pillar.group', string="Pillar Name", required=True, tracking=True)
    status_budget = fields.Many2one('status.kegiatan',string="Budget Status", required=True, tracking=True, default=lambda self: self.env['status.kegiatan'].search([], limit=1))
    tahun_anggaran = fields.Selection(selection='_get_years', string='Year', default=lambda self: str(datetime.now().year), tracking=True)
    id_anggaran = fields.One2many('detail.anggaran.perbulan', 'anggaran_id', string="Lines")
    keterangan_anggaran = fields.Text(string="Notes", tracking=True)
    totalbudget_sum = fields.Char(string="Total Budget Count", compute='_compute_budget_sum')
    totalexpense_sum = fields.Char(string="Total Expense Count", compute='_compute_expense_sum')
    totalbalance_sum = fields.Char(string="Balance", compute='_compute_balance_sum')
    sum_total_budget= fields.Float(string="Total Budget", compute='_compute_total_budget', store=True)
    budgetgrandtotal= fields.Char(string="Grand Total", compute='_compute_grand_total')
    # ------------------Ini Connect ke Module UAC ------------------------------------------#
    approval_route_id = fields.Many2one('approval.route', string='Approval Route',readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step',readonly=True,tracking=True)
    existing_status = fields.Char(string="Current Status", readonly=True,tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status',readonly=True,tracking=True)
    pending_approval_by = fields.Many2one('res.users',string="Pending Approval By", readonly=True,tracking=True)
    button_visible = fields.Boolean(compute='_compute_button_visibility', store=False)
    # -------------------------------------------------------------------------------------#


    budget_month = fields.Selection([
        ('1', 'Januari'),
        ('2', 'Februari'),
        ('3', 'Maret'),
        ('4', 'April'),
        ('5', 'Mei'),
        ('6', 'Juni'),
        ('7', 'Juli'),
        ('8', 'Agustus'),
        ('9', 'September'),
        ('10', 'Oktober'),
        ('11', 'November'),
        ('12', 'Desember'),
    ], string="Month", required=True, default='1', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approval_process', 'Approval Process'),
        ('approve','Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancelled')
    ], default="draft", string="Status", tracking=True)

    @property
    def uid(self):
        return self.env.uid
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
        self._compute_total_budget()
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
        self._compute_total_budget()

    def action_done(self):
        self.state = 'done'
        self._compute_total_budget()

    def action_draft(self):
        self.state = 'draft'
        self._compute_total_budget()

    def action_cancel(self):
        self.state = 'cancel'
        self._compute_total_budget()

    budget_id = fields.Char(string = "Budget ID", readonly=True, copy=False, default='New')
    fiscal_date = fields.Date(string='Month Date')



    @api.onchange('tahun_anggaran', 'budget_month')
    def _onchange_month_number(self):
        try:
            month_number = int(self.budget_month)
            year = int(self.tahun_anggaran)
            if 1 <= month_number <= 12:
                self.fiscal_date = datetime(year, month_number, 1).date()
            else:
                self.fiscal_date = False
        except ValueError:
            self.fiscal_date = False



    def _get_years(self):
        current_year = datetime.now().year
        year_range = 10  # Number of years to generate
        years = [(str(year), str(year)) for year in range(current_year, current_year + year_range)]
        return years


    @api.model
    def create(self, vals):
        if vals.get('budget_id','New') == 'New' :
            year = vals['tahun_anggaran']
            month = vals['budget_month']
            # Fetch the related prefix code from pillar.group table
            pillar = self.env['pillar.group'].browse(vals.get('kode_pillar'))
            #Custom budget code using pillar prefix code
            prefix_code = pillar.pillar_prefix.upper() if pillar else 'XXX'
            # Generate the sequence number
            sequence = self.env['ir.sequence'].next_by_code('informasi.perpillar') or '00000'
            # Combine them into the final name
            vals['budget_id'] = f'{prefix_code}-{sequence}-{month}-{year}'
            self._compute_total_budget()

        # UAC Find the configured approval route for the current model for new document creation
        config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
        if config:
            vals['approval_route_id'] = config.approval_route_id.id

        return super(InputDataBudgeting, self).create(vals)
        #-----------------------------------------------------------------------------------#

    # Approval button visibility configuration by approval workflow's user ID and need to compared with current user ID logged in
    # if match then set as True, if not then set as False
    def _compute_button_visibility(self):
        for record in self:
            # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.pending_approval_by.id == self.env.user.id)
            else:
                record.button_visible = False
    def name_get(self):
        result = []
        for record in self:
            name = f"({record.budget_id}) - {record.name}"
            result.append((record.id, name))  # or any other meaningful field
        return result

    def _compute_expense_sum(self):
        for rec in self:
                totalexpense_sum = self.env['transaksi.anggaran'].search([('kode_anggaran','=',rec.id)])
                findtransactioncodeby_BudgetID = totalexpense_sum.id
                for record in self:
                    totalexpense_sum = self.env['detail.trans.perbudget'].search([('detail_trans_id','=',findtransactioncodeby_BudgetID)]).mapped('transaction_subtotal')
                    record.totalexpense_sum =  f"Rp {float(sum(totalexpense_sum)):,.2f}"

    def _compute_total_budget(self):
        for rec in self:
            sum_total_budget = self.env['detail.anggaran.perbulan'].search([('anggaran_id','=',rec.id)]).mapped('nilai_anggaran')
            rec.sum_total_budget = float(sum(sum_total_budget))

    def _compute_budget_sum(self):
        for rec in self:
            totalbudget_sum = self.env['detail.anggaran.perbulan'].search([('anggaran_id','=',rec.id)]).mapped('nilai_anggaran')
            rec.totalbudget_sum = f"Rp {float(sum(totalbudget_sum)):,.2f}"
    def hitungtotalbudget(self):
        for rec in self:
            totalbudget = float(sum(self.env['detail.anggaran.perbulan'].search([('anggaran_id','=',rec.id)]).mapped('nilai_anggaran')))
        return totalbudget

    def hitungtransaksibudget(self):
        for rec in self:
            totalexpense_sum = self.env['transaksi.anggaran'].search([('kode_anggaran', '=', rec.id)])
            findtransactioncodeby_BudgetID = totalexpense_sum.id
            totalexpense = float(sum(self.env['detail.trans.perbudget'].search([('detail_trans_id', '=', findtransactioncodeby_BudgetID)]).mapped('transaction_subtotal')))
        return totalexpense

    def _compute_balance_sum(self):
        for rec in self:
            rec.totalbalance_sum = f"Rp {(self.hitungtotalbudget() - self.hitungtransaksibudget()):,.2f}"
    def _compute_grand_total(self):
        for rec in self:
            rec.budgetgrandtotal = f"Total Budget : Rp {self.hitungtotalbudget():,.2f}"

    def action_open_budgets(self):
        print("Test")

class InputDetailAnggaranPerBulanPerPillar(models.Model):

    _name ="detail.anggaran.perbulan"
    _description = "Detail Informasi Anggaran Perbulan Per Pillar"
    anggaran_id = fields.Many2one('informasi.perpillar', string="Parent")
    currency_id = fields.Many2one('res.currency', string='Currency')
    nilai_anggaran = fields.Monetary(string='Budget Amount', help="Input Your Monhtly Budget", currency_field='currency_id', required=True)
    keterangan_budget = fields.Text(string="Program")
    activity_start_date = fields.Date(string='Start Date')
    activity_end_date = fields.Date(string='End Date')
    duration = fields.Integer(string='Duration (Days)', compute='_compute_duration', store=True)
    location_ids = fields.Many2many("daftar.lokasi", string="Locations")
    budget_status = fields.Many2one(related="anggaran_id.status_budget", string="Status")
    budget_activity_type = fields.Many2one("jenis.kegiatan", string="Activity Type", required=True)
    budget_activity_category = fields.Many2one("kategori.kegiatan", string="Category", required=True)
    budget_chartofaccounts = fields.Many2one("tabel.coa", string="Chart Of Account(COA)", required=True)
    namapillar = fields.Char(related="anggaran_id.kode_pillar.nama_pillar", string="Pillar Name", store=True)
    budgetid = fields.Char(related="anggaran_id.budget_id", string="Budget ID")
    budgetname = fields.Char(related="anggaran_id.name", string="Budget ID")
    total_expenses = fields.Monetary(string='Total Expense', compute='_compute_total_expense_per_program')
    amount_balance = fields.Monetary(string='Balance Amount', compute='_compute_total_balance_per_program')
    percentage_of_expense = fields.Float(string='% of Expense', compute='_compute_percentage_of_expense')
    percentage_of_balance = fields.Float(string='% of Balance', compute='_compute_percentage_of_balance')
    tahun_budget = fields.Selection(string='Year',related='anggaran_id.tahun_anggaran',store=True)
    date_of_fiscal = fields.Date(string='Month', related='anggaran_id.fiscal_date',store=True)


    @api.depends('nilai_anggaran')
    def _compute_percentage_of_balance(self):
        for rec in self:
            if rec.nilai_anggaran:
                getprogramcode = self.env['transaksi.anggaran'].search([('program_code', '=', rec.id)])
                prog_code = getprogramcode.id
                total_exp = sum(self.env['detail.trans.perbudget'].search([('detail_trans_id', '=', prog_code)]).mapped(
                    'transaction_subtotal'))
                balance = rec.nilai_anggaran - total_exp
                rec.percentage_of_balance = float(balance / rec.nilai_anggaran * 100)
    @api.depends('nilai_anggaran')
    def _compute_percentage_of_expense(self):
        for rec in self:
            if rec.nilai_anggaran:
                getprogramcode = self.env['transaksi.anggaran'].search([('program_code', '=', rec.id)])
                prog_code = getprogramcode.id
                total_exp = sum(self.env['detail.trans.perbudget'].search([('detail_trans_id', '=', prog_code)]).mapped(
                    'transaction_subtotal'))
                rec.percentage_of_expense  = float(total_exp / rec.nilai_anggaran * 100)
    @api.depends('nilai_anggaran')
    def _compute_total_balance_per_program(self):
        for rec in self:
            if rec.nilai_anggaran:
                getprogramcode = self.env['transaksi.anggaran'].search([('program_code','=',rec.id)])
                prog_code = getprogramcode.id
                total_exp = sum(self.env['detail.trans.perbudget'].search([('detail_trans_id', '=', prog_code)]).mapped('transaction_subtotal'))
                balance = rec.nilai_anggaran - total_exp
                rec.amount_balance = balance
    @api.depends('nilai_anggaran')
    def _compute_total_expense_per_program(self):
        for rec in self:
            if rec.nilai_anggaran:
                findprogramcode = self.env['transaksi.anggaran'].search([('program_code','=',rec.id)])
                programcode = findprogramcode.id
                totalexpenses = sum(self.env['detail.trans.perbudget'].search([('detail_trans_id', '=', programcode)]).mapped('transaction_subtotal'))
                rec.total_expenses = totalexpenses

    @api.depends('activity_start_date', 'activity_end_date')
    def _compute_duration(self):
        for record in self:
            if record.activity_start_date and record.activity_end_date:
                activity_start_date = fields.Date.from_string(record.activity_start_date)
                activity_end_date = fields.Date.from_string(record.activity_end_date)
                record.duration = (activity_end_date - activity_start_date).days
            else:
                record.duration = 0
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.keterangan_budget}"
            result.append((record.id, name))  # or any other meaningful field
        return result



