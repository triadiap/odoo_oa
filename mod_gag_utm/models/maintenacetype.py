# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class MaintenanceTypeMaster(models.Model):

    _name = "oa.maintenancetype.master"
    _description = "Utility Maintenance Type Master"

    name = fields.Char(string="Maintenance Type")
    description = fields.Char(string="Description")