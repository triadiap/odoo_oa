from odoo import api, models, fields, _

class QmaMasterStatusSop(models.Model):
    _name = "qma.master.status.sop"
    _description = "Model for QMA Master Status SOP"

    name = fields.Char(string="Status SOP", required=True)
    notes = fields.Char(string="Keterangan")