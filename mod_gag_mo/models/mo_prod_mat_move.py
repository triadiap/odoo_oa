from odoo import api, models, fields, _

class MoProdMatMove(models.Model):
    _name = "mo.production.material.movement"
    _description = "Model for MO Production Material Movement"

    mitra = fields.Many2one("res.partner", string="Mitra", required=True)
    tanggal = fields.Date(string="Tanggal", required=True)
    shift = fields.Selection([
        ("shift_1", "Shift 1"),
        ("shift_2", "Shift 2"),
    ], string="Shift", required=True)
    loader = fields.Char(string="Loader")
    front = fields.Char(string="Front", required=True)
    eto = fields.Char(string="ETO")
    wd = fields.Char(string="WD")
    slctv = fields.Char(string="Slctv.")
    hauler = fields.Char(string="Hauler")
    trim = fields.Char(string="Trim")

    prod_item = fields.One2many("mo.production.material.movement.item", "id_prod", string="Ritase")

class MoBmmItems(models.Model):
    _name = "mo.production.material.movement.item"
    _description = "Model for MO Production Material Movement Item"

    hauler = fields.Char(string="Hauler", required=True)
    hrs_selection = fields.Selection([
        ("1", "07-08"),
        ("2", "08-09"),
        ("3", "09-10"),
        ("4", "10-11"),
        ("5", "11-12"),
        ("6", "12-13"),
        ("7", "13-14"),
        ("8", "14-15"),
        ("9", "15-16"),
        ("10", "16-17"),
        ("11", "17-18"),
        ("12", "18-19"),
        ("13", "19-20"),
        ("14", "20-21"),
        ("15", "21-22"),
        ("16", "22-23"),
        ("17", "23-00"),
        ("18", "00-01"),
        ("19", "01-02"),
        ("20", "02-03"),
        ("21", "03-04"),
        ("22", "04-05"),
        ("23", "05-06"),
        ("24", "06-07"),
    ], string="Periode", required=True)
    soil = fields.Integer(string="Soil")
    waste = fields.Integer(string="Wst")
    limonit = fields.Integer(string="Lim")
    ore = fields.Integer(string="Ore")
    dvl = fields.Integer(string="Dvl")

    id_prod = fields.Many2one("mo.production.material.movement", string="ID Prod")