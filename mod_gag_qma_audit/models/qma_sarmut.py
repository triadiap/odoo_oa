from odoo import api, models, fields, _
from datetime import datetime

class QmaSarmut(models.Model):
    _name = "qma.sarmut"
    _description = "QMA Sasaran Target Program Mutu K3 dan Lingkungan"

    department_id = fields.Many2one("hr.department", string="Satuan Kerja", required=True, default=lambda self:self.env.user.department_id.id)
    manager_dept_id = fields.Many2one("hr.employee", string="Kepala Satuan Kerja",related="department_id.manager_id", store=True, readonly=True)
    penilai = fields.Char(string="Penilai", required=True)
    nama_penilai = fields.Char(string="Nama Penilai", required=True)
    periode = fields.Char(string="Periode", required=True)
    year = fields.Selection(selection="_get_years", string="Tahun", required=True)

    sarmut_detail = fields.One2many("qma.sarmut.detail", "id_sarmut", string="Detail")

    def name_get(self):
        result = []
        for record in self:
            display_name = f"{record.department_id.name} - {record.periode} {record.year}"  # Custom display
            result.append((record.id, display_name))
        return result

    def _get_years(self):
        current_year = datetime.now().year
        return [(str(year), str(year)) for year in range(current_year - 1, current_year + 2 )]

class QmaSarmutDetail(models.Model):
    _name = "qma.sarmut.detail"
    _description = "QMA Sasaran Target Program Mutu K3 dan Lingkungan Details"

    sasaran = fields.Char(string="Sasaran", required=True)
    target = fields.Char(string="Target", required=True)
    proker = fields.Text(string="Program Kerja", required=True)
    penanggung_jawab = fields.Char(string="Penanggung Jawab")
    q1_jan = fields.Char(string="Q1 Jan")
    q1_feb = fields.Char(string="Q1 Feb")
    q1_mar = fields.Char(string="Q1 Mar")
    q2_apr = fields.Char(string="Q2 Apr")
    q2_may = fields.Char(string="Q2 May")
    q2_jun = fields.Char(string="Q2 Jun")
    q3_jul = fields.Char(string="Q3 Jul")
    q3_aug = fields.Char(string="Q3 Aug")
    q3_sep = fields.Char(string="Q3 Sep")
    q4_oct = fields.Char(string="Q4 Oct")
    q4_nov = fields.Char(string="Q4 Nov")
    q4_dec = fields.Char(string="Q4 dec")

    id_sarmut = fields.Many2one("qma.sarmut", string="ID Parent Sarmut")