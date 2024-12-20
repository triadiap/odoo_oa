from odoo import api, fields, models, _

class BusdevMonitoringProjectInv(models.Model):
    _name = "busdev.monitoring.project"
    _description = "Model for BUSDEV Monitoring Project"

    name = fields.Char(string="Nama Investasi", required=True)
    pic = fields.Many2one("res.users", string="PIC", required=True)
    start_date = fields.Date(string="Tanggal Mulai Pekerjaan", required=True)
    due_date = fields.Date(string="Due Date", required=True)
    notes = fields.Text(string="Keterangan")
    satuan_kerja = fields.Many2one("hr.department", string="Satuan Kerja", required=True)
    kepala_satker = fields.Many2one("hr.employee", string="Kepala Satker", store=True)
    status_project = fields.Selection([
        ("inisiasi", "Inisiasi"),
        ("sedang_berjalan", "Sedang Berjalan"),
        ("selesai", "Selesai"),
    ], string="Status", required=True)
    klasifikasi = fields.Selection([
        ("capex", "CAPEX"),
        ("opex", "OPEX"),
    ], string="Klasifikasi", required=True)
    kriteria = fields.Selection([
        ("rutin", "Rutin"),
        ("non_rutin", "Non-Rutin"),
        ("carryover", "Carryover"),
    ], string="Kriteria", required=True)
    nama_vendor = fields.Char(string="Nama Vendor")

    detail_items = fields.One2many("busdev.monitoring.project.detail", "id_project", string="Progres")
    list_dokumen = fields.One2many("busdev.project.document", "id_project_d", string="Dokumen")
    list_pembayaran = fields.One2many("busdev.project.payment", "id_project_p", string="Dokumen")

    @api.onchange('satuan_kerja')
    def _get_satker_manager(self):
        for record in self:
            record.kepala_satker = record.satuan_kerja.manager_id

class BusdevMonitoringProjectDetails(models.Model):
    _name = "busdev.monitoring.project.detail"
    _description = "Model for BUSDEV Monitoring Project Progress Item"

    date = fields.Date(string="Tanggal", required=True)
    progress = fields.Text(string="Deskripsi Progres", required=True)
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
    jumlah = fields.Integer(string="Jumlah", required=True)

    id_project_p = fields.Many2one("busdev.monitoring.project", string="ID Project")