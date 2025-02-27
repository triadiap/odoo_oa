from odoo import api, models, fields, _

class  HcMasterApprovalNdpp(models.Model):
    _name = "hc.master.approval.ndpp"
    _description = "HC Master Approval NDPP"

    name = fields.Many2one("hr.employee", string="Nama")
    jabatan = fields.Char(string="Jabatan")