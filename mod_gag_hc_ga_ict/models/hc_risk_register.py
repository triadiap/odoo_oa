from odoo import api, models, fields, _
from datetime import datetime

class HcRiskRegister(models.Model):
    _name = "hc.risk.regist"
    _description = "Model for HC Risk Register"

    def _get_months(self):
        return [
            ('01', 'Januari'), ('02', 'Februari'), ('03', 'Maret'),
            ('04', 'April'), ('05', 'Mei'), ('06', 'Juni'),
            ('07', 'Juli'), ('08', 'Agustus'), ('09', 'September'),
            ('10', 'Oktober'), ('11', 'November'), ('12', 'Desember')
        ]

    def _get_years(self):
        current_year = datetime.now().year
        return [(str(year), str(year)) for year in range(current_year - 1, current_year + 2 )]

    def _get_dept_id(self):
        return self.env.user.employee_id.department_id.id

    month = fields.Selection(selection=_get_months, string="Bulan", required=True)
    year = fields.Selection(selection=_get_years, string="Tahun", required=True)
    department_id = fields.Many2one('hr.department', string="Satker", default=lambda self: self.env.user.employee_id.department_id.id)

    # Identifikasi Resiko
    sasaran_strategis = fields.Char(string="Sasaran Strategis", required=True)
    sasaran_kpi = fields.Char(string="Sasaran/KPI Unit Kerja")
    sasaran_mind_id = fields.Char(string="Sasaran/KPI MIND ID")
    tahapan = fields.Char(string="Tahapan Proses Bisnis")
    no_resiko = fields.Char(string="No. Resiko")
    kejadian_resiko = fields.Text(string="Kejadian Resiko")
    tipe_resiko = fields.Many2one("hc.master.risk.type", string="Tipe Resiko", required=True) # Change with master data tipe resiko
    tipe_resiko_kbumn = fields.Char(related="tipe_resiko.taksonomi", string="Tipe Resiko Sesuai Taksonomi KBUMN", readonly=True) # Change with related fields based on master data tipe resiko

    # Penilaian Resiko Inheren
    sumber_resiko = fields.Text(string="Sumber Penyebab Resiko")
    parameter = fields.Char(string="Parameter")
    t_green = fields.Char(string="Hijau")
    t_yellow = fields.Char(string="Kuning")
    t_red = fields.Char(string="Merah")
    penjelasan_dampak = fields.Char(string="Penjelasan Dampak Resiko (Kualitatif)")
    nilai_dampak = fields.Float(string="Nilai Dampak Resiko (Kuantitatif - IDR)")
    tingkat_resiko_l = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ],string="L")
    tingkat_resiko_d = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ],string="D")
    risk_level = fields.Integer(string="Risk Level (RL)", compute="_compute_rl", store=True)
    kuadran = fields.Char(string="Kuadran", readonly=True, compute="_get_kuadran", store=True) # Change with master data risk_level

    @api.depends('tingkat_resiko_l', 'tingkat_resiko_d')
    def _compute_rl(self):
        for record in self:
            risk_l = int(record.tingkat_resiko_l)
            risk_d = int(record.tingkat_resiko_d)
            risk_level = risk_l * risk_d
            record.risk_level = risk_level

    @api.depends('risk_level')
    def _get_kuadran(self):
        for record in self:
            kuadran = self.env['hc.master.risk.level'].search([('risk_level', '=', record.risk_level)], limit=1)
            if (kuadran):
                record.kuadran = kuadran.kuadran
            else:
                record.kuadran = ""

    # Penilaian Kontrol Eksisting dan Current Risk
    kontrol_proses = fields.Text(string="Kontrol Proses Bisnis Yang Ada Saat Ini")
    sifat_kontrol = fields.Selection([
        ("L", "Likelihood"),
        ("D", "Impact"),
        ("LD", "Likelihood & Impact")
    ], string="Sifat Kontrol")
    pn_desain = fields.Selection([
        ("effective", "Effective"),
        ("partially_effective", "Partially Effective"),
        ("non_effective", "Non Effective"),
        ("belum_ada", "Belum Ada Kontrol")
    ],string="Penilaian Kontrol Desain")
    pn_implementasi = fields.Selection([
        ("effective", "Effective"),
        ("partially_effective", "Partially Effective"),
        ("non_effective", "Non Effective"),
        ("belum_ada", "Belum Ada Kontrol")
    ], string="Penilaian Kontrol Implementasi")
    current_tingkat_resiko_l = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ],string="L")
    current_tingkat_resiko_d = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ],string="D")
    current_risk_level = fields.Integer(string="Risk Level (RL)", compute="_compute_current_rl", store=True)
    current_kuadran = fields.Char(string="Kuadran", readonly=True, compute="_get_current_kuadran", store=True,)

    @api.depends('current_tingkat_resiko_l', 'current_tingkat_resiko_d')
    def _compute_current_rl(self):
        for record in self:
            risk_l = int(record.current_tingkat_resiko_l)
            risk_d = int(record.current_tingkat_resiko_d)
            risk_level = risk_l * risk_d
            record.current_risk_level = risk_level

    @api.depends('current_risk_level')
    def _get_current_kuadran(self):
        for record in self:
            kuadran = self.env['hc.master.risk.level'].search([('risk_level', '=', record.current_risk_level)], limit=1)
            if(kuadran):
                record.current_kuadran = kuadran.kuadran
            else:
                record.current_kuadran = ""

    # Rencana Mitigasi Resiko
    no_mitigasi = fields.Char(string="No. Mitigasi")
    rencana_mitigasi = fields.Text(string="Rencana Mitigasi")
    detail_aktivitas = fields.Text(string="Detail Aktivitas")
    deliverables = fields.Text(string="Deliverables")
    budget_cost = fields.Float(string="Budget Cost")
    due_date = fields.Date(string="Due Date")
    pic = fields.Char(string="PIC")
    residual_tingkat_resiko_l = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ],string="L")
    residual_tingkat_resiko_d = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ],string="D")
    residual_risk_level = fields.Integer(string="Risk Level (RL)", compute="_compute_residual_rl", readonly=True, store=True)
    residual_kuadran = fields.Char(string="Kuadran", compute="_get_residual_kuadran", readonly=True, store=True)

    @api.depends('residual_tingkat_resiko_l', 'residual_tingkat_resiko_d')
    def _compute_residual_rl(self):
        for record in self:
            risk_l = int(record.residual_tingkat_resiko_l)
            risk_d = int(record.residual_tingkat_resiko_d)
            risk_level = risk_l * risk_d
            record.residual_risk_level = risk_level

    @api.depends('residual_risk_level')
    def _get_residual_kuadran(self):
        for record in self:
            kuadran = self.env['hc.master.risk.level'].search([('risk_level', '=', record.residual_risk_level)], limit=1)
            if (kuadran):
                record.residual_kuadran = kuadran.kuadran
            else:
                record.residual_kuadran = ""

    monitoring = fields.One2many("hc.risk.regist.realisasi", "id_risk_register", string="Monitoring Realisasi")
    dokumen = fields.One2many("hc.risk.regist.doc", "id_risk_reg", string="Dokumen Pendukung")

    def name_get(self):
        result = []
        for record in self:
            display_name = f"{record.department_id.display_name} {record.month}-{record.year}"  # Custom display
            result.append((record.id, display_name))
        return result

