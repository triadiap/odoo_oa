# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ReportingType(models.Model):
    _name = 'oa.reporting.type'
    _description = 'Auto Reporting Type Master Data'

    name = fields.Char(string="Document Type")

    def unlink(self):
        for rec in self:
            if self.env['odm.document.configuration'].search_count([('document_type', '=', rec.id)]):
                raise UserError(_('You cannot delete document type "%s" because it is still being used in report configuration.') % (rec.name,))
        return super(ReportingType, self).unlink()

    def action_delete_selected(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Confirm Deletion'),
            'res_model': 'reporting.type.delete.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_ids': self.ids},
        }
