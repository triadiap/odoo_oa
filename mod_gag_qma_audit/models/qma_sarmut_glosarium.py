from odoo import api, models, fields, _
from datetime import datetime

class QmaSarmutGlosarium(models.Model):
    _name = "qma.sarmut.glosarium"
    _description = "QMA Sasaran Target Mutu Glosarium"

    department_id = fields.Many2one("hr.department", string="Satuan Kerja", required=True,
                                    default=lambda self: self.env.user.department_id.id)
    year = fields.Selection(selection="_get_years", string="Tahun", required=True)

    glo_detail = fields.One2many("qma.sarmut.glosarium.detail", "id_sarmut_glosarium", string="Detail")

    def _get_years(self):
        current_year = datetime.now().year
        return [(str(year), str(year)) for year in range(current_year - 1, current_year + 2)]

    def name_get(self):
        result = []
        for record in self:
            display_name = f"{record.department_id.display_name} {record.year}"  # Custom display
            result.append((record.id, display_name))
        return result

class QmaSarmutGlosariumDetail(models.Model):
    _name = "qma.sarmut.glosarium.detail"
    _description = "QMA Sasaran Target Mutu Glosarium Detail"

    name = fields.Char(string="Judul", required=True)
    definisi = fields.Char(string="Definisi", required=True)
    satuan = fields.Char(string="Satuan Pengukuran", required=True)
    sasaran = fields.Char(string="Pemenuhan Sasaran", required=True)
    arah = fields.Char(string="Arah")
    pencapaian_max = fields.Char(string="Maksimal Pencapaian")
    bobot = fields.Integer(string="Bobot")
    q1 = fields.Html(string="Target Q1", required=True)
    q2 = fields.Html(string="Target Q2", required=True)
    q3 = fields.Html(string="Target Q3", required=True)
    q4 = fields.Html(string="Target Q4", required=True)

    id_sarmut_glosarium = fields.Many2one("qma.sarmut.glosarium", string="ID")