# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class MasterDataEquipment(models.Model):
    _name = 'oa.master.equipment'
    _description = 'Office Automation Utility And Maintenance Equipment Master Data'

    name = fields.Char(string="Equipment Name", required=True, tracking=True)
    manuf_year = fields.Char(string="Manufacturing Year", tracking=True)
    equipment_model = fields.Char(string="Model", tracking=True)
    equipment_capacity = fields.Float(string="Maximum Capacity [Kwh]", tracking=True)
    serial_number = fields.Char(string="Serial Number", tracking=True)
    equip_preventive_duration = fields.Integer(string="Preventive Maintenance Frequency")
    equip_frequency_maintenance = fields.Integer(string="Frequency Of Maintenance Duration")
    equipment_desc = fields.Text(string="Description", tracking=True)
    brand_name = fields.Char(string="Brand Name", tracking=True)
    group_id = fields.Many2one('point.group', string="Asset Group", required=True, tracking=True)
    location_id = fields.Many2one('msdata.location', string="Location", tracking=True)
    asset_number = fields.Char(string='Asset Number',tracking=True,required=True)
    pkt_number = fields.Char(string='PKT Number', tracking=True)
    id_detail_maintenance = fields.One2many('oa.detailed.maintenance','maintenance_detail_id',string='Maintenance')


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

    def write(self, vals):
        if 'serial_number' in vals:
            domain = [
                ('asset_number', '=', vals['asset_number']),
                ('name', '=', vals['name'])
            ]
            existing_record = self.search(domain)
            if existing_record:
                raise ValidationError(
                    'Selected Serial Number "{}" is already exists. Please choose a different one.'.format(
                        vals['asset_number']))
        return super(MasterDataEquipment, self).create(vals)

    @api.onchange('group_id')
    def _onchange_field_a_id(self):
        for child in self.id_detail_maintenance:
            child.name.group_id = self.group_id  # Example: set the same value


class DetailMaintenanceActivity(models.Model):
    _name="oa.detailed.maintenance"
    _description = "Detailed Maintenance By Checkpoint and Type"

    maintenance_detail_id = fields.Many2one('oa.master.equipment',string="Maintenance Detail")
    id_maintenance_type = fields.Many2one('oa.maintenancetype.master',string="Maintenance Type",required=True,tracking=True)
    name = fields.Many2one('msdata.checkpoints', string='Sub Equipment')
    maintenance_freq = fields.Float(string="Frequency",required=True,tracking=True)
    percentage_condition_min = fields.Float(string="% Unit Condition Min", required=True, tracking=True)
    percentage_condition_max = fields.Float(string="% Unit Condition Max", required=True, tracking=True)
