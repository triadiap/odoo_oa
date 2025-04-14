from odoo import api, models, fields, _

class MoLkh(models.Model):
    _name="mo.lkh.main"

    _description = "Main model for MO LKH"

    report_date = fields.Date(string="Tanggal Pelaporan", required=True)
    shift = fields.Selection([
        ("1", "Shift 1"),
        ("2", "Shift 2"),
        ("3", "Shift 3"),
    ], string="Shift", required=True, default="1")
    mitra = fields.Many2one("res.partner", string="Nama Mitra", required=True)

    standby_unsafe_buldozer = fields.Many2many("mo.master.equipment.bulldozer",'standby_unsafe_bulldozer_rel',  # Unique relation table name
        'record_id',
        'bulldozer_id', string="Bulldozer",
                                      domain="[('id_master.partner_id', '=', mitra)]")
    standby_unsafe_excavator = fields.Many2many("mo.master.equipment.excavator",'standby_unsafe_excavator_rel',  # Unique relation table name
        'record_id',
        'bulldozer_id', string="Excavator",
                                       domain="[('id_master.partner_id', '=', mitra)]")
    standby_unsafe_alat_angkut = fields.Many2many("mo.master.equipment.alatangkut",'standby_unsafe_alat_angkut_rel',  # Unique relation table name
        'record_id',
        'bulldozer_id', string="Alat Angkut", domain="[('id_master.partner_id', '=', mitra)]")


    standby_no_op_buldozer = fields.Many2many("mo.master.equipment.bulldozer",'standby_no_op_bulldozer_rel',  # Unique relation table name
        'record_id',
        'bulldozer_id', string="Bulldozer",
                                      domain="[('id_master.partner_id', '=', mitra)]")
    standby_no_op_excavator = fields.Many2many("mo.master.equipment.excavator",'standby_no_op_excavator_rel',  # Unique relation table name
        'record_id',
        'bulldozer_id', string="Excavator",
                                       domain="[('id_master.partner_id', '=', mitra)]")
    standby_no_op_alat_angkut = fields.Many2many("mo.master.equipment.alatangkut",'standby_no_op_alat_angkut_rel',  # Unique relation table name
        'record_id',
        'bulldozer_id', string="Alat Angkut", domain="[('id_master.partner_id', '=', mitra)]")


    breakdown_buldozer = fields.Many2many("mo.master.equipment.bulldozer",'breakdown_bulldozer_rel',  # Unique relation table name
        'record_id',
        'bulldozer_id', string="Bulldozer",
                                      domain="[('id_master.partner_id', '=', mitra)]")
    breakdown_excavator = fields.Many2many("mo.master.equipment.excavator",'breakdown_excavator_rel',  # Unique relation table name
        'record_id',
        'bulldozer_id', string="Excavator",
                                       domain="[('id_master.partner_id', '=', mitra)]")
    breakdown_alat_angkut = fields.Many2many("mo.master.equipment.alatangkut",'breakdown_alat_angkut_rel',  # Unique relation table name
        'record_id',
        'bulldozer_id', string="Alat Angkut", domain="[('id_master.partner_id', '=', mitra)]")

    bool_mh = fields.Boolean(string="MH", default=False)
    unit_mh = fields.Char(string="No. Unit")
    bool_ft = fields.Boolean(string="FT", default=False)
    unit_ft = fields.Char(string="No. Unit")
    bool_wt = fields.Boolean(string="WT", default=False)
    unit_wt = fields.Char(string="No. Unit")
    bool_vb = fields.Boolean(string="VB", default=False)
    unit_vb = fields.Char(string="No. Unit")
    bool_mg = fields.Boolean(string="MG", default=False)
    unit_mg = fields.Char(string="No. Unit")

    barge_items = fields.One2many("mo.lkh.barging", "lkh_id", string="Barging")
    ore_items = fields.One2many("mo.lkh.ore", "lkh_id", string="Ore Material")
    ob_items = fields.One2many("mo.lkh.ob", "lkh_id", string="OB Material")
    act_items = fields.One2many("mo.lkh.activity", "lkh_id", string="Activity")
    delay_items = fields.One2many("mo.lkh.delayinfo", "lkh_id", string="Delay Information")
    rain_prod_items = fields.One2many("mo.lkh.delay.rain.prod", "lkh_id", string="Rain Prod")
    rain_brg_items = fields.One2many("mo.lkh.delay.rain.brg", "lkh_id", string="Rain Barging")
    slippery_prod_items = fields.One2many("mo.lkh.delay.slippery.prod", "lkh_id", string="Slippery Prod")
    slippery_brg_items = fields.One2many("mo.lkh.delay.slippery.brg", "lkh_id", string="Slippery Barging")

    def name_get(self):
        result = []
        for record in self:
            display_name = f"{record.report_date} - {record.shift} - {record.mitra.name}"  # Custom display
            result.append((record.id, display_name))
        return result

class MoLkhBarging(models.Model):
    _name="mo.lkh.barging"

    _description = "Model for MO LKH Barging activity"

    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")

    partner_id = fields.Many2one("res.partner", related="lkh_id.mitra", store=True, readonly=True)
    barge_no = fields.Char(string="Barging Number", required=True)
    nama_kapal = fields.Char(string="Nama Kapal", required=True)
    plan = fields.Char(string="Plan")
    total_tonnage = fields.Float(string='Belum Termuat')
    loaded = fields.Float(string='Termuat')
    balance = fields.Float(string='Balance', compute='_compute_balance', store=True, readonly=True)
    rit_count = fields.Integer(string="Rit count", required=True)
    barge_buldozer = fields.Many2many("mo.master.equipment.bulldozer", string="Bulldozer", domain="[('id_master.partner_id', '=', partner_id)]")
    barge_excavator = fields.Many2many("mo.master.equipment.excavator", string="Excavator", domain="[('id_master.partner_id', '=', partner_id)]")
    barge_alat_angkut = fields.Many2many("mo.master.equipment.alatangkut", string="Alat Angkut", domain="[('id_master.partner_id', '=', partner_id)]")

    @api.depends('total_tonnage', 'loaded')
    def _compute_balance(self):
        for record in self:
            record.balance = record.total_tonnage - record.loaded
class MoLkhOreMaterial(models.Model):
    _name="mo.lkh.ore"

    _description = "Model for MO LKH Ore Material Activity"
    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")

    partner_id = fields.Many2one("res.partner", related="lkh_id.mitra", store=True, readonly=True)
    location = fields.Many2one("mo.master.lokasi", string="Lokasi Angkut", required=True)
    location_drop = fields.Many2one("mo.master.lokasi", string="Lokasi Tujuan", required=True)
    ore_adt_rit_count = fields.Integer(string="ADT Rit", default=0)
    ore_dt_rit_count = fields.Integer(string="DT Rit", default=0)
    ore_buldozer = fields.Many2many("mo.master.equipment.bulldozer", string="Bulldozer",
                                      domain="[('id_master.partner_id', '=', partner_id)]")
    ore_excavator = fields.Many2many("mo.master.equipment.excavator", string="Excavator",
                                       domain="[('id_master.partner_id', '=', partner_id)]")
    ore_alat_angkut = fields.Many2many("mo.master.equipment.alatangkut", string="Alat Angkut",
                                         domain="[('id_master.partner_id', '=', partner_id)]")

class MoLkhOb(models.Model):
    _name="mo.lkh.ob"

    _description = "Model for MO LKH OB Material Activity"

    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")

    location = fields.Char(string="Location")
    partner_id = fields.Many2one("res.partner", related="lkh_id.mitra", store=True, readonly=True)
    ob_adt_topsoil = fields.Integer(string="Top Soil ADT")
    ob_dt_topsoil = fields.Integer(string="Top Soil ADT")
    ob_adt_limonit = fields.Integer(string="Limonit ADT")
    ob_dt_limonit = fields.Integer(string="Limonit ADT")
    ob_adt_waste = fields.Integer(string="Waste ADT")
    ob_dt_waste = fields.Integer(string="Waste ADT")
    ob_adt_develop = fields.Integer(string="Develop ADT")
    ob_dt_develop = fields.Integer(string="Develop ADT")
    ob_buldozer = fields.Many2many("mo.master.equipment.bulldozer", string="Bulldozer",
                                      domain="[('id_master.partner_id', '=', partner_id)]")
    ob_excavator = fields.Many2many("mo.master.equipment.excavator", string="Excavator",
                                       domain="[('id_master.partner_id', '=', partner_id)]")
    ob_alat_angkut = fields.Many2many("mo.master.equipment.alatangkut", string="Alat Angkut",
                                         domain="[('id_master.partner_id', '=', partner_id)]")

class MoLkhActivity(models.Model):
    _name = "mo.lkh.activity"

    _description = "Model for MO LKH Activity detail"

    act_start = fields.Datetime(string="Start")
    act_stop = fields.Datetime(string="End")
    activity_detail = fields.Char(string="Activity")

    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")

class MoLkhDelayInfo(models.Model):
    _name = "mo.lkh.delayinfo"

    _description = "Model for MO LKH Delay Information"

    location = fields.Char(string="Location")
    delay_item = fields.Char(string="Delay Item")
    jam_delay = fields.Datetime(string="Jam")

    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")

class MoLkhDelayRainProd(models.Model):
    _name = "mo.lkh.delay.rain.prod"
    _description = "Model for MO LKH Delay Rain Prod"

    w_from = fields.Float(string="Rain Prod. Start")
    w_to = fields.Float(string="Rain Prod. End")
    curah = fields.Float(string="Curah Hujan (mm)")
    notes = fields.Char(string="Notes")

    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")

class MoLkhDelayRainBrg(models.Model):
    _name = "mo.lkh.delay.rain.brg"
    _description = "Model for MO LKH Delay Rain Barging"

    w_from = fields.Float(string="Rain Brg. Start")
    w_to = fields.Float(string="Rain Brg. End")
    curah = fields.Float(string="Curah Hujan (mm)")
    notes = fields.Char(string="Notes")

    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")

class MoLkhDelaySlipperyProd(models.Model):
    _name = "mo.lkh.delay.slippery.prod"
    _description = "Model for MO LKH Delay Slippery Prod"

    w_from = fields.Float(string="Slippery Prod. Start")
    w_to = fields.Float(string="Slippery Prod. End")
    notes = fields.Char(string="Notes")

    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")

class MoLkhDelaySlipperyBrg(models.Model):
    _name = "mo.lkh.delay.slippery.brg"
    _description = "Model for MO LKH Delay Slippery Barging"

    w_from = fields.Float(string="Slippery Brg. Start")
    w_to = fields.Float(string="Slippery Brg. End")
    notes = fields.Char(string="Notes")

    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")