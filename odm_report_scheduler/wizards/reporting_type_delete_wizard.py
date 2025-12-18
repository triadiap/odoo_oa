# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ReportingTypeDeleteWizard(models.TransientModel):
    _name = 'reporting.type.delete.wizard'
    _description = 'Reporting Type Delete Wizard'

    def action_confirm_delete(self):
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            reporting_types = self.env['oa.reporting.type'].browse(active_ids)
            return reporting_types.unlink()
