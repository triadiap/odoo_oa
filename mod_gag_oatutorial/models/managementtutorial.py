# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import logging

class TutorialManagement(models.Model):
    _name = 'oa.management.tutorial'
    _description = 'Office Automation Tutorial Management'

    name = fields.Char(string="Title", required=True)
    content = fields.Html(string="Description",sanitize=False)
    menu_id = fields.Many2one('ir.ui.menu',string="Parent Menu", domain=[('parent_id', '=', False)],required=True)
    child_menu_id = fields.Many2one(
        'ir.ui.menu',
        string="Child Menu",
        domain=[]  # The domain will be set dynamically
    )

    hide_css = fields.Html(string='CSS', compute='_compute_edit_visibility', sanitize=False, store=False)

    def _compute_edit_visibility(self):
        for record in self:
            # If the current user is not the creator, hide the Edit button
            if record.create_uid.id != self.env.uid:
                record.hide_css = '''
                    <style>
                        .o_form_button_edit { display: none !important; }
                    </style>
                '''
            else:
                record.hide_css = ''

    @api.onchange('menu_id')
    def _onchange_menu_id(self):
        """Dynamically update the domain of child_menu_id based on menu_id."""
        if self.menu_id:
            self.child_menu_id = False  # Reset the value when menu_id changes
            return {
                'domain': {
                    'child_menu_id': [('parent_id', '=', self.menu_id.id)],
                }
            }
        else:
            self.child_menu_id = False
            return {
                'domain': {
                    'child_menu_id': [],
                }
            }




