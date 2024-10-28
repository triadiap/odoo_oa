from odoo import api, fields, models, _

class BusdevMonitoringProjectInv(models.Model):
    _name = "busdev.monitoring.project"
    _description = "Model for BUSDEV Monitoring Project"

    name = fields.Char(string="Nama Investasi", required=True)
    pic = fields.Many2one("res.users", string="PIC", required=True)
    start_date = fields.Date(string="Tanggal Mulai Pekerjaan", required=True)
    due_date = fields.Date(string="Due Date", required=True)
    notes = fields.Text(string="Keterangan")
    detail_items = fields.One2many("busdev.monitoring.project.detail", "id_project", string="Progres")

class BusdevMonitoringProjectDetails(models.Model):
    _name = "busdev.monitoring.project.detail"
    _description = "Model for BUSDEV Monitoring Project Progress Item"

    date = fields.Date(string="Tanggal", required=True)
    progress = fields.Text(string="Deskripsi Progres", required=True)
    id_project = fields.Many2one("busdev.monitoring.project", string="ID Project")