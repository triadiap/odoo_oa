from odoo import api, fields, models, _

class MoMasterApd(models.Model):
    _name = "mo.master.apd"
    _description = "Model for APD items"

    apd = fields.Char(string="Nama APD")

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.apd}"
            result.append((record.id, name))
        return result