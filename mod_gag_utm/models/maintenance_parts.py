# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ParentMaintenance(models.Model):
    _inherit = "maintenance.request"
    id_maintenance = fields.One2many('detail.part', 'maintenance_id', string="Lines")

    def copy(self, default=None):
        default = dict(default or {})
        # Optionally, modify the name of the duplicated record
        default['name'] = f"Copy of {self.name}" if not self.name.startswith('Copy of') else self.name
        # Copy the parent record
        new_parent = super(ParentMaintenance, self).copy(default)
        # Copy each child record
        for child in self.id_maintenance:
            child.copy({'maintenance_id': new_parent.id})
        return new_parent

class DetailMaintenanceParts(models.Model):
    _name = "detail.part"
    _Description = "Detail Part Used"
    part_number = fields.Many2one('gagtb.part', string="Sparepart", required=True)
    stok_sparepart = fields.Integer(string="Stock", required=True)
    consumption_qty = fields.Integer(string="Jml Penggunaan", required=True)
    maintenance_id = fields.Many2one('maintenance.request', string="Parent")
    equpmnt_id = fields.Many2one('maintenance.equipment', string="EquipmentID")

