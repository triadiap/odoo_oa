from odoo import models, fields

class Daftarmenu(models.Model):
    _name = 'tb.menu'
    _description = 'Tabel Menu'

    idmenu = fields.Integer
    menu_name = fields.Char(string='Nama Menu')
    route_address = fields.Char(string='Route Address')