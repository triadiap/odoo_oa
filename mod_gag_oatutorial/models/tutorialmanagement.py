# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import logging

class TutorialManagement(models.Model):
    _name = 'oa.tutorial.management'
    _description = 'Office Automation Tutorial Management'

    name = fields.Char(string="Title", required=True)
    content = fields.Html(string="Description")
    menu_id = fields.Many2one('ir.ui.menu',string="Related Menu", domain=[('parent_id', '=', False)])

    @api.model
    def create(self, vals):
        """Override create to add custom menu when saving the record."""
        # Create the record first
        record = super(TutorialManagement, self).create(vals)

        # Create the custom menu
        if record.menu_id:
            record.create_custom_menu(record.menu_id.id)

        return record

    def write(self, vals):
        """Override write to update custom menu when updating the record."""
        res = super(TutorialManagement, self).write(vals)

        # Create or update custom menu if menu_id has been changed
        if 'menu_id' in vals:
            self.create_custom_menu(self.menu_id.id)

        return res

    def unlink(self):
        """Override unlink to delete custom menu when deleting the record."""
        # Delete the custom menu before unlinking the record
        for record in self:
            if record.menu_id:
                record.delete_custom_menu(record.menu_id.id)

        return super(TutorialManagement, self).unlink()

    def create_custom_menu(self, menu_id):
        """Create custom submenus under the selected menu."""
        selected_menu = self.env['ir.ui.menu'].browse(menu_id)
        if not selected_menu:
            raise ValidationError("Selected menu does not exist.")

        # Check if the custom submenu already exists to avoid duplication
        custom_submenu_name = f'Tutorial {selected_menu.name}'
        existing_submenu = self.env['ir.ui.menu'].search([
            ('name', '=', custom_submenu_name),
            ('parent_id', '=', selected_menu.id),
        ], limit=1)

        if not existing_submenu:
            # Create the custom submenu
            self.env['ir.ui.menu'].create({
                'name': custom_submenu_name,
                'parent_id': selected_menu.id,
                'action': 'ir.actions.act_window,%d' % self._get_action_id(selected_menu.id),
            })

    def delete_custom_menu(self, menu_id):
        """Delete the custom submenu created under the selected menu."""
        selected_menu = self.env['ir.ui.menu'].browse(menu_id)
        if not selected_menu:
            raise ValidationError("Selected menu does not exist.")

        # Search for the custom submenu and delete it
        custom_submenu_name = f'Tutorial {selected_menu.name}'
        existing_submenu = self.env['ir.ui.menu'].search([
            ('name', '=', custom_submenu_name),
            ('parent_id', '=', selected_menu.id),
        ], limit=1)

        if existing_submenu:
            existing_submenu.unlink()  # Unlink (delete) the submenu

    def _get_action_id(self,menu_id):
        selected_menu = self.env['ir.ui.menu'].browse(menu_id)
        """Create and return a sample action for the custom menu."""
        custom_header_name = f'Tutorial For {selected_menu.name}'
        action = self.env['ir.actions.act_window'].create({
            'name': custom_header_name,
            'res_model': 'oa.tutorial.management',  # Link to this model
            'view_mode': 'tree,form',
            'domain': [('menu_id', '=', menu_id)],
        })
        return action.id

    @api.model
    def search_based_on_menu(self, menu_id):
        """Override the search to filter by selected menu."""
        return self.search([('menu_id', '=', menu_id)])
