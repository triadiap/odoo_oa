from odoo import api, models, fields, _

class QmaMasterJenisDokumen(models.Model):
    _name = "qma.master.jenis.dokumen"
    _description = "Model for QMA Master Jenis Dokumen"

    name = fields.Char(string="Jenis Dokumen", required=True)
    notes = fields.Char(string="Keterangan")