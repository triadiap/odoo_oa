from odoo import api, models, fields, _

class HcMasterRiskType(models.Model):
    _name = "hc.master.risk.type"
    _description = "HC, GA, ICT Master Risk Type"

    name = fields.Char(string="Risk Type", required=True)
    taksonomi = fields.Char(string="Taksonomi", required=True)