# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ParentEquipment(models.Model):
    _inherit =[ "maintenance.equipment"]
    id_equipment = fields.One2many('part.byequipment', 'equipment_id', string="Lines")

class DetailPartPerEquipment(models.Model):
    _name = "part.byequipment"
    _description = "Detail Part Per Equipment"

    part_code = fields.Many2one('gagtb.part', string="Nama Sparepart", required=True)
    equipment_id = fields.Many2one('maintenance.equipment', string="Parent")