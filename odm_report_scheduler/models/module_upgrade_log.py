# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import re


class ModuleUpgradeLog(models.Model):
    _name = 'module.upgrade.log'
    _description = 'Module Upgrade Log'
    _order = 'upgrade_datetime desc'

    module_name = fields.Char(string="Module Name", required=True)
    old_version = fields.Char(string="Old Version")
    new_version = fields.Char(string="New Version")
    upgraded_by = fields.Many2one('res.users', string="Upgraded By")
    upgrade_datetime = fields.Datetime(string="Upgrade Time")
    status = fields.Selection([
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string="Status")
    error_message = fields.Text(string="Error Message")
    module_summary = fields.Char(string="Summary")
    module_description = fields.Text(string="Description")

    def name_get(self):
        result = []
        for record in self:
            name = f"({record.module_name}) - {record.new_version} - {record.upgrade_datetime}"
            result.append((record.id, name))  # or any other meaningful field
        return result
