from odoo import models, fields

class UserInput(models.Model):
    _name = 'user.input'
    _description = 'User Input'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
