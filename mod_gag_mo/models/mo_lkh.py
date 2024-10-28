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
    mitra = fields.Selection([
        ("MKA", "PT. MKA"),
        ("SMA", "PT. SMA")
    ], string="Nama Mitra", required=True)

    standby_unsafe_buldozer = fields.Char(string="Buldozer")
    standby_unsafe_excavator = fields.Char(string="Excavator")
    standby_unsafe_alat_angkut = fields.Char(string="Alat Angkut (ADT/DT)")
    standby_no_op_buldozer = fields.Char(string="Buldozer")
    standby_no_op_excavator = fields.Char(string="Excavator")
    standby_no_op_alat_angkut = fields.Char(string="Alat Angkut (ADT/DT)")
    breakdown_buldozer = fields.Char(string="Buldozer")
    breakdown_excavator = fields.Char(string="Excavator")
    breakdown_alat_angkut = fields.Char(string="Alat Angkut (ADT/DT)")

    bool_mh = fields.Boolean(string="MH", default=False)
    bool_ft = fields.Boolean(string="FT", default=False)
    bool_wt = fields.Boolean(string="WT", default=False)
    bool_vb = fields.Boolean(string="VB", default=False)
    bool_mg = fields.Boolean(string="MG", default=False)

    rain_prod_from = fields.Datetime(string="Rain Prod. Start")
    rain_prod_to = fields.Datetime(string="Rain Prod. End")

    rain_brg_from = fields.Datetime(string="Rain Brg. Start")
    rain_brg_to = fields.Datetime(string="Rain Brg. End")

    slippery_prod_from = fields.Datetime(string="Slippery Prod. Start")
    slippery_prod_to = fields.Datetime(string="Slippery Prod. End")

    slippery_brg_from = fields.Datetime(string="Slippery Brg. Start")
    slippery_brg_to = fields.Datetime(string="Slippery Brg. End")

    barge_items = fields.One2many("mo.lkh.barging", "lkh_id", string="Barging")
    ore_items = fields.One2many("mo.lkh.ore", "lkh_id", string="Ore Material")
    ob_items = fields.One2many("mo.lkh.ob", "lkh_id", string="OB Material")
    act_items = fields.One2many("mo.lkh.activity", "lkh_id", string="Activity")
    delay_items = fields.One2many("mo.lkh.delayinfo", "lkh_id", string="Detaly Information")

class MoLkhBarging(models.Model):
    _name="mo.lkh.barging"

    _description = "Model for MO LKH Barging activity"

    barge_no = fields.Char(string="Barging Number", required=True)
    rit_count = fields.Integer(string="Rit count", required=True)
    barge_buldozer = fields.Char(string="Buldozer")
    barge_excavator = fields.Char(string="Excavator")
    barge_alat_angkut = fields.Char(string="Alat Angkut (ADT/DT)")

    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")

class MoLkhOreMaterial(models.Model):
    _name="mo.lkh.ore"

    _description = "Model for MO LKH Ore Material Activity"

    location = fields.Char(string="Location", required=True)
    ore_adt_rit_count = fields.Integer(string="ADT Rit", default=0)
    ore_dt_rit_count = fields.Integer(string="DT Rit", default=0)
    ore_buldozer = fields.Char(string="Buldozer")
    ore_excavator = fields.Char(string="Excavator")
    ore_alat_angkut = fields.Char(string="Alat Angkut (ADT/DT)")

    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")

class MoLkhOb(models.Model):
    _name="mo.lkh.ob"

    _description = "Model for MO LKH OB Material Activity"

    location = fields.Char(string="Location")
    ob_adt_topsoil = fields.Integer(string="Top Soil ADT")
    ob_dt_topsoil = fields.Integer(string="Top Soil ADT")
    ob_adt_limonit = fields.Integer(string="Limonit ADT")
    ob_dt_limonit = fields.Integer(string="Limonit ADT")
    ob_adt_waste = fields.Integer(string="Waste ADT")
    ob_dt_waste = fields.Integer(string="Waste ADT")
    ob_adt_develop = fields.Integer(string="Develop ADT")
    ob_dt_develop = fields.Integer(string="Develop ADT")
    ob_buldozer = fields.Char(string="Buldozer")
    ob_excavator = fields.Char(string="Excavator")
    ob_alat_angkut = fields.Char(string="Alat Angkut (ADT/DT)")

    lkh_id = fields.Many2one("mo.lkh.main", string="LKH ID")

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
