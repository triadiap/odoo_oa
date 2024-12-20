from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class ExcavaMiniChecklistIndikator(models.Model):
    _name = 'oa.excavaceklist.indikator'
    _description = 'Excavator Mini Checklist Indikator Master Data'

    name = fields.Char(string="Indikator Yang Diperiksa", required=True, tracking=True)
