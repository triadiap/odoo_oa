from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
class  PelaporanReporting(models.Model):
    _name = "gag.oa.hse.pelaporan.reporting"
    _description = "Pelaporan jumlah pekerja per bulan"

    vendor = fields.Many2one("res.partner","Nama Kontraktor",required=True)
    year = fields.Char("Tahun",required = True)

    jml_tenaga_kerja_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_jamkerja_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_sakit_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_absen_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_spell_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_sakitkerja_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_nov = fields.Integer("Jan",compute="_compute_jam_kerja")    
    jml_sakitkerja_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_kelayakan_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_dec = fields.Integer("Jan",compute="_compute_jam_kerja")
    
    jml_kesakitan_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_dec = fields.Integer("Jan",compute="_compute_jam_kerja")
    
    jml_keseringan_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_dec = fields.Integer("Jan",compute="_compute_jam_kerja")
    
    jml_keparahan_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_dec = fields.Integer("Jan",compute="_compute_jam_kerja")
    
    jml_absenseverity_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_dec = fields.Integer("Jan",compute="_compute_jam_kerja")
    
    jml_ratiopak_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    def _compute_jam_kerja(self):
        for rec in self:
            rec.jml_kelayakan_jan = 0
            rec.jml_kelayakan_feb = 0
            rec.jml_kelayakan_mar = 0
            rec.jml_kelayakan_apr = 0
            rec.jml_kelayakan_may = 0
            rec.jml_kelayakan_jun = 0
            rec.jml_kelayakan_jul = 0
            rec.jml_kelayakan_aug = 0
            rec.jml_kelayakan_sep = 0
            rec.jml_kelayakan_oct = 0
            rec.jml_kelayakan_nov = 0
            rec.jml_kelayakan_dec = 0

            rec.jml_kesakitan_jan = 0
            rec.jml_kesakitan_feb = 0
            rec.jml_kesakitan_mar = 0
            rec.jml_kesakitan_apr = 0
            rec.jml_kesakitan_may = 0
            rec.jml_kesakitan_jun = 0
            rec.jml_kesakitan_jul = 0
            rec.jml_kesakitan_aug = 0
            rec.jml_kesakitan_sep = 0
            rec.jml_kesakitan_oct = 0
            rec.jml_kesakitan_nov = 0
            rec.jml_kesakitan_dec = 0

            rec.jml_keseringan_jan = 0
            rec.jml_keseringan_feb = 0
            rec.jml_keseringan_mar = 0
            rec.jml_keseringan_apr = 0
            rec.jml_keseringan_may = 0
            rec.jml_keseringan_jun = 0
            rec.jml_keseringan_jul = 0
            rec.jml_keseringan_aug = 0
            rec.jml_keseringan_sep = 0
            rec.jml_keseringan_oct = 0
            rec.jml_keseringan_nov = 0
            rec.jml_keseringan_dec = 0

            rec.jml_keparahan_jan = 0
            rec.jml_keparahan_feb = 0
            rec.jml_keparahan_mar = 0
            rec.jml_keparahan_apr = 0
            rec.jml_keparahan_may = 0
            rec.jml_keparahan_jun = 0
            rec.jml_keparahan_jul = 0
            rec.jml_keparahan_aug = 0
            rec.jml_keparahan_sep = 0
            rec.jml_keparahan_oct = 0
            rec.jml_keparahan_nov = 0
            rec.jml_keparahan_dec = 0

            rec.jml_absenseverity_jan = 0
            rec.jml_absenseverity_feb = 0
            rec.jml_absenseverity_mar = 0
            rec.jml_absenseverity_apr = 0
            rec.jml_absenseverity_may = 0
            rec.jml_absenseverity_jun = 0
            rec.jml_absenseverity_jul = 0
            rec.jml_absenseverity_aug = 0
            rec.jml_absenseverity_sep = 0
            rec.jml_absenseverity_oct = 0
            rec.jml_absenseverity_nov = 0
            rec.jml_absenseverity_dec = 0
            
            rec.jml_ratiopak_jan = 0
            rec.jml_ratiopak_feb = 0
            rec.jml_ratiopak_mar = 0
            rec.jml_ratiopak_apr = 0
            rec.jml_ratiopak_may = 0
            rec.jml_ratiopak_jun = 0
            rec.jml_ratiopak_jul = 0
            rec.jml_ratiopak_aug = 0
            rec.jml_ratiopak_sep = 0
            rec.jml_ratiopak_oct = 0
            rec.jml_ratiopak_nov = 0
            rec.jml_ratiopak_dec = 0


            rec.jml_tenaga_kerja_jan = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','1'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_feb = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','2'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_mar = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','3'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_apr = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','4'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_may = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','5'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_jun = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','6'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_jul = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','7'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_aug = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','8'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_sep = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','9'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_oct = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','10'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_nov = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','11'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_dec = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','12'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_pekerja')))
            
            rec.jml_jamkerja_jan = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','1'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_feb = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','2'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_mar = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','3'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_apr = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','4'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_may = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','5'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_jun = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','6'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_jul = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','7'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_aug = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','8'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_sep = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','9'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_oct = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','10'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_nov = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','11'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_dec = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','12'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_jamkerja')))

            rec.jml_sakit_jan = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','1'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))
            rec.jml_sakit_feb = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','2'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))
            rec.jml_sakit_mar = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','3'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))
            rec.jml_sakit_apr = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','4'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))
            rec.jml_sakit_may = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','5'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))
            rec.jml_sakit_jun = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','6'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))
            rec.jml_sakit_jul = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','7'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))
            rec.jml_sakit_aug = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','8'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))
            rec.jml_sakit_sep = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','9'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))
            rec.jml_sakit_oct = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','10'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))
            rec.jml_sakit_nov = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','11'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))
            rec.jml_sakit_dec = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','12'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakit')))

            rec.jml_absen_jan = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','1'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            rec.jml_absen_feb = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','2'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            rec.jml_absen_mar = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','3'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            rec.jml_absen_apr = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','4'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            rec.jml_absen_may = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','5'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            rec.jml_absen_jun = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','6'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            rec.jml_absen_jul = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','7'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            rec.jml_absen_aug = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','8'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            rec.jml_absen_sep = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','9'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            rec.jml_absen_oct = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','10'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            rec.jml_absen_nov = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','11'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            rec.jml_absen_dec = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','12'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_absen')))
            
            rec.jml_spell_jan = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','1'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            rec.jml_spell_feb = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','2'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            rec.jml_spell_mar = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','3'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            rec.jml_spell_apr = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','4'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            rec.jml_spell_may = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','5'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            rec.jml_spell_jun = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','6'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            rec.jml_spell_jul = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','7'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            rec.jml_spell_aug = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','8'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            rec.jml_spell_sep = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','9'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            rec.jml_spell_oct = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','10'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            rec.jml_spell_nov = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','11'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            rec.jml_spell_dec = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','12'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_spell')))
            
            rec.jml_sakitkerja_jan = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','1'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_feb = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','2'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_mar = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','3'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_apr = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','4'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_may = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','5'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_jun = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','6'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_jul = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','7'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_aug = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','8'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_sep = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','9'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_oct = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','10'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_nov = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','11'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_dec = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','12'),('year', '=',rec.year),('vendor','=',rec.vendor.id)]).mapped('total_sakitkerja')))


            if(rec.jml_tenaga_kerja_jan !=0):
                rec.jml_kelayakan_jan = ((rec.jml_tenaga_kerja_jan - rec.jml_sakit_jan)/rec.jml_tenaga_kerja_jan)*100
                rec.jml_kesakitan_jan = (rec.jml_sakit_jan /rec.jml_tenaga_kerja_jan)*100
                rec.jml_ratiopak_jan = (rec.jml_sakitkerja_jan /rec.jml_tenaga_kerja_jan)*100
                
            if(rec.jml_tenaga_kerja_feb !=0):
                rec.jml_kelayakan_feb = ((rec.jml_tenaga_kerja_feb - rec.jml_sakit_feb)/rec.jml_tenaga_kerja_feb)*100
                rec.jml_kesakitan_feb = (rec.jml_sakit_feb /rec.jml_tenaga_kerja_feb)*100
                rec.jml_ratiopak_feb = (rec.jml_sakitkerja_feb /rec.jml_tenaga_kerja_feb)*100
                
            if(rec.jml_tenaga_kerja_mar !=0):
                rec.jml_kelayakan_mar = ((rec.jml_tenaga_kerja_mar - rec.jml_sakit_mar)/rec.jml_tenaga_kerja_mar)*100
                rec.jml_kesakitan_mar = (rec.jml_sakit_mar /rec.jml_tenaga_kerja_mar)*100
                rec.jml_ratiopak_mar = (rec.jml_sakitkerja_mar /rec.jml_tenaga_kerja_mar)*100

            if(rec.jml_tenaga_kerja_apr !=0):
                rec.jml_kelayakan_apr = ((rec.jml_tenaga_kerja_apr - rec.jml_sakit_apr)/rec.jml_tenaga_kerja_apr)*100
                rec.jml_kesakitan_apr = (rec.jml_sakit_apr /rec.jml_tenaga_kerja_apr)*100
                rec.jml_ratiopak_apr = (rec.jml_sakitkerja_apr /rec.jml_tenaga_kerja_apr)*100

            if(rec.jml_tenaga_kerja_may !=0):
                rec.jml_kelayakan_may = ((rec.jml_tenaga_kerja_may - rec.jml_sakit_may)/rec.jml_tenaga_kerja_may)*100
                rec.jml_kesakitan_may = (rec.jml_sakit_may /rec.jml_tenaga_kerja_may)*100
                rec.jml_ratiopak_may = (rec.jml_sakitkerja_may /rec.jml_tenaga_kerja_may)*100

            if(rec.jml_tenaga_kerja_jun !=0):
                rec.jml_kelayakan_jun = ((rec.jml_tenaga_kerja_jun - rec.jml_sakit_jun)/rec.jml_tenaga_kerja_jun)*100
                rec.jml_kesakitan_jun = (rec.jml_sakit_jun /rec.jml_tenaga_kerja_jun)*100
                rec.jml_ratiopak_jun = (rec.jml_sakitkerja_jun /rec.jml_tenaga_kerja_jun)*100
                
            if(rec.jml_tenaga_kerja_jul !=0):
                rec.jml_kelayakan_jul = ((rec.jml_tenaga_kerja_jul - rec.jml_sakit_jul)/rec.jml_tenaga_kerja_jul)*100
                rec.jml_kesakitan_jul = (rec.jml_sakit_jul /rec.jml_tenaga_kerja_jul)*100
                rec.jml_ratiopak_jul = (rec.jml_sakitkerja_jul /rec.jml_tenaga_kerja_jul)*100
                
            if(rec.jml_tenaga_kerja_aug !=0):
                rec.jml_kelayakan_aug = ((rec.jml_tenaga_kerja_aug - rec.jml_sakit_aug)/rec.jml_tenaga_kerja_aug)*100
                rec.jml_kesakitan_aug = (rec.jml_sakit_aug /rec.jml_tenaga_kerja_aug)*100
                rec.jml_ratiopak_aug = (rec.jml_sakitkerja_aug /rec.jml_tenaga_kerja_aug)*100

            if(rec.jml_tenaga_kerja_sep !=0):
                rec.jml_kelayakan_sep = ((rec.jml_tenaga_kerja_sep - rec.jml_sakit_sep)/rec.jml_tenaga_kerja_sep)*100
                rec.jml_kesakitan_sep = (rec.jml_sakit_sep /rec.jml_tenaga_kerja_sep)*100
                rec.jml_ratiopak_sep = (rec.jml_sakitkerja_sep /rec.jml_tenaga_kerja_sep)*100

            if(rec.jml_tenaga_kerja_oct !=0):
                rec.jml_kelayakan_oct = ((rec.jml_tenaga_kerja_oct - rec.jml_sakit_oct)/rec.jml_tenaga_kerja_oct)*100
                rec.jml_kesakitan_oct = (rec.jml_sakit_oct /rec.jml_tenaga_kerja_oct)*100
                rec.jml_ratiopak_oct = (rec.jml_sakitkerja_oct /rec.jml_tenaga_kerja_oct)*100

            if(rec.jml_tenaga_kerja_nov !=0):
                rec.jml_kelayakan_nov = ((rec.jml_tenaga_kerja_nov - rec.jml_sakit_nov)/rec.jml_tenaga_kerja_nov)*100
                rec.jml_kesakitan_nov = (rec.jml_sakit_nov /rec.jml_tenaga_kerja_nov)*100
                rec.jml_ratiopak_nov = (rec.jml_sakitkerja_nov /rec.jml_tenaga_kerja_nov)*100

            if(rec.jml_tenaga_kerja_dec !=0):
                rec.jml_kelayakan_dec = ((rec.jml_tenaga_kerja_dec - rec.jml_sakit_dec)/rec.jml_tenaga_kerja_dec)*100
                rec.jml_kesakitan_dec = (rec.jml_sakit_dec /rec.jml_tenaga_kerja_dec)*100
                rec.jml_ratiopak_dec = (rec.jml_sakitkerja_dec /rec.jml_tenaga_kerja_dec)*100


            if(rec.jml_spell_jan !=0):
                rec.jml_keparahan_jan = rec.jml_absen_jan /rec.jml_spell_jan

            if(rec.jml_spell_feb !=0):
                rec.jml_keparahan_feb = rec.jml_absen_feb /rec.jml_spell_feb

            if(rec.jml_spell_mar !=0):
                rec.jml_keparahan_mar = rec.jml_absen_mar /rec.jml_spell_mar

            if(rec.jml_spell_apr !=0):
                rec.jml_keparahan_apr = rec.jml_absen_apr /rec.jml_spell_apr

            if(rec.jml_spell_may !=0):
                rec.jml_keparahan_may = rec.jml_absen_may /rec.jml_spell_may

            if(rec.jml_spell_jun !=0):
                rec.jml_keparahan_jun = rec.jml_absen_jun /rec.jml_spell_jun

            if(rec.jml_spell_jul !=0):
                rec.jml_keparahan_jul = rec.jml_absen_jul /rec.jml_spell_jul

            if(rec.jml_spell_aug !=0):
                rec.jml_keparahan_aug = rec.jml_absen_aug /rec.jml_spell_aug

            if(rec.jml_spell_sep !=0):
                rec.jml_keparahan_sep = rec.jml_absen_sep /rec.jml_spell_sep

            if(rec.jml_spell_oct !=0):
                rec.jml_keparahan_oct = rec.jml_absen_oct /rec.jml_spell_oct

            if(rec.jml_spell_nov !=0):
                rec.jml_keparahan_nov = rec.jml_absen_nov /rec.jml_spell_nov

            if(rec.jml_spell_dec !=0):
                rec.jml_keparahan_dec = rec.jml_absen_dec /rec.jml_spell_dec


            if(rec.jml_jamkerja_jan !=0):
                rec.jml_absenseverity_jan = (rec.jml_absen_jan * 1000000) / rec.jml_jamkerja_jan
                rec.jml_keseringan_jan = (rec.jml_sakit_jan*1000000)/rec.jml_jamkerja_jan
                
            if(rec.jml_jamkerja_feb !=0):
                rec.jml_absenseverity_feb = (rec.jml_absen_feb * 1000000) / rec.jml_jamkerja_feb
                rec.jml_keseringan_feb = (rec.jml_sakit_feb*1000000)/rec.jml_jamkerja_feb

            if(rec.jml_jamkerja_mar !=0):
                rec.jml_absenseverity_mar = (rec.jml_absen_mar * 1000000) / rec.jml_jamkerja_mar
                rec.jml_keseringan_mar = (rec.jml_sakit_mar*1000000)/rec.jml_jamkerja_mar

            if(rec.jml_jamkerja_apr !=0):
                rec.jml_absenseverity_apr = (rec.jml_absen_apr * 1000000) / rec.jml_jamkerja_apr
                rec.jml_keseringan_apr = (rec.jml_sakit_apr*1000000)/rec.jml_jamkerja_apr

            if(rec.jml_jamkerja_may !=0):
                rec.jml_absenseverity_may = (rec.jml_absen_may * 1000000) / rec.jml_jamkerja_may
                rec.jml_keseringan_may = (rec.jml_sakit_may*1000000)/rec.jml_jamkerja_may

            if(rec.jml_jamkerja_jun !=0):
                rec.jml_absenseverity_jun = (rec.jml_absen_jun * 1000000) / rec.jml_jamkerja_jun
                rec.jml_keseringan_jun = (rec.jml_sakit_jun*1000000)/rec.jml_jamkerja_jun

            if(rec.jml_jamkerja_jul !=0):
                rec.jml_absenseverity_jul = (rec.jml_absen_jul * 1000000) / rec.jml_jamkerja_jul
                rec.jml_keseringan_jul = (rec.jml_sakit_jul*1000000)/rec.jml_jamkerja_jul

            if(rec.jml_jamkerja_aug !=0):
                rec.jml_absenseverity_aug = (rec.jml_absen_aug * 1000000) / rec.jml_jamkerja_aug
                rec.jml_keseringan_aug = (rec.jml_sakit_aug*1000000)/rec.jml_jamkerja_aug

            if(rec.jml_jamkerja_sep !=0):
                rec.jml_absenseverity_sep = (rec.jml_absen_sep * 1000000) / rec.jml_jamkerja_sep
                rec.jml_keseringan_sep = (rec.jml_sakit_sep*1000000)/rec.jml_jamkerja_sep

            if(rec.jml_jamkerja_oct !=0):
                rec.jml_absenseverity_oct = (rec.jml_absen_oct * 1000000) / rec.jml_jamkerja_oct
                rec.jml_keseringan_oct = (rec.jml_sakit_oct*1000000)/rec.jml_jamkerja_oct

            if(rec.jml_jamkerja_nov !=0):
                rec.jml_absenseverity_nov = (rec.jml_absen_nov * 1000000) / rec.jml_jamkerja_nov
                rec.jml_keseringan_nov = (rec.jml_sakit_nov*1000000)/rec.jml_jamkerja_nov

            if(rec.jml_jamkerja_dec !=0):
                rec.jml_absenseverity_dec = (rec.jml_absen_dec * 1000000) / rec.jml_jamkerja_dec
                rec.jml_keseringan_dec = (rec.jml_sakit_dec*1000000)/rec.jml_jamkerja_dec


class  PelaporanReportingAll(models.Model):
    _name = "gag.oa.hse.pelaporan.reporting.all"
    _description = "Pelaporan jumlah pekerja per bulan"

    year = fields.Char("Tahun",required = True)

    jml_tenaga_kerja_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_tenaga_kerja_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_jamkerja_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_jamkerja_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_sakit_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakit_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_absen_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absen_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_spell_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_spell_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_sakitkerja_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_sakitkerja_nov = fields.Integer("Jan",compute="_compute_jam_kerja")    
    jml_sakitkerja_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    jml_kelayakan_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kelayakan_dec = fields.Integer("Jan",compute="_compute_jam_kerja")
    
    jml_kesakitan_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_kesakitan_dec = fields.Integer("Jan",compute="_compute_jam_kerja")
    
    jml_keseringan_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keseringan_dec = fields.Integer("Jan",compute="_compute_jam_kerja")
    
    jml_keparahan_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_keparahan_dec = fields.Integer("Jan",compute="_compute_jam_kerja")
    
    jml_absenseverity_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_absenseverity_dec = fields.Integer("Jan",compute="_compute_jam_kerja")
    
    jml_ratiopak_jan = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_feb = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_mar = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_apr = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_may = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_jun = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_jul = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_aug = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_sep = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_oct = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_nov = fields.Integer("Jan",compute="_compute_jam_kerja")
    jml_ratiopak_dec = fields.Integer("Jan",compute="_compute_jam_kerja")

    def _compute_jam_kerja(self):
        for rec in self:
            rec.jml_kelayakan_jan = 0
            rec.jml_kelayakan_feb = 0
            rec.jml_kelayakan_mar = 0
            rec.jml_kelayakan_apr = 0
            rec.jml_kelayakan_may = 0
            rec.jml_kelayakan_jun = 0
            rec.jml_kelayakan_jul = 0
            rec.jml_kelayakan_aug = 0
            rec.jml_kelayakan_sep = 0
            rec.jml_kelayakan_oct = 0
            rec.jml_kelayakan_nov = 0
            rec.jml_kelayakan_dec = 0

            rec.jml_kesakitan_jan = 0
            rec.jml_kesakitan_feb = 0
            rec.jml_kesakitan_mar = 0
            rec.jml_kesakitan_apr = 0
            rec.jml_kesakitan_may = 0
            rec.jml_kesakitan_jun = 0
            rec.jml_kesakitan_jul = 0
            rec.jml_kesakitan_aug = 0
            rec.jml_kesakitan_sep = 0
            rec.jml_kesakitan_oct = 0
            rec.jml_kesakitan_nov = 0
            rec.jml_kesakitan_dec = 0

            rec.jml_keseringan_jan = 0
            rec.jml_keseringan_feb = 0
            rec.jml_keseringan_mar = 0
            rec.jml_keseringan_apr = 0
            rec.jml_keseringan_may = 0
            rec.jml_keseringan_jun = 0
            rec.jml_keseringan_jul = 0
            rec.jml_keseringan_aug = 0
            rec.jml_keseringan_sep = 0
            rec.jml_keseringan_oct = 0
            rec.jml_keseringan_nov = 0
            rec.jml_keseringan_dec = 0

            rec.jml_keparahan_jan = 0
            rec.jml_keparahan_feb = 0
            rec.jml_keparahan_mar = 0
            rec.jml_keparahan_apr = 0
            rec.jml_keparahan_may = 0
            rec.jml_keparahan_jun = 0
            rec.jml_keparahan_jul = 0
            rec.jml_keparahan_aug = 0
            rec.jml_keparahan_sep = 0
            rec.jml_keparahan_oct = 0
            rec.jml_keparahan_nov = 0
            rec.jml_keparahan_dec = 0

            rec.jml_absenseverity_jan = 0
            rec.jml_absenseverity_feb = 0
            rec.jml_absenseverity_mar = 0
            rec.jml_absenseverity_apr = 0
            rec.jml_absenseverity_may = 0
            rec.jml_absenseverity_jun = 0
            rec.jml_absenseverity_jul = 0
            rec.jml_absenseverity_aug = 0
            rec.jml_absenseverity_sep = 0
            rec.jml_absenseverity_oct = 0
            rec.jml_absenseverity_nov = 0
            rec.jml_absenseverity_dec = 0
            
            rec.jml_ratiopak_jan = 0
            rec.jml_ratiopak_feb = 0
            rec.jml_ratiopak_mar = 0
            rec.jml_ratiopak_apr = 0
            rec.jml_ratiopak_may = 0
            rec.jml_ratiopak_jun = 0
            rec.jml_ratiopak_jul = 0
            rec.jml_ratiopak_aug = 0
            rec.jml_ratiopak_sep = 0
            rec.jml_ratiopak_oct = 0
            rec.jml_ratiopak_nov = 0
            rec.jml_ratiopak_dec = 0


            rec.jml_tenaga_kerja_jan = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','1'),('year', '=',rec.year)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_feb = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','2'),('year', '=',rec.year)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_mar = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','3'),('year', '=',rec.year)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_apr = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','4'),('year', '=',rec.year)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_may = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','5'),('year', '=',rec.year)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_jun = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','6'),('year', '=',rec.year)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_jul = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','7'),('year', '=',rec.year)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_aug = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','8'),('year', '=',rec.year)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_sep = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','9'),('year', '=',rec.year)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_oct = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','10'),('year', '=',rec.year)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_nov = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','11'),('year', '=',rec.year)]).mapped('total_pekerja')))
            rec.jml_tenaga_kerja_dec = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','12'),('year', '=',rec.year)]).mapped('total_pekerja')))
            
            rec.jml_jamkerja_jan = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','1'),('year', '=',rec.year)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_feb = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','2'),('year', '=',rec.year)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_mar = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','3'),('year', '=',rec.year)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_apr = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','4'),('year', '=',rec.year)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_may = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','5'),('year', '=',rec.year)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_jun = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','6'),('year', '=',rec.year)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_jul = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','7'),('year', '=',rec.year)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_aug = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','8'),('year', '=',rec.year)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_sep = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','9'),('year', '=',rec.year)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_oct = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','10'),('year', '=',rec.year)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_nov = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','11'),('year', '=',rec.year)]).mapped('total_jamkerja')))
            rec.jml_jamkerja_dec = float(sum(self.env['gag.oa.hse.pelaporan.pekerja'].search([('month','=','12'),('year', '=',rec.year)]).mapped('total_jamkerja')))

            rec.jml_sakit_jan = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','1'),('year', '=',rec.year)]).mapped('total_sakit')))
            rec.jml_sakit_feb = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','2'),('year', '=',rec.year)]).mapped('total_sakit')))
            rec.jml_sakit_mar = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','3'),('year', '=',rec.year)]).mapped('total_sakit')))
            rec.jml_sakit_apr = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','4'),('year', '=',rec.year)]).mapped('total_sakit')))
            rec.jml_sakit_may = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','5'),('year', '=',rec.year)]).mapped('total_sakit')))
            rec.jml_sakit_jun = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','6'),('year', '=',rec.year)]).mapped('total_sakit')))
            rec.jml_sakit_jul = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','7'),('year', '=',rec.year)]).mapped('total_sakit')))
            rec.jml_sakit_aug = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','8'),('year', '=',rec.year)]).mapped('total_sakit')))
            rec.jml_sakit_sep = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','9'),('year', '=',rec.year)]).mapped('total_sakit')))
            rec.jml_sakit_oct = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','10'),('year', '=',rec.year)]).mapped('total_sakit')))
            rec.jml_sakit_nov = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','11'),('year', '=',rec.year)]).mapped('total_sakit')))
            rec.jml_sakit_dec = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','12'),('year', '=',rec.year)]).mapped('total_sakit')))

            rec.jml_absen_jan = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','1'),('year', '=',rec.year)]).mapped('total_absen')))
            rec.jml_absen_feb = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','2'),('year', '=',rec.year)]).mapped('total_absen')))
            rec.jml_absen_mar = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','3'),('year', '=',rec.year)]).mapped('total_absen')))
            rec.jml_absen_apr = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','4'),('year', '=',rec.year)]).mapped('total_absen')))
            rec.jml_absen_may = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','5'),('year', '=',rec.year)]).mapped('total_absen')))
            rec.jml_absen_jun = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','6'),('year', '=',rec.year)]).mapped('total_absen')))
            rec.jml_absen_jul = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','7'),('year', '=',rec.year)]).mapped('total_absen')))
            rec.jml_absen_aug = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','8'),('year', '=',rec.year)]).mapped('total_absen')))
            rec.jml_absen_sep = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','9'),('year', '=',rec.year)]).mapped('total_absen')))
            rec.jml_absen_oct = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','10'),('year', '=',rec.year)]).mapped('total_absen')))
            rec.jml_absen_nov = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','11'),('year', '=',rec.year)]).mapped('total_absen')))
            rec.jml_absen_dec = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','12'),('year', '=',rec.year)]).mapped('total_absen')))
            
            rec.jml_spell_jan = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','1'),('year', '=',rec.year)]).mapped('total_spell')))
            rec.jml_spell_feb = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','2'),('year', '=',rec.year)]).mapped('total_spell')))
            rec.jml_spell_mar = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','3'),('year', '=',rec.year)]).mapped('total_spell')))
            rec.jml_spell_apr = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','4'),('year', '=',rec.year)]).mapped('total_spell')))
            rec.jml_spell_may = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','5'),('year', '=',rec.year)]).mapped('total_spell')))
            rec.jml_spell_jun = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','6'),('year', '=',rec.year)]).mapped('total_spell')))
            rec.jml_spell_jul = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','7'),('year', '=',rec.year)]).mapped('total_spell')))
            rec.jml_spell_aug = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','8'),('year', '=',rec.year)]).mapped('total_spell')))
            rec.jml_spell_sep = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','9'),('year', '=',rec.year)]).mapped('total_spell')))
            rec.jml_spell_oct = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','10'),('year', '=',rec.year)]).mapped('total_spell')))
            rec.jml_spell_nov = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','11'),('year', '=',rec.year)]).mapped('total_spell')))
            rec.jml_spell_dec = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','12'),('year', '=',rec.year)]).mapped('total_spell')))
            
            rec.jml_sakitkerja_jan = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','1'),('year', '=',rec.year)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_feb = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','2'),('year', '=',rec.year)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_mar = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','3'),('year', '=',rec.year)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_apr = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','4'),('year', '=',rec.year)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_may = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','5'),('year', '=',rec.year)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_jun = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','6'),('year', '=',rec.year)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_jul = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','7'),('year', '=',rec.year)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_aug = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','8'),('year', '=',rec.year)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_sep = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','9'),('year', '=',rec.year)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_oct = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','10'),('year', '=',rec.year)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_nov = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','11'),('year', '=',rec.year)]).mapped('total_sakitkerja')))
            rec.jml_sakitkerja_dec = float(sum(self.env['gag.oa.hse.pelaporan.kesehatan'].search([('month','=','12'),('year', '=',rec.year)]).mapped('total_sakitkerja')))


            if(rec.jml_tenaga_kerja_jan !=0):
                rec.jml_kelayakan_jan = ((rec.jml_tenaga_kerja_jan - rec.jml_sakit_jan)/rec.jml_tenaga_kerja_jan)*100
                rec.jml_kesakitan_jan = (rec.jml_sakit_jan /rec.jml_tenaga_kerja_jan)*100
                rec.jml_ratiopak_jan = (rec.jml_sakitkerja_jan /rec.jml_tenaga_kerja_jan)*100
                
            if(rec.jml_tenaga_kerja_feb !=0):
                rec.jml_kelayakan_feb = ((rec.jml_tenaga_kerja_feb - rec.jml_sakit_feb)/rec.jml_tenaga_kerja_feb)*100
                rec.jml_kesakitan_feb = (rec.jml_sakit_feb /rec.jml_tenaga_kerja_feb)*100
                rec.jml_ratiopak_feb = (rec.jml_sakitkerja_feb /rec.jml_tenaga_kerja_feb)*100
                
            if(rec.jml_tenaga_kerja_mar !=0):
                rec.jml_kelayakan_mar = ((rec.jml_tenaga_kerja_mar - rec.jml_sakit_mar)/rec.jml_tenaga_kerja_mar)*100
                rec.jml_kesakitan_mar = (rec.jml_sakit_mar /rec.jml_tenaga_kerja_mar)*100
                rec.jml_ratiopak_mar = (rec.jml_sakitkerja_mar /rec.jml_tenaga_kerja_mar)*100

            if(rec.jml_tenaga_kerja_apr !=0):
                rec.jml_kelayakan_apr = ((rec.jml_tenaga_kerja_apr - rec.jml_sakit_apr)/rec.jml_tenaga_kerja_apr)*100
                rec.jml_kesakitan_apr = (rec.jml_sakit_apr /rec.jml_tenaga_kerja_apr)*100
                rec.jml_ratiopak_apr = (rec.jml_sakitkerja_apr /rec.jml_tenaga_kerja_apr)*100

            if(rec.jml_tenaga_kerja_may !=0):
                rec.jml_kelayakan_may = ((rec.jml_tenaga_kerja_may - rec.jml_sakit_may)/rec.jml_tenaga_kerja_may)*100
                rec.jml_kesakitan_may = (rec.jml_sakit_may /rec.jml_tenaga_kerja_may)*100
                rec.jml_ratiopak_may = (rec.jml_sakitkerja_may /rec.jml_tenaga_kerja_may)*100

            if(rec.jml_tenaga_kerja_jun !=0):
                rec.jml_kelayakan_jun = ((rec.jml_tenaga_kerja_jun - rec.jml_sakit_jun)/rec.jml_tenaga_kerja_jun)*100
                rec.jml_kesakitan_jun = (rec.jml_sakit_jun /rec.jml_tenaga_kerja_jun)*100
                rec.jml_ratiopak_jun = (rec.jml_sakitkerja_jun /rec.jml_tenaga_kerja_jun)*100
                
            if(rec.jml_tenaga_kerja_jul !=0):
                rec.jml_kelayakan_jul = ((rec.jml_tenaga_kerja_jul - rec.jml_sakit_jul)/rec.jml_tenaga_kerja_jul)*100
                rec.jml_kesakitan_jul = (rec.jml_sakit_jul /rec.jml_tenaga_kerja_jul)*100
                rec.jml_ratiopak_jul = (rec.jml_sakitkerja_jul /rec.jml_tenaga_kerja_jul)*100
                
            if(rec.jml_tenaga_kerja_aug !=0):
                rec.jml_kelayakan_aug = ((rec.jml_tenaga_kerja_aug - rec.jml_sakit_aug)/rec.jml_tenaga_kerja_aug)*100
                rec.jml_kesakitan_aug = (rec.jml_sakit_aug /rec.jml_tenaga_kerja_aug)*100
                rec.jml_ratiopak_aug = (rec.jml_sakitkerja_aug /rec.jml_tenaga_kerja_aug)*100

            if(rec.jml_tenaga_kerja_sep !=0):
                rec.jml_kelayakan_sep = ((rec.jml_tenaga_kerja_sep - rec.jml_sakit_sep)/rec.jml_tenaga_kerja_sep)*100
                rec.jml_kesakitan_sep = (rec.jml_sakit_sep /rec.jml_tenaga_kerja_sep)*100
                rec.jml_ratiopak_sep = (rec.jml_sakitkerja_sep /rec.jml_tenaga_kerja_sep)*100

            if(rec.jml_tenaga_kerja_oct !=0):
                rec.jml_kelayakan_oct = ((rec.jml_tenaga_kerja_oct - rec.jml_sakit_oct)/rec.jml_tenaga_kerja_oct)*100
                rec.jml_kesakitan_oct = (rec.jml_sakit_oct /rec.jml_tenaga_kerja_oct)*100
                rec.jml_ratiopak_oct = (rec.jml_sakitkerja_oct /rec.jml_tenaga_kerja_oct)*100

            if(rec.jml_tenaga_kerja_nov !=0):
                rec.jml_kelayakan_nov = ((rec.jml_tenaga_kerja_nov - rec.jml_sakit_nov)/rec.jml_tenaga_kerja_nov)*100
                rec.jml_kesakitan_nov = (rec.jml_sakit_nov /rec.jml_tenaga_kerja_nov)*100
                rec.jml_ratiopak_nov = (rec.jml_sakitkerja_nov /rec.jml_tenaga_kerja_nov)*100

            if(rec.jml_tenaga_kerja_dec !=0):
                rec.jml_kelayakan_dec = ((rec.jml_tenaga_kerja_dec - rec.jml_sakit_dec)/rec.jml_tenaga_kerja_dec)*100
                rec.jml_kesakitan_dec = (rec.jml_sakit_dec /rec.jml_tenaga_kerja_dec)*100
                rec.jml_ratiopak_dec = (rec.jml_sakitkerja_dec /rec.jml_tenaga_kerja_dec)*100


            if(rec.jml_spell_jan !=0):
                rec.jml_keparahan_jan = rec.jml_absen_jan /rec.jml_spell_jan

            if(rec.jml_spell_feb !=0):
                rec.jml_keparahan_feb = rec.jml_absen_feb /rec.jml_spell_feb

            if(rec.jml_spell_mar !=0):
                rec.jml_keparahan_mar = rec.jml_absen_mar /rec.jml_spell_mar

            if(rec.jml_spell_apr !=0):
                rec.jml_keparahan_apr = rec.jml_absen_apr /rec.jml_spell_apr

            if(rec.jml_spell_may !=0):
                rec.jml_keparahan_may = rec.jml_absen_may /rec.jml_spell_may

            if(rec.jml_spell_jun !=0):
                rec.jml_keparahan_jun = rec.jml_absen_jun /rec.jml_spell_jun

            if(rec.jml_spell_jul !=0):
                rec.jml_keparahan_jul = rec.jml_absen_jul /rec.jml_spell_jul

            if(rec.jml_spell_aug !=0):
                rec.jml_keparahan_aug = rec.jml_absen_aug /rec.jml_spell_aug

            if(rec.jml_spell_sep !=0):
                rec.jml_keparahan_sep = rec.jml_absen_sep /rec.jml_spell_sep

            if(rec.jml_spell_oct !=0):
                rec.jml_keparahan_oct = rec.jml_absen_oct /rec.jml_spell_oct

            if(rec.jml_spell_nov !=0):
                rec.jml_keparahan_nov = rec.jml_absen_nov /rec.jml_spell_nov

            if(rec.jml_spell_dec !=0):
                rec.jml_keparahan_dec = rec.jml_absen_dec /rec.jml_spell_dec


            if(rec.jml_jamkerja_jan !=0):
                rec.jml_absenseverity_jan = (rec.jml_absen_jan * 1000000) / rec.jml_jamkerja_jan
                rec.jml_keseringan_jan = (rec.jml_sakit_jan*1000000)/rec.jml_jamkerja_jan
                
            if(rec.jml_jamkerja_feb !=0):
                rec.jml_absenseverity_feb = (rec.jml_absen_feb * 1000000) / rec.jml_jamkerja_feb
                rec.jml_keseringan_feb = (rec.jml_sakit_feb*1000000)/rec.jml_jamkerja_feb

            if(rec.jml_jamkerja_mar !=0):
                rec.jml_absenseverity_mar = (rec.jml_absen_mar * 1000000) / rec.jml_jamkerja_mar
                rec.jml_keseringan_mar = (rec.jml_sakit_mar*1000000)/rec.jml_jamkerja_mar

            if(rec.jml_jamkerja_apr !=0):
                rec.jml_absenseverity_apr = (rec.jml_absen_apr * 1000000) / rec.jml_jamkerja_apr
                rec.jml_keseringan_apr = (rec.jml_sakit_apr*1000000)/rec.jml_jamkerja_apr

            if(rec.jml_jamkerja_may !=0):
                rec.jml_absenseverity_may = (rec.jml_absen_may * 1000000) / rec.jml_jamkerja_may
                rec.jml_keseringan_may = (rec.jml_sakit_may*1000000)/rec.jml_jamkerja_may

            if(rec.jml_jamkerja_jun !=0):
                rec.jml_absenseverity_jun = (rec.jml_absen_jun * 1000000) / rec.jml_jamkerja_jun
                rec.jml_keseringan_jun = (rec.jml_sakit_jun*1000000)/rec.jml_jamkerja_jun

            if(rec.jml_jamkerja_jul !=0):
                rec.jml_absenseverity_jul = (rec.jml_absen_jul * 1000000) / rec.jml_jamkerja_jul
                rec.jml_keseringan_jul = (rec.jml_sakit_jul*1000000)/rec.jml_jamkerja_jul

            if(rec.jml_jamkerja_aug !=0):
                rec.jml_absenseverity_aug = (rec.jml_absen_aug * 1000000) / rec.jml_jamkerja_aug
                rec.jml_keseringan_aug = (rec.jml_sakit_aug*1000000)/rec.jml_jamkerja_aug

            if(rec.jml_jamkerja_sep !=0):
                rec.jml_absenseverity_sep = (rec.jml_absen_sep * 1000000) / rec.jml_jamkerja_sep
                rec.jml_keseringan_sep = (rec.jml_sakit_sep*1000000)/rec.jml_jamkerja_sep

            if(rec.jml_jamkerja_oct !=0):
                rec.jml_absenseverity_oct = (rec.jml_absen_oct * 1000000) / rec.jml_jamkerja_oct
                rec.jml_keseringan_oct = (rec.jml_sakit_oct*1000000)/rec.jml_jamkerja_oct

            if(rec.jml_jamkerja_nov !=0):
                rec.jml_absenseverity_nov = (rec.jml_absen_nov * 1000000) / rec.jml_jamkerja_nov
                rec.jml_keseringan_nov = (rec.jml_sakit_nov*1000000)/rec.jml_jamkerja_nov

            if(rec.jml_jamkerja_dec !=0):
                rec.jml_absenseverity_dec = (rec.jml_absen_dec * 1000000) / rec.jml_jamkerja_dec
                rec.jml_keseringan_dec = (rec.jml_sakit_dec*1000000)/rec.jml_jamkerja_dec