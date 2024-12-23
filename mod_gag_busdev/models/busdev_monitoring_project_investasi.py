from odoo import api, fields, models, _

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
        domain="[('company_id', 'in', [company_id, False]), ('department_id', '=', [satuan_kerja, False])]"
    )
    budget_line_id = fields.Many2one(
        "crossovered.budget.lines",  # Note: it's "budget.lines", not "budget.line"
        string="Budget",
        domain="[('crossovered_budget_id', '=', budget_id)]"
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
    id_project_d = fields.Many2one("busdev.monitoring.project", string="ID Project")

class BusdevProjectPayment(models.Model):
    _name = "busdev.project.payment"
    _description = "Model for BUSDEV Project Payment"

    termin = fields.Char(string="Termin", required=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        related="id_project_p.budget_line_id.currency_id"
    )
    payment = fields.Monetary(string="Jumlah", required=True)

    id_project_p = fields.Many2one("busdev.monitoring.project", string="ID Project")