from odoo import api, models, fields, _
from datetime import datetime

class MpdBeritaAcaraRealisasiProduksi(models.Model):
    _name = "mpd.realisasi.produksi"
    _description = "Model for MPD Berita Acara Rencana Produksi"

    def _get_months(self):
        return [
            ('01', 'January'), ('02', 'February'), ('03', 'March'),
            ('04', 'April'), ('05', 'May'), ('06', 'June'),
            ('07', 'July'), ('08', 'August'), ('09', 'September'),
            ('10', 'October'), ('11', 'November'), ('12', 'December')
        ]

    def _get_years(self):
        current_year = datetime.now().year
        return [(str(year), str(year)) for year in range(current_year - 1, current_year + 2 )]

    month = fields.Selection(selection=_get_months, string="Bulan", required=True)
    year = fields.Selection(selection=_get_years, string="Tahun", required=True)
    mitra = fields.Char(string="Mitra", required=True)
    ore = fields.Float(string="Ore (WMT)", required=True)
    waste = fields.Float(string="Waste (WMT)", required=True)
    waste_left = fields.Float(string="Waste Tertinggal (WMT)", required=True)
    sr = fields.Float(string="SR", required=True)
    density_ore = fields.Float(string="Density Ore", required=True)
    pengapalan = fields.Float(string="Pengapalan (WMT)", required=True)
    total_stock = fields.Float(string="Total Stock", required=True)
    file = fields.Binary(string="Soft Copy Berita Acara")

    state = fields.Selection([
        ("draft", "Draft"),
        ("approval_1", "Approved By MPD Manager"),
        ("approval_2", "Approved By QC Manager"),
        ("approval_3", "Approved By MO Manager"),
        ("approval_4", "Approved By General Manager"),
    ], string="Status", default="draft")

    approval_1 = fields.Many2one("res_users", string="MPD Manager")
    approval_2 = fields.Many2one("res_users", string="QC Manager")
    approval_3 = fields.Many2one("res_users", string="MO Manager")
    approval_4 = fields.Many2one("res_users", string="General Manager")

    def action_approval_1(self):
        self.state = "approval_1"
        self.approval_1 = self.env.user.id

    def action_approval_2(self):
        self.state = "approval_2"
        self.approval_2 = self.env.user.id

    def action_approval_3(self):
        self.state = "approval_3"
        self.approval_3 = self.env.user.id

    def action_approval_4(self):
        self.state = "approval_4"
        self.approval_4 = self.env.user.id