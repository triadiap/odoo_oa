from odoo import api, models, fields, _

class HcMasterRiskLevel(models.Model):
    _name = "hc.master.risk.level"
    _description = "HC, GA, ICT Master Risk Level"

    risk_level = fields.Integer(string="Risk Level (RL)")
    kuadran = fields.Char(string="Kuadran")