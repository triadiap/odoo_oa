# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from datetime import datetime

class PercentageMachineCondition(models.Model):
    _name = 'oa.machine.condition'
    _description = "Set Point and Percentage Of Machine Condition Report"
    _auto = False

    # Fields corresponding to the SQL query columns
    equipment_info = fields.Char(string='Equipment Info')  # VARCHAR for equipment_info
    readiness = fields.Char(string='Siap')  # VARCHAR for readiness
    production_min = fields.Char(string='Prod(Min)')  # VARCHAR for production_min
    qty_backup_max = fields.Integer(string='Cad(Min)')  # INTEGER for qty_backup_max
    qty_repair_max = fields.Char(string='Rep(Max)')  # VARCHAR for qty_repair_max
    percentage_ma = fields.Float(string='%MA')  # FLOAT for percentage_ma
    percentage_we = fields.Float(string='%WE')  # FLOAT for percentage_we
    year = fields.Char(string='Year')  # VARCHAR for year
    jan = fields.Float(string='Jan')  # FLOAT for jan
    feb = fields.Float(string='Feb')  # FLOAT for feb
    mar = fields.Float(string='Mar')  # FLOAT for mar
    apr = fields.Float(string='Apr')  # FLOAT for apr
    may = fields.Float(string='May')  # FLOAT for may
    jun = fields.Float(string='Jun')  # FLOAT for jun
    jul = fields.Float(string='Jul')  # FLOAT for jul
    aug = fields.Float(string='Aug')  # FLOAT for aug
    sep = fields.Float(string='Sep')  # FLOAT for sep
    oct = fields.Float(string='Oct')  # FLOAT for oct
    nov = fields.Float(string='Nov')  # FLOAT for nov
    dec = fields.Float(string='Dec')  # FLOAT for dec

    # Override the init method to create the view
    def init(self):
        # Drop the view if it already exists to refresh it
        tools.drop_view_if_exists(self._cr, 'oa_machine_condition')

        # Enable tablefunc extension if not already enabled
        self._cr.execute("CREATE EXTENSION IF NOT EXISTS tablefunc;")

        # Create the view using crosstab to pivot the months into columns
        self._cr.execute("""
                CREATE OR REPLACE VIEW oa_machine_condition AS
                SELECT *
                FROM crosstab(
                    $$
                    SELECT
                        row_number() OVER() as id,
                        CONCAT(d.name, ' - ', d.asset_number) AS equipment_info,
                        setpoint_readiness AS readiness,
                        setpoint_production AS production_min,
                        setpoint_backup AS qty_backup_max,
                        setpoint_repair AS qty_repair_max,
                        setpoint_ma AS percentage_ma,
                        setpoint_we AS percentage_we,
                        year_setpoint AS year,
                        TO_CHAR(c.report_date, 'Mon') AS month,
                        (c.plan_hour - c.total_breakdown_time) / SUM(c.plan_hour) OVER (PARTITION BY c.equipment_id) * 100 AS machine_availibility
                    FROM oa_setpoint_availibility m
                    JOIN oa_master_equipment d ON m.name = d.id
                    JOIN oa_equipment_maintenance c ON m.name = c.equipment_id
                    WHERE c.report_date BETWEEN '2024-01-01' AND '2024-12-31'
                    GROUP BY month, CONCAT(d.name, ' - ', d.asset_number), year, readiness, production_min, qty_backup_max, qty_repair_max, percentage_ma, percentage_we, c.plan_hour, c.total_breakdown_time, c.equipment_id
                    ORDER BY CONCAT(d.name, ' - ', d.asset_number), month
                    $$,
                    $$ VALUES ('Jan'), ('Feb'), ('Mar'), ('Apr'), ('May'), ('Jun'), 
                              ('Jul'), ('Aug'), ('Sep'), ('Oct'), ('Nov'), ('Dec') $$
                ) AS monthly_trend (
                    id INTEGER,
                    equipment_info VARCHAR,
                    readiness VARCHAR,
                    production_min VARCHAR,
                    qty_backup_max INTEGER,
                    qty_repair_max VARCHAR,
                    percentage_ma FLOAT,
                    percentage_we FLOAT,
                    year VARCHAR,
                    jan FLOAT,
                    feb FLOAT,
                    mar FLOAT,
                    apr FLOAT,
                    may FLOAT,
                    jun FLOAT,
                    jul FLOAT,
                    aug FLOAT,
                    sep FLOAT,
                    oct FLOAT,
                    nov FLOAT,
                    dec FLOAT
                );
            """)


