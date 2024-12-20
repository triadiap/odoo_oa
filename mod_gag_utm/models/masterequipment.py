# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class MasterDataEquipment(models.Model):
    _name = 'oa.master.equipment'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Office Automation Utility And Maintenance Equipment Master Data'

    name = fields.Char(string="Nama Mesin / Perlengkapan", required=True, tracking=True)
    manuf_year = fields.Char(string="Tahun Pembuatan", tracking=True)
    equipment_model = fields.Char(string="Model", tracking=True)
    equipment_capacity = fields.Float(string="Ampere", tracking=True)
    equipment_capacity_input = fields.Float(string="Voltage", tracking=True)
    general_maintenance_frequency = fields.Float(string="Frekuensi (Hari)",tracking=True)
    serial_number = fields.Char(string="Nomor Seri", tracking=True)
    equip_preventive_duration = fields.Integer(string="Maintenance Frequency (Hari)")
    equip_frequency_maintenance = fields.Integer(string="Durasi Maintenance")
    equipment_desc = fields.Text(string="Deskripsi", tracking=True)
    brand_name = fields.Char(string="Merek", tracking=True)
    group_id = fields.Many2one('point.group', string="Asset Group", required=True, tracking=True)
    location_id = fields.Many2one('msdata.location', string="Lokasi", tracking=True,required=True)
    asset_number = fields.Char(string='Nomor Asset',tracking=True)
    pkt_number = fields.Char(string='Code No', tracking=True)
    id_detail_maintenance = fields.One2many('oa.detailed.maintenance','maintenance_detail_id',string='Maintenance')
    product_id = fields.Char(string="Product ID",tracking=True)
    rated_output = fields.Char(string="Rated Output",tracking=True)
    equipment_weight = fields.Char(string="Weight (Kg)",tracking=True)
    equipment_date = fields.Date(string="Tanggal Pembuatan (Opsional)", tracking=True)
    equipment_power = fields.Float(string="Power (Hp)",tracking=True)
    equipment_rated_engine = fields.Char(string="Rated Engine/ RPM",tracking=True)
    equipment_engine_power = fields.Char(string="Engine Power",tracking=True)
    equipment_calibration_nr = fields.Char(string="Calibration NR",tracking=True)
    equipment_engine_number = fields.Char(string="Engine Number",tracking=True)
    equipment_trans_axle = fields.Char(string="Trans Axle",tracking=True)
    equipment_dimension = fields.Char(string="Dimension",tracking=True)
    # ---------------------------------------------------------------------------------------------
    btn_fix_routine_schedule = fields.Boolean(string="Schedule Perawatan Tetap ?", default=False)
    btn_set_schedule = fields.Boolean(compute='_compute_btn_visibility', store=False)


    @api.onchange('btn_fix_routine_schedule')
    def _compute_btn_visibility(self):
        for record in self:
            record.btn_set_schedule = record.btn_fix_routine_schedule


    def name_get(self):
        result = []
        for record in self:
            namadanassetnumber = f"{record.asset_number} - {record.name}"
            result.append((record.id, namadanassetnumber))  # or any other meaningful field
        return result

    @api.model
    def create(self, vals):
        if 'serial_number' in vals:
            domain = [
                ('asset_number', '=', vals['asset_number']),
                ('name', '=', vals['name'])
            ]
            existing_record = self.search(domain)
            if existing_record:
                raise ValidationError(
                    'Selected Serial Number "{}" is already exists. Please choose a different one.'.format(vals['asset_number']))
        return super(MasterDataEquipment, self).create(vals)


    @api.onchange('group_id')
    def _onchange_field_a_id(self):
        for child in self.id_detail_maintenance:
            child.name.group_id = self.group_id  # Example: set the same value


class DetailMaintenanceActivity(models.Model):
    _name="oa.detailed.maintenance"
    _description = "Detailed Maintenance By Checkpoint and Type"

    maintenance_detail_id = fields.Many2one('oa.master.equipment',string="Maintenance Detail")
    id_maintenance_type = fields.Selection([
        ('top_over_haul', 'TOP OVER HAUL'),
        ('minor_over_haul', 'MINOR OVER HAUL'),
        ('general_over_haul', 'GENERAL OVER HAUL'),
        ('services', 'SERVICES'),
        ('greasing', 'GREASING'),
        ('body_repair', 'BODY REPAIR'),
        ('corrective_maintenance', 'CORRECTIVE MAINTENANCE'),
        ('breakdown_maintenance', 'BREAKDOWN MAINTENANCE')
    ], default="top_over_haul", string="Status", tracking=True)
    name = fields.Many2one('msdata.checkpoints', string='Sub Equipment')
    maintenance_freq = fields.Float(string="Frequency",required=True,tracking=True)
    part_name = fields.Text(string="Nama Part",tracking=True)
    unit_of_measure = fields.Selection([
        ('hour_meter','Hour Meter (HM)'),
        ('kilometer','Kilometer (Km)'),
        ('meter','Meter (M)')
    ], default='hour_meter',string="Satuan",tracking=True)
