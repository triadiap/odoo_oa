# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta

class AddActionRemarksWizard(models.TransientModel):
    _name = 'odm.remarks.wizard'
    _description = 'Add Action Remarks'

    submission_id = fields.Many2one("odm.report.submission", string="Configuration", readonly=True)
    action_remarks = fields.Text(string="Remarks", required=True)
    move_notes = fields.Text(string="Move Notes")

    def action_confirm(self):
        rec = self.submission_id
        if not rec:
            raise ValidationError("Origin setting is not found.")

        if self.move_notes == "backtoreview":
            rec.write({
                "state": 'pending',
                "status_color": 2
            })
        elif self.move_notes == "setasapproved":
            rec.write({
                "state": 'approved',
                "status_color": 2
            })
        elif self.move_notes == "setasdraft":
            rec.write({
                "state": 'draft',
                "status_color": 2
            })
        # 🔥 Kirim remarks ke chatter
        body_message = f"""
            <b>Action Remarks:</b><br/>
            {self.action_remarks}
            """

        rec.message_post(
            body=body_message,
            message_type='comment',
            subtype_xmlid='mail.mt_comment'
        )

        return {'type': 'ir.actions.act_window_close'}