class HcRiskRegistItem(models.Model):
    _name = "hc.risk.regist.realisasi"
    _description = "Model for Risk Register Monitoring Realisasi"

    # Monitoring Realisasi
    progress_mitigasi = fields.Text(string="Progress Mitigasi")
    status_update = fields.Char(string="Status Update")
    progress_info = fields.Text(string="Progress Information")
    realisasi_anggaran = fields.Float(string="Realisasi Anggaran Mitigasi")
    nilai_aktual = fields.Float(string="Nilai Aktual")
    status = fields.Char(string="Status")
    p_sisa_dampak_resiko = fields.Text(string="Penjelasan Sisa Dampak Resiko (Kualitatif)")
    n_sisa_dampak_resiko = fields.Text(string="Nilai Sisa Dampak Resiko (Kuantitatif)")
    item_tingkat_resiko_l = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ],string="L")
    item_tingkat_resiko_d = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ],string="D")
    item_risk_level = fields.Integer(string="Risk Level (RL)", compute="_compute_item_rl", readonly=True, store=True)
    item_kuadran = fields.Char(string="Kuadran", compute="_get_item_kuadran", readonly=True, store=True)

    id_risk_register = fields.Many2one("hc.risk.regist", string="ID Risk Register")

    @api.depends('item_tingkat_resiko_l', 'item_tingkat_resiko_d')
    def _compute_item_rl(self):
        for record in self:
            risk_l = int(record.item_tingkat_resiko_l)
            risk_d = int(record.item_tingkat_resiko_d)
            risk_level = risk_l * risk_d
            record.item_risk_level = risk_level

    @api.depends('item_risk_level')
    def _get_item_kuadran(self):
        for record in self:
            kuadran = self.env['hc.master.risk.level'].search([('risk_level', '=', record.item_risk_level)], limit=1)
            if (kuadran):
                record.item_kuadran = kuadran.kuadran
            else:
                record.item_kuadran = ""

class HcRiskRegistDoc(models.Model):
    _name = "hc.risk.regist.doc"
    _description = "Model for HC Risk Register document"

    name = fields.Char(string="Nama Dokumen", required=True)
    file = fields.Binary(string="Dokumen", required=True)
    id_risk_reg = fields.Many2one('hc.risk.regist', string="ID Risk Regist")