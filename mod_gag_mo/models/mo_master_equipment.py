from odoo import api, models, fields, _

class MoMasterEquipment(models.Model):
    _name = "mo.master.equipment"
    _description = "MO Master Equipment"

    partner_id = fields.Many2one("res.partner", string="Nama Mitra", required=True)

    bulldozer_list = fields.One2many("mo.master.equipment.bulldozer", "id_master", string="Bulldozer List")
    excavator_list = fields.One2many("mo.master.equipment.excavator", "id_master", string="Excavator List")
    alat_angkut_list = fields.One2many("mo.master.equipment.alatangkut", "id_master", string="Alat Angkut List")

    buldozer_count = fields.Integer(string="Bulldozer", compute="_compute_buldozer_count")
    excavator_count = fields.Integer(string="Excavator", compute="_compute_excavator_count")
    aa_count = fields.Integer(string="Alat Angkut", compute="_compute_aa_count")

    @api.depends("bulldozer_list")
    def _compute_buldozer_count(self):
        for record in self:
            record.buldozer_count = len(record.bulldozer_list)

    @api.depends("excavator_list")
    def _compute_excavator_count(self):
        for record in self:
            record.excavator_count = len(record.excavator_list)

    @api.depends("alat_angkut_list")
    def _compute_aa_count(self):
        for record in self:
            record.aa_count = len(record.alat_angkut_list)

class MoEquipmentBuldozer(models.Model):
    _name = "mo.master.equipment.bulldozer"
    _description = "MO Master Equipment Bulldozer"

    no_unit = fields.Char(string="No. Unit", required=True)
    name = fields.Char(string="Unit Name / Type", required=True)

    id_master = fields.Many2one("mo.master.equipment", string="ID Master")

    def name_get(self):
        result = []
        for record in self:
            display_name = f"{record.no_unit}"  # Custom display
            result.append((record.id, display_name))
        return result

class MoEquipmentExcavator(models.Model):
    _name = "mo.master.equipment.excavator"
    _description = "MO Master Equipment Excavator"

    no_unit = fields.Char(string="No. Unit", required=True)
    name = fields.Char(string="Unit Name / Type", required=True)

    id_master = fields.Many2one("mo.master.equipment", string="ID Master")

    def name_get(self):
        result = []
        for record in self:
            display_name = f"{record.no_unit}"  # Custom display
            result.append((record.id, display_name))
        return result

class MoEquipmentAlatAngkut(models.Model):
    _name = "mo.master.equipment.alatangkut"
    _description = "MO Master Equipment Alat Angkut"

    no_unit = fields.Char(string="No. Unit", required=True)
    name = fields.Char(string="Unit Name", required=True)
    tipe = fields.Selection([
        ("adt", "ADT"),
        ("dt", "DT"),
    ], string="Tipe", required=True)

    id_master = fields.Many2one("mo.master.equipment", string="ID Master")

    def name_get(self):
        result = []
        for record in self:
            display_name = f"{record.no_unit}"  # Custom display
            result.append((record.id, display_name))
        return result