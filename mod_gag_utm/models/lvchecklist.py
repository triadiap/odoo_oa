from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class LVchecklistMasterData(models.Model):
    _name = 'oa.lv.checklistindikator'
    _description = 'LV Machine Checklist Indicator Master Data'

    name = fields.Char(string="Indikator Yang Diperiksa", required=True, tracking=True)
    subunit = fields.Many2one('msdata.checkpoints',string="Unit Group",tracking=True)
