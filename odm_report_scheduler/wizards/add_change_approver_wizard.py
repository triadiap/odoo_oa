# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import re

class AddChangeApproverWizard(models.TransientModel):
    _name = "odm.approver.wizard"
    _description = "Wizard for add or change approver"

    submission_id = fields.Many2one("odm.report.submission", string="Configuration", readonly=True)
    need_approval = fields.Boolean(string="Need Approval", required=True)
    approver_name = fields.Many2one("res.users",string="Approver Names")

    def addchange_approver(self):
        rec = self.submission_id

        if not rec:
            raise ValidationError("Origin setting is not found.")

        rec.write({
            "is_need_approval": self.need_approval,
            "name_approver": self.approver_name.id
        })

        # SUCCESS NOTIFICATION
        title = _("Approver Setting")
        message = _("Approver Has Been Updated For This Report")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'sticky': False,
                'type': 'success',  # hijau
                'next': {
                    'type': 'ir.actions.act_window_close'
                }
            }
        }

