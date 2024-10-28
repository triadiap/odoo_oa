# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class ParentAuditInfo(models.Model):
    _name="audit.building"
    _description = "Data Audit Building"

    location_id = fields.Many2one('msdata.location', string="Lokasi", required=True, tracking=True)
    building_id = fields.Many2one('msdata.building', string="Nama Bangunan", required=True, tracking=True)
    periode = fields.Char(string="Periode", required=True, tracking=True)
    year = fields.Selection(selection='_get_years', string='Tahun', default=lambda self: str(datetime.now().year))

    id_audit = fields.One2many('detail.audits', 'audit_id', string="Lines")
    def _get_years(self):
        current_year = datetime.now().year
        year_range = 10  # Number of years to generate
        years = [(str(year), str(year)) for year in range(current_year, current_year + year_range)]
        return years

class DetailAuditChecklist(models.Model):
    _name = "detail.audits"
    _description = "Detail Data Audit Building"

    audit_id = fields.Many2one('audit.building', string="Parent")
    checklist_id = fields.Many2one('msdata.checkpoints', string="Checking Point", required=True)
    condition = fields.Selection([
        ('1', 'Baik'),
        ('2', 'Cukup Baik'),
        ('3', 'Rusak'),
    ], string="Kondisi", required=True, default='1', tracking=True)
    action_propose = fields.Text(string="Tindakan")
    remarks = fields.Text(string="Keterangan")