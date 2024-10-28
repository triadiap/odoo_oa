# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class GetConfigPPM(models.Model):
    _name = "gag.bi.config.ppm"
    _description = "Config PPM"

    name = fields.Char(string='Config Name')
    models = fields.Many2one('ir.model',string='PPM Models')
    date_fields = fields.Many2one('ir.model.fields',string='')
    group_fields = fields.Many2one('ir.model.fields',string='Group Data')
    budget_fields = fields.Many2one('ir.model.fields',string='Budget')
    expense_fields = fields.Many2one('ir.model.fields',string='Expense')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
    ],'Status',default='draft')

    @api.onchange('models')
    def config_ppm_change_model(self):
        """Update options in field_b_id based on the selected field_a_id."""
        if self.models:
            # Search for matching records in Model C
            return {
                'domain': {
                    'date_fields':[('model_id','=',self.models.id)],
                    'group_fields':[('model_id','=',self.models.id)],
                    'budget_fields':[('model_id','=',self.models.id)],
                    'expense_fields':[('model_id','=',self.models.id)]
                }
            }
        else:
            # No value selected in field_a_id, clear field_b_id and set domain to empty
            self.models = False
            return {
                'domain': {
                    'groupid': [('model_id', '=', False)],
                    'group_fields': [('model_id', '=', False)],
                    'budget_fields': [('model_id', '=', False)],
                    'expense_fields': [('model_id', '=', False)]
                }
            } 

class GetConfigProduction(models.Model):
    _name = "gag.bi.config.production"
    _description = "Config Production"

    name = fields.Char(string='Config Name')
    models = fields.Many2one('ir.model',string='PPM Models')
    date_fields = fields.Many2one('ir.model.fields',string='')
    group_fields = fields.Many2one('ir.model.fields',string='Group Data')
    plan_fields = fields.Many2one('ir.model.fields',string='Plan')
    production_fields = fields.Many2one('ir.model.fields',string='Actual')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
    ],'Status',default='draft')

    @api.onchange('models')
    def config_production_change_model(self):
        """Update options in field_b_id based on the selected field_a_id."""
        if self.models:
            # Search for matching records in Model C
            return {
                'domain': {
                    'date_fields':[('model_id','=',self.models.id)],
                    'group_fields':[('model_id','=',self.models.id)],
                    'plan_fields':[('model_id','=',self.models.id)],
                    'production_fields':[('model_id','=',self.models.id)]
                }
            }
        else:
            # No value selected in field_a_id, clear field_b_id and set domain to empty
            self.models = False
            return {
                'domain': {
                    'groupid': [('model_id', '=', False)],
                    'group_fields': [('model_id', '=', False)],
                    'plan_fields': [('model_id', '=', False)],
                    'production_fields': [('model_id', '=', False)]
                }
            } 

class GetConfigSales(models.Model):
    _name = "gag.bi.config.sales"
    _description = "Config Sales"

    name = fields.Char(string='Config Name')
    models = fields.Many2one('ir.model',string='PPM Models')
    date_fields = fields.Many2one('ir.model.fields',string='')
    group_fields = fields.Many2one('ir.model.fields',string='Group Data')
    sales_fields = fields.Many2one('ir.model.fields',string='Sales')
    sales_condition = fields.Many2one('ir.model.fields',string='Sales Condition')
    sales_condition_selection = fields.Char('Sales Condition value')
    income_fields = fields.Many2one('ir.model.fields',string='Income')
    income_condition = fields.Many2one('ir.model.fields',string='Income Condition')
    income_condition_selection = fields.Char('Sales Condition value')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
    ],'Status',default='draft')

    @api.onchange('models')
    def config_sales_change_model(self):
        """Update options in field_b_id based on the selected field_a_id."""
        if self.models:
            # Search for matching records in Model C
            return {
                'domain': {
                    'date_fields':[('model_id','=',self.models.id)],
                    'group_fields':[('model_id','=',self.models.id)],
                    'sales_fields':[('model_id','=',self.models.id)],
                    'sales_condition':[('model_id','=',self.models.id)],
                    'sales_condition_selection':[('model_id','=',self.models.id)],
                    'income_fields':[('model_id','=',self.models.id)],
                    'income_condition':[('model_id','=',self.models.id)],
                    'income_condition_selection':[('model_id','=',self.models.id)],
                }
            }
        else:
            # No value selected in field_a_id, clear field_b_id and set domain to empty
            self.models = False
            return {
                'domain': {
                    'date_fields':[('model_id','=',False)],
                    'group_fields':[('model_id','=',False)],
                    'sales_fields':[('model_id','=',False)],
                    'sales_condition':[('model_id','=',False)],
                    'sales_condition_selection':[('model_id','=',False)],
                    'income_fields':[('model_id','=',False)],
                    'income_condition':[('model_id','=',False)],
                    'income_condition_selection':[('model_id','=',False)],
                }
            } 