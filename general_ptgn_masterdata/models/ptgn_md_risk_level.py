from odoo import api, models, fields, _

class PtgnMdRiskLevel(models.Model):
    _name = "ptgn.md.risk.level"
    _description = "PTGN MD Risk Level"

    risk_level = fields.Integer(string="Risk Level (RL)")
    kuadran = fields.Char(string="Kuadran")