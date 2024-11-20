from odoo import api, fields, models, _

class PtgnApdItem(models.Model):
    _name = "ptgn.apd.item"
    _description = "Model for PTGN MD APD items"

    apd = fields.Char(string="Nama APD")

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.apd}"
            result.append((record.id, name))
        return result