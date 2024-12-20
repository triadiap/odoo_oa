from odoo import api, models, fields, _
from datetime import datetime

class QmaFormAudit(models.Model):
    _name = "qma.form.audit"
    _description = "Model for Form Audit 5R"

    area = fields.Char(string="Area / Kantor", required=True)
    def _get_months(self):
        return [
            ('01', 'January'), ('02', 'February'), ('03', 'March'),
            ('04', 'April'), ('05', 'May'), ('06', 'June'),
            ('07', 'July'), ('08', 'August'), ('09', 'September'),
            ('10', 'October'), ('11', 'November'), ('12', 'December')
        ]

    def _get_years(self):
        current_year = datetime.now().year
        return [(str(year), str(year)) for year in range(current_year - 1, current_year + 1)]

    month = fields.Selection(selection=_get_months, string="Bulan", required=True)
    year = fields.Selection(selection=_get_years, string="Tahun", required=True)
    datetime = fields.Datetime(string="Tanggal & Waktu Inspeksi", required=True)

    notes = fields.Text(string="Catatan Verifikator")

    verif_one = fields.Many2one("hr.employee", string="Verifikator 1")
    verif_two = fields.Many2one("hr.employee", string="Verifikator 2")

    ringkas_1 = fields.Many2one("qma.master.score", string="1. Makanan ", required=True)
    note_ringkas_1 = fields.Char(string="Catatan")

    ringkas_2 = fields.Many2one("qma.master.score", string="2. Komponen / Bahan ", required=True)
    note_ringkas_2 = fields.Char(string="Catatan")

    ringkas_3 = fields.Many2one("qma.master.score", string="3. Peralatan Kerja ", required=True)
    note_ringkas_3 = fields.Char(string="Catatan")

    ringkas_4 = fields.Many2one("qma.master.score", string="4. Dokumen ", required=True)
    note_ringkas_4 = fields.Char(string="Catatan")

    ringkas_5 = fields.Many2one("qma.master.score", string="5. Pengendalian Visual ", required=True)
    note_ringkas_5 = fields.Char(string="Catatan")

    ts_ringkas = fields.Integer(string="Total Score Ringkas", readonly=True, store=True, compute="_compute_ts_ringkas")

    rapi_1 = fields.Many2one("qma.master.score", string="6. Meja Kerja ", required=True)
    note_rapi_1 = fields.Char(string="Catatan")

    rapi_2 = fields.Many2one("qma.master.score", string="7. Alat Tulis Kantor (ATK) ", required=True)
    note_rapi_2 = fields.Char(string="Catatan")

    rapi_3 = fields.Many2one("qma.master.score", string="8. Peralatan ", required=True)
    note_rapi_3 = fields.Char(string="Catatan")

    rapi_4 = fields.Many2one("qma.master.score", string="9. Kursi ", required=True)
    note_rapi_4 = fields.Char(string="Catatan")

    rapi_5 = fields.Many2one("qma.master.score", string="10. P3K ", required=True)
    note_rapi_5 = fields.Char(string="Catatan")

    ts_rapi = fields.Integer(string="Total Score Rapi", readonly=True, store=True, compute="_compute_ts_rapi")

    resik_1 = fields.Many2one("qma.master.score", string="11. Lantai ", required=True)
    note_resik_1 = fields.Char(string="Catatan")

    resik_2 = fields.Many2one("qma.master.score", string="12. Printer / Peralatan Kerja ", required=True)
    note_resik_2 = fields.Char(string="Catatan")

    resik_3 = fields.Many2one("qma.master.score", string="13. Tempat Sampah ", required=True)
    note_resik_3 = fields.Char(string="Catatan")

    resik_4 = fields.Many2one("qma.master.score", string="14. Peralatan Kebersihan ", required=True)
    note_resik_4 = fields.Char(string="Catatan")

    resik_5 = fields.Many2one("qma.master.score", string="15. Kebersihan ", required=True)
    note_resik_5 = fields.Char(string="Catatan")

    ts_resik = fields.Integer(string="Total Score Resik", readonly=True, store=True, compute="_compute_ts_resik")

    rawat_1 = fields.Many2one("qma.master.score", string="16. Peralatan Kerja ", required=True)
    note_rawat_1 = fields.Char(string="Catatan")

    rawat_2 = fields.Many2one("qma.master.score", string="17. Berpakaian ", required=True)
    note_rawat_2 = fields.Char(string="Catatan")

    rawat_3 = fields.Many2one("qma.master.score", string="18. Kondisi Lingkungan ", required=True)
    note_rawat_3 = fields.Char(string="Catatan")

    rawat_4 = fields.Many2one("qma.master.score", string="19. Pengumuman Tertulis ", required=True)
    note_rawat_4 = fields.Char(string="Catatan")

    rawat_5 = fields.Many2one("qma.master.score", string="20. AC, Lampu, APAR ", required=True)
    note_rawat_5 = fields.Char(string="Catatan")

    ts_rawat = fields.Integer(string="Total Score Rawat", readonly=True, store=True, compute="_compute_ts_rawat")

    rajin_1 = fields.Many2one("qma.master.score", string="21. Peraturan Perusahaan ", required=True)
    note_rajin_1 = fields.Char(string="Catatan")

    rajin_2 = fields.Many2one("qma.master.score", string="22. Absensi ", required=True)
    note_rajin_2 = fields.Char(string="Catatan")

    rajin_3 = fields.Many2one("qma.master.score", string="23. Hub. Antar Pekerja ", required=True)
    note_rajin_3 = fields.Char(string="Catatan")

    rajin_4 = fields.Many2one("qma.master.score", string="24. Jobdesk ", required=True)
    note_rajin_4 = fields.Char(string="Catatan")

    rajin_5 = fields.Many2one("qma.master.score", string="25. SOP ", required=True)
    note_rajin_5 = fields.Char(string="Catatan")

    ts_rajin = fields.Integer(string="Total Score Rajin", readonly=True, store=True, compute="_compute_ts_rajin")

    ts_all = fields.Integer(string="Total Score Keseluruhan", readonly=True, store=True, compute="_compute_ts_all")

    score_legend = fields.Html(string="Score Legend", compute='_compute_score_legend', store=False, readonly=True)

    @api.depends('area')
    def _compute_score_legend(self):
        for record in self:
            scores = self.env['qma.master.score'].search([])
            legend = "<br/>".join([f"{score.name} -- {score.notes}" for score in scores])
            record.score_legend = legend
            return record

    @api.depends('ringkas_1', 'ringkas_2', 'ringkas_3', 'ringkas_4', 'ringkas_5')
    def _compute_ts_ringkas(self):
        for record in self:
            total_score = sum(int(getattr(record, f'ringkas_{i}').name or 0) for i in range(1, 6))
            record.ts_ringkas = total_score

    @api.depends('rapi_1', 'rapi_2', 'rapi_3', 'rapi_4', 'rapi_5')
    def _compute_ts_rapi(self):
        for record in self:
            total_score = sum(int(getattr(record, f'rapi_{i}').name or 0) for i in range(1, 6))
            record.ts_rapi = total_score

    @api.depends('resik_1', 'resik_2', 'resik_3', 'resik_4', 'resik_5')
    def _compute_ts_resik(self):
        for record in self:
            total_score = sum(int(getattr(record, f'resik_{i}').name or 0) for i in range(1, 6))
            record.ts_resik = total_score

    @api.depends('rawat_1', 'rawat_2', 'rawat_3', 'rawat_4', 'rawat_5')
    def _compute_ts_rawat(self):
        for record in self:
            total_score = sum(int(getattr(record, f'rawat_{i}').name or 0) for i in range(1, 6))
            record.ts_rawat = total_score

    @api.depends('rajin_1', 'rajin_2', 'rajin_3', 'rajin_4', 'rajin_5')
    def _compute_ts_rajin(self):
        for record in self:
            total_score = sum(int(getattr(record, f'rajin_{i}').name or 0) for i in range(1, 6))
            record.ts_rajin = total_score

    @api.depends('ts_ringkas', 'ts_rapi', 'ts_resik', 'ts_rawat', 'ts_rajin')
    def _compute_ts_all(self):
        for record in self:
            total_score = record.ts_ringkas + record.ts_rapi + record.ts_resik + record.ts_rawat + record.ts_rajin
            record.ts_all = total_score
