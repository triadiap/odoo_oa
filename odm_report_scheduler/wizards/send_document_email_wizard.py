# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import re


class SendDocumentEmailWizard(models.TransientModel):
    _name = "odm.send.mail.wizard"
    _description = "Wizard for sending document via email"

    attachment_id = fields.Many2one(
        "odm.report.attachments", string="Attachment", readonly=True)

    email_to_ids = fields.Many2many(
        "docmon.mail.recipient",
        'wizard_mail_to_rel',  # nama tabel relasi khusus
        'wizard_id',  # kolom yang mengarah ke wizard
        'recipient_id',  # kolom yang mengarah ke mail.recipient
        string="Send To",
        required=True
    )

    email_cc_ids = fields.Many2many(
        "docmon.mail.recipient",
        'wizard_mail_cc_rel',  # tabel relasi berbeda
        'wizard_id',
        'recipient_id',
        string="CC"
    )

    subject = fields.Char("Subject", required=True)
    body = fields.Html("Body Message")
    file_name = fields.Char("File Name", readonly=True)
    file_data = fields.Binary(string="Attachment", readonly=True)

    def action_send_email(self):
        """Send email via direct SMTP using data from wizard."""
        rec = self.attachment_id

        if not rec:
            raise ValidationError("Origin document not found.")

        # GET MAIL SERVER
        mail_server = self.env['docmon.mail.server'].search([
            ('smtp_port', '=', 465),
            ('active', '=', 'true'),
            ('smtp_encryption', '=', 'ssl')
        ], limit=1)

        if not mail_server:
            raise ValidationError("No outgoing mail server configured!")

        smtp_server = mail_server.smtp_host
        smtp_port = mail_server.smtp_port
        smtp_user = mail_server.smtp_user
        smtp_password = mail_server.smtp_pass

        email_from = smtp_user

        # EMAIL MESSAGE
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = email_from

        # ==========================
        # FIX: FORCE FLUSH M2M FIELDS
        # ==========================
        self.flush()
        self.invalidate_cache()
        
        # Convert Many2many → list string email
        email_to_list = [r.name for r in self.email_to_ids]
        email_cc_list = [r.name for r in self.email_cc_ids]

        msg['To'] = ", ".join(email_to_list)
        if email_cc_list:
            msg['Cc'] = ", ".join(email_cc_list)

        msg.attach(MIMEText(self.body, 'html'))

        # ATTACHMENT
        if self.file_data:
            attachment = MIMEApplication(base64.b64decode(self.file_data))
            attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=self.file_name or 'document.pdf'
            )
            msg.attach(attachment)

        # SEND EMAIL
        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_user, smtp_password)
                server.sendmail(
                    email_from,
                    email_to_list + email_cc_list,
                    msg.as_string()
                )
        except Exception as e:
            raise ValidationError("Error sending email: %s" % str(e))

        # SAVE LOG
        self.env["odm.email.log"].create({
            "attachment_id": rec.id,
            "email_to": ", ".join(email_to_list),
            "email_cc": ", ".join(email_cc_list) if email_cc_list else "",
            "subject": self.subject,
            "body": self.body,
            "file_name": self.file_name,
            "file_data": self.file_data,
            "user_id": self.env.user.id,
        })

        # SUCCESS NOTIFICATION
        title = _("Email Sent Successfully!")
        message = _("Email telah berhasil dikirim")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'sticky': False,
                'type': 'success',  # hijau
            }
        }
