from odoo import api, models, fields, _

class QmaMasterScore(models.Model):
    _name = "qma.master.score"
    _description = "QMA Master Score"

    name = fields.Char(string="Score", required=True)
    notes = fields.Char(string="Keterangan", required=True)