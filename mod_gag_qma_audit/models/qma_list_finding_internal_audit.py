from odoo import api, models, fields, _

class QmaListFindingInternalAudit(models.Model):
    _name = "qma.list.finding.internal.audit"
    _description = "Model for QMA & Audit List Finding Internal Audit"

    divisi = fields.Char(string="Divisi", required=True)
    ptp = fields.Integer(string="PTP")
    temuan = fields.Text(string="Temuan", required=True)
    internal_audit = fields.Char(string="Internal Audit", required=True)
    prosedur = fields.Char(string="Prosedur")
    root_cause = fields.Text(string="Root Cause")
    tindakan_perbaikan = fields.Text(string="Tindakan Perbaikan")
    kriteria = fields.Char(string="Kriteria Penilaian / Klausul")
    state = fields.Selection([
        ("open", "Open"),
        ("close", "Close"),
    ], string="Status", default="open")
    date_close = fields.Date(string="Date Closing")
    deadline_close = fields.Date(string="Dateline Close Findings")
    catatan = fields.Text(string="Catatan Hasil IA")