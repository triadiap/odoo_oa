# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class MasterSparepart(models.Model):
    _name = "gagtb.part"
    _description = "Master Data Sparepart"
    _rec_name = 'part_description'

    part_number = fields.Char(string="Part Number", required=True)
    part_description = fields.Char(string="Part Name", required=True)
    part_uom = fields.Selection([
        ('1', ' PC ( Pcs )'),
        ('2', ' T ( Thousand )'),
        ('4', ' Gr ( Gram )'),
        ('5', ' Kg ( Kilogram )'),
        ('6', ' Ltr ( Liter )'),
        ('7', ' m ( Meter )'),
        ('8', ' ROL ( Roll )'),
    ], string="Satuan", required=True, default='1')
    part_qty = fields.Char(string="Jumlah Stock", required=True)
