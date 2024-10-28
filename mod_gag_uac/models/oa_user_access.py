# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class OAUserAccess(models.Model):
    _name = 'custom.menu.access'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Custom Menu Access'

    name = fields.Char(string="Name", required=True, tracking=True)
    menu_id = fields.Many2one('ir.ui.menu', string="Menu", required=True, tracking=True)
    group_ids = fields.Many2many('res.groups', string="User Groups" , tracking=True)
    visible = fields.Boolean(string="Is Visible", default=True, tracking=True)

    @api.model
    def create(self, vals):
        record = super(OAUserAccess, self).create(vals)
        # Apply visibility when creating a new record
        record.apply_menu_visibility()
        return record

    def write(self, vals):
        res = super(OAUserAccess, self).write(vals)
        # Apply visibility when updating an existing record
        self.apply_menu_visibility()
        return res

    def unlink(self):
        # Restore menu access to default state on record deletion
        for record in self:
            # Example of reverting to a default state (remove all group restrictions)
            if record.visible:
                # Make menu visible to all if applicable
                record.menu_id.write({'groups_id': [(6, 0, record.group_ids.ids)]})
            else:
                # Remove all group restrictions
                record.menu_id.write({'groups_id': [(5,)]})
        return super(OAUserAccess, self).unlink()
    def apply_menu_visibility(self):
        # Logic to apply visibility based on user groups
        for record in self:
            if record.visible:
                record.menu_id.write({'groups_id': [(6, 0, record.group_ids.ids)]})
            else:
                record.menu_id.write({'groups_id': [(5,)]})  # Remove groups



