from odoo import api, fields, models, _
from datetime import datetime

class BusdevMonitoringProjectInv(models.Model):
    _name = "busdev.monitoring.project"
    _description = "Model for BUSDEV Monitoring Project"

    name = fields.Char(string="Nama Investasi", required=True)
    pic = fields.Many2one("res.users", string="PIC", required=True)
    start_date = fields.Date(string="Tanggal Mulai Pekerjaan", required=True)
    due_date = fields.Date(string="Due Date")
    notes = fields.Text(string="Keterangan")
    satuan_kerja = fields.Many2one("hr.department", string="Satuan Kerja", required=True)
    kepala_satker = fields.Many2one("hr.employee", string="Kepala Satker", readonly=True, store=True)
    status_project = fields.Selection([
        ("inisiasi", "Inisiasi"),
        ("sedang_berjalan", "Sedang Berjalan"),
        ("selesai", "Selesai"),
    ], string="Status", required=True)
    klasifikasi = fields.Selection([
        ("capex", "CAPEX"),
        ("opex", "OPEX"),
    ], string="Klasifikasi", required=True)
    nama_vendor = fields.Many2one("res.partner", string="Nama Vendor")
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        readonly=True
    )
    budget_id = fields.Many2one(
        "crossovered.budget",
        string="Cost Center",
        check_company=True,
        domain="[('company_id', 'in', [company_id, False]), ('department_id', '=', [satuan_kerja, False])]",
    )
    budget_line_id = fields.Many2one(
        "crossovered.budget.lines",  # Note: it's "budget.lines", not "budget.line"
        string="Budget",
        domain="[('crossovered_budget_id', '=', budget_id)]",
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        related="budget_line_id.currency_id"
    )
    planned_amount = fields.Monetary(string="Planned Amount", related="budget_line_id.planned_amount")
    used_amount = fields.Monetary(string="Used Amount", compute="_compute_used_amount", readonly=True)
    percentage = fields.Integer(string="Penggunaan Anggaran %", compute="_compute_percentage", readonly=True)

    detail_items = fields.One2many("busdev.monitoring.project.detail", "id_project", string="Progres")
    list_dokumen = fields.One2many("busdev.project.document", "id_project_d", string="Dokumen")
    list_pembayaran = fields.One2many("busdev.project.payment", "id_project_p", string="Dokumen")

    approval_1 = fields.Many2one("res.users", string="Approved By")
    approval_date_1 = fields.Date(string="Approved At")
    state = fields.Selection([
        ("draft", "Draft"),
        ("approved", "Approved")
    ], string="Status", default="draft")

    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', readonly=True, tracking=True)
    existing_status = fields.Char(string="Current Status", readonly=True, tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", readonly=True, tracking=True)
    button_visible = fields.Boolean(string="BVS", compute='_compute_button_visibility', store=False)

    @api.model
    def create(self, vals):
        # UAC Find the configured approval route for the current model for new document creation
        config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
        if config:
            vals['approval_route_id'] = config.approval_route_id.id
            next_step = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)],
                                                                       limit=1).approval_route_id.step_ids.sorted(
                key='sequence')[0]
            vals['current_step_id'] = next_step.id
            vals['state'] = 'draft'
            vals['existing_status'] = 'Draft'
            vals['pending_approval_by'] = next_step.user_id.id
            vals['upcoming_status'] = next_step.id

        return super(BusdevMonitoringProjectInv, self).create(vals)

    def _compute_button_visibility(self):
        for record in self:
            # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.current_step_id.user_id.id == self.env.user.id)
            else:
                record.button_visible = False

    def action_approval_1(self):
        self.state = "approved"
        self.approval_1 = self.env.user.id
        self.approval_date_1 = datetime.today()

    @api.onchange('satuan_kerja')
    def _get_satker_manager(self):
        for record in self:
            record.kepala_satker = record.satuan_kerja.manager_id

    @api.depends('list_pembayaran.payment')
    def _compute_used_amount(self):
        for record in self:
            record.used_amount = sum(record.list_pembayaran.mapped('payment'))

    @api.depends('planned_amount', 'used_amount')
    def _compute_percentage(self):
        for record in self:
            if record.planned_amount == 0 or record.used_amount == 0:
                record.percentage = 0
            else:
                record.percentage = (record.used_amount / record.planned_amount) * 100

class BusdevMonitoringProjectDetails(models.Model):
    _name = "busdev.monitoring.project.detail"
    _description = "Model for BUSDEV Monitoring Project Progress Item"

    date = fields.Date(string="Tanggal", required=True)
    progress = fields.Text(string="Deskripsi Progres", required=True)
    kriteria = fields.Selection([
        ("rutin", "Rutin"),
        ("non_rutin", "Non Rutin")
    ], string="Kriteria", required=True)
    id_project = fields.Many2one("busdev.monitoring.project", string="ID Project")

class BusdevProjectDocument(models.Model):
    _name = "busdev.project.document"
    _description = "Model for BUSDEV Project Document"

    name = fields.Char(string="Nama Dokumen", required=True)
    file = fields.Binary(string="Soft Copy", required=True)
    upload_date = fields.Date(string="Tanggal")
    id_project_d = fields.Many2one("busdev.monitoring.project", string="ID Project")

class BusdevProjectPayment(models.Model):
    _name = "busdev.project.payment"
    _description = "Model for BUSDEV Project Payment"

    termin = fields.Char(string="Termin", required=True)
    plan_date = fields.Date(string="Plan Date", required=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        related="id_project_p.budget_line_id.currency_id"
    )
    plan = fields.Monetary(string="Plan", required=True)
    payment = fields.Monetary(string="Actual", required=True)
    actual_date = fields.Date(string="Actual Payment Date")

    id_project_p = fields.Many2one("busdev.monitoring.project", string="ID Project")