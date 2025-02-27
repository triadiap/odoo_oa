from odoo import api, models, fields, _

class QmaInternalAudit(models.Model):
    _name = "qma.internal.audit"
    _description = "QMA Internal Audit"

    code = fields.Char(string="IA Code")
    area = fields.Char(string="Area Audit", required=True)
    audit_date = fields.Date(string="Tanggal", required=True)
    tim_no = fields.Char(string="Tim", required=True)
    audit_kriteria = fields.Char(string="Audit Kriteria", required=True)
    auditee = fields.Many2one("hr.department", string="Auditee", required=True)
    ref_doc = fields.Char(string="Referensi Dokumen", required=True)
    standard_ref = fields.Char(string="Standard Ref.", required=True)

    audit_issue = fields.Text(string="Penjelasan Ketidaksesuaian / Peluang Perbaikan", required=True)
    issue_auditee = fields.Many2one('hr.employee', string="Auditee", required=True)
    issue_auditor = fields.Many2one('hr.employee', string="Auditor", required=True)

    root_cause = fields.Text(string="Akar Masalah dan Rencana Tindakan Korektif", required=True)
    root_cause_auditee = fields.Many2one('hr.employee', string="Auditee", required=True)
    root_cause_auditor = fields.Many2one('hr.employee', string="Auditor", required=True)

    corrective = fields.Text(string="Bukti Tindakan Perbaikan dan Komentar Verifikator")
    verifikator = fields.Many2one("qma.internal.audit.auditor", string="Verifikator", domain="[('id_ia_main', '=', id)]")
    verification_date = fields.Date(string="Tanggal Penyelesaian")
    status = fields.Selection([
        ("Berulang", "Berulang"),
        ("Ditutup", "Ditutup")
    ], string="Status Tindakan Perbaikan")
    file = fields.Binary(string="File / Dokumen")
    photo = fields.Binary(string="Foto", attachment=True)
    link = fields.Char(string="Link")

    auditor_type = fields.Selection([
        ("internal", "Internal"),
        ("external", "Eksternal"),
    ], string="Kelompok Auditor", default="internal")
    auditor = fields.One2many("qma.internal.audit.auditor", "id_ia_main", string="Auditor")
    ex_auditor = fields.One2many("qma.internal.audit.external.auditor", "id_ia_main", string="External Auditor")

    def name_get(self):
        result = []
        for record in self:
            display_name = f" Code {record.code} : {record.area} - {record.audit_date}"  # Custom display
            result.append((record.id, display_name))
        return result

class QmaInternalAuditor(models.Model):
    _name = "qma.internal.audit.auditor"
    _description = "QMA IA Auditor"

    name = fields.Many2one("res.users", string="Auditor", required=True)

    id_ia_main = fields.Many2one("qma.internal.audit", string="ID IA Main")

class QmaExternalAuditor(models.Model):
    _name = "qma.internal.audit.external.auditor"
    _description = "QMA IA External Auditor"

    name = fields.Char(string="Auditor", required=True)

    id_ia_main = fields.Many2one("qma.internal.audit", string="ID IA Main")