# `-*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from pytz import timezone, UTC
from datetime import date, datetime, timedelta
import random
import string
import logging
import mimetypes
import base64
import re

_logger = logging.getLogger(__name__)


def convert_to_utc_naive(dt):
    if dt.tzinfo is None:
        dt = timezone('Asia/Jakarta').localize(dt)
    return dt.astimezone(UTC).replace(tzinfo=None)

class ReportSubmission(models.Model):
    _name = 'odm.report.submission'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Report submission form'
    _order = 'x_state_priority asc, deadline_time asc'

    name = fields.Char(string="Report Name", required=True, tracking=True)
    submission_freq = fields.Char(string="Frequency", required=True, tracking=True)
    doc_type = fields.Many2one("oa.reporting.type",string="Report Type",required=True,tracking=True)
    deadline_time = fields.Datetime(string='Deadline Time',required=True,tracking=True)
    report_description = fields.Html(string="Description", sanitize=False)
    conf_id = fields.Many2one("odm.document.configuration",string="Configuration_ID")
    user_owner = fields.Many2many("res.users",string="Report Owner",related="conf_id.report_ownership",readonly=True,store=False)
    status_color = fields.Integer(string="Color")
    attachment_ids = fields.One2many(
        'odm.report.attachments',
        'submission_id',
        string='Attachment List',
        tracking = True
    )
    deadline_day = fields.Selection(
        [('monday', 'Senin'),
         ('tuesday', 'Selasa'),
         ('wednesday', 'Rabu'),
         ('thursday', 'Kamis'),
         ('friday', 'Jumat'),
         ('saturday', 'Sabtu'),
         ('sunday', 'Minggu')],
        string="Deadline Day", tracking=True)
    deadline_month = fields.Selection(
        [('1', 'Januari'),
         ('2', 'Februari'),
         ('3', 'Maret'),
         ('4', 'April'),
         ('5', 'Mei'),
         ('6', 'Juni'),
         ('7', 'Juli'),
         ('8', 'Agustus'),
         ('9', 'September'),
         ('10', 'Oktober'),
         ('11', 'November'),
         ('12', 'Desember')],
        string="Deadline Month", tracking=True)
    report_pic_id = fields.Many2one("res.users", string="Report PIC", tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('completed', 'Completed')
    ], default="draft", string="Status", tracking=True)

    x_state_priority = fields.Integer(
        string='State Priority',
        compute='_compute_state_priority',
        store=True,  # MUST be stored in the database for proper sorting
        readonly=True
    )
    submission_result = fields.Selection(
        [
            ('ontime', 'On Time'),
            ('late', 'Late'),
        ],
        string="Submission Result",
        compute="_compute_submission_result",
        store=True,
        tracking=True
    )

    @api.depends('deadline_time', 'realization_date')
    def _compute_submission_result(self):
        for rec in self:
            if rec.deadline_time and rec.realization_date:
                deadline_date = rec.deadline_time.date()

                if rec.realization_date <= deadline_date:
                    rec.submission_result = 'ontime'
                else:
                    rec.submission_result = 'late'
            else:
                rec.submission_result = False

    # Compute Method: Assigns the priority number
    @api.depends('state')
    def _compute_state_priority(self):
        for record in self:
            # Completed = 1 (Highest Priority)
            if record.state == 'completed':
                record.x_state_priority = 1
            # Pending = 2
            elif record.state == 'pending':
                record.x_state_priority = 2
            # Draft = 3 (Lowest Priority)
            elif record.state == 'draft':
                record.x_state_priority = 3
            # Fallback for any other state
            else:
                record.x_state_priority = 99

    receipt_code = fields.Char(string="Report Code", tracking=True, default='Draft')
    realization_date = fields.Date(string="Realization Date", tracking=True, required=False)

    def action_complete(self):
        for record in self:
            record.state = 'completed'
            if record.receipt_code == 'Draft':
                today_str = datetime.today().strftime('%d%m%y')
                random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                record.receipt_code = f"{today_str}-{random_str}"
                record.status_color = 10

    def action_draft(self):
        self.state = 'draft'
        self.status_color = 2

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # If skip_custom_search is in context, bypass all custom logic
        if self.env.context.get('skip_custom_search'):
            return super(ReportSubmission, self).search(args, offset=offset, limit=limit, order=order, count=count)

        # For the 'Review' view, we bypass the department filter
        if self.env.context.get('is_review_view'):
            return super(ReportSubmission, self).search(args, offset=offset, limit=limit, order=order, count=count)
            
        # Explicitly filter by the current user's department
        user_id = self.env.user.id
        if user_id:
            # Ensure args is a mutable list
            if args is None:
                args = []
            elif not isinstance(args, list):
                args = list(args)
            args.append(('report_pic_id', '=', user_id))

        all_user_records = super(ReportSubmission, self).search(args, order='deadline_time asc')

        if not all_user_records:
            return super(ReportSubmission, self).search([('id', '=', 0)], count=count)

        # We want to show all completed records + the single closest upcoming record for each configuration.
        visible_submission_ids = []
        processed_conf_ids_for_upcoming = set()
        now = datetime.now()

        # Separate records
        completed_records = all_user_records.filtered(lambda r: r.state == 'completed')
        pending_records = all_user_records.filtered(lambda r: r.state == 'pending')
        # Upcoming records should only be in the 'draft' state.
        upcoming_records = all_user_records.filtered(lambda r: r.state == 'draft' and r.deadline_time >= now)

        # Add all completed records to the visible list
        visible_submission_ids.extend(completed_records.ids)
        visible_submission_ids.extend(pending_records.ids)

        # Find the closest upcoming for each conf_id from the remaining records
        for submission in upcoming_records:
            conf_id = submission.conf_id.id
            # Since the list is sorted by deadline_time, the first one we see is the closest
            if conf_id not in processed_conf_ids_for_upcoming:
                visible_submission_ids.append(submission.id)
                processed_conf_ids_for_upcoming.add(conf_id)

        # Build the final domain to filter by our calculated IDs, respecting original filters
        final_domain = args + [('id', 'in', visible_submission_ids)]

        if count:
            return super(ReportSubmission, self).search(final_domain, count=True)

        return super(ReportSubmission, self).search(final_domain, offset=offset, limit=limit, order=order, count=count)



    def generate_report(self,configuration_id,name,submission_freq,doc_type,deadline_time,deadline_day,deadline_month,department_id=None):
        # Konversi deadline_time string ke datetime object
        if isinstance(deadline_time, str):
            deadline_time = datetime.strptime(deadline_time, "%Y-%m-%d %H:%M:%S")

        # Konversi ke UTC jika ingin disimpan dalam UTC
        deadline_time_utc = convert_to_utc_naive(deadline_time)

        search_domain = [
            ('conf_id','=',configuration_id),
            ('name','=',name),
            ('submission_freq', '=', submission_freq),
            ('doc_type', '=', doc_type),
            ('deadline_time', '=', deadline_time_utc),
            ('deadline_day', '=', deadline_day),
            ('deadline_month', '=', deadline_month)
        ]
        if department_id:
            search_domain.append(('department_id', '=', department_id))

        check_similar_report = self.env['odm.report.submission'].search(search_domain)
        if not check_similar_report:
            vals = {
                'conf_id' : configuration_id,
                'name': name,
                'submission_freq': submission_freq,
                'doc_type': doc_type,
                'deadline_time': deadline_time_utc,
                'deadline_day': deadline_day,  # <-- sebelumnya salah diisi dengan deadline_time
                'deadline_month': deadline_month,
            }
            if department_id:
                vals['department_id'] = department_id
            created = self.create(vals)
            if created:
                return created.id
        return False

    def action_print_ticket(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/print/model_x/%s' % self.id,
            'target': 'new',
        }

    def write(self, vals):
        res = super(ReportSubmission, self).write(vals)
        for record in self:
            # When an attachment is added, the state becomes 'pending'
            if record.state == 'draft' and record.attachment_ids and record.report_description:
                record.state = 'pending'
                self._send_email_to_reviewer()
                # And we clear the activity for the user who submitted it
                activities_for_user = record.activity_ids.filtered(lambda act: act.user_id == self.env.user)
                if activities_for_user:
                    activities_for_user.action_feedback(feedback='Submitted')

            # When a reviewer marks as completed, clear all remaining activities
            if vals.get('state') == 'completed':
                record.activity_ids.action_feedback(feedback='Report Approved')
                
        for rec in self:
            updates = {}
            # ambil value terbaru yang dikirim lewat write()
            state = vals.get('state', rec.state)
            doc_type_id = vals.get('doc_type', rec.doc_type.id)
            report_name = vals.get('name', rec.name)
            report_desc = vals.get('report_description', rec.report_description)
            receipt_code = vals.get('receipt_code', rec.receipt_code)
            # hanya update jika state berubah
            if 'state' in vals:
                updates.update({
                    'state_submission': state,
                    'document_type': doc_type_id,
                    'report_name': report_name,
                    'report_desc': report_desc,
                    'code_receipt':receipt_code
                })

            if updates:
                rec.attachment_ids.write(updates)
        
        return res

    def _cron_create_submission_activities(self):
        _logger.info("Starting cron job: Create Report Submission Activities")
        # Find draft submissions, bypassing custom search logic by adding a context key
        submissions = self.with_context(skip_custom_search=True).search([('state', '=', 'draft')])
        _logger.info(f"Found {len(submissions)} draft submissions to process.")

        activity_type = self.env.ref('odm_report_scheduler.mail_activity_type_report_submission')

        for sub in submissions:
            _logger.info(f"Processing submission: {sub.name} (ID: {sub.id})")
            # Check if an activity already exists for this user and submission
            activity = self.env['mail.activity'].search([
                ('res_id', '=', sub.id),
                ('res_model_id', '=', self.env.ref('odm_report_scheduler.model_odm_report_submission').id),
                ('user_id', '=', sub.report_pic_id.id),
                ('activity_type_id', '=', activity_type.id)
            ])
            if not activity:
                # Create activity if it doesn't exist
                self.env['mail.activity'].create({
                    'res_id': sub.id,
                    'res_model_id': self.env.ref('odm_report_scheduler.model_odm_report_submission').id,
                    'activity_type_id': activity_type.id,
                    'summary': activity_type.summary,
                    'date_deadline': sub.deadline_time.date(),
                    'user_id': sub.report_pic_id.id,
                })

    def _cron_email_reminder(self):
        _logger.info("Starting cron job: Email Reminder")
        today = fields.Date.context_today(self)

        # Find draft submissions that are not daily or weekly
        submissions = self.with_context(skip_custom_search=True).search([
            ('state', '=', 'draft'),
        ])

        submissions_to_remind = []
        for sub in submissions:
            # Check if the submission is linked to a configuration with a reminder set
            if sub.conf_id.reporting_period == 'daily' and sub.deadline_time.date() == today:
                submissions_to_remind.append(sub)
            elif sub.conf_id and sub.conf_id.remaining_time >= 0:
                reminder_date = sub.deadline_time.date() - timedelta(days=sub.conf_id.remaining_time)
                if reminder_date == today:
                    submissions_to_remind.append(sub)
        
        _logger.info(f"Found {len(submissions_to_remind)} submissions to send reminders for.")

        for sub in submissions_to_remind:
            mail_server = sub.conf_id.mail_config_id
            if not mail_server:
                _logger.warning(f"Submission '{sub.name}' (ID: {sub.id}) is missing mail configuration. Skipping email reminder.")
                continue
            
            user = self.env['res.users'].search([
                ('id', '=', sub.report_pic_id.id)
            ])

            recipient_emails = [user.partner_id.email]
            if not recipient_emails:
                _logger.warning(f"User doesn't have email address. Skipping.")
                continue

            # Construct email subject and body
            subject = f"Reminder: Report Submission '{sub.name}'"
            deadline_str = sub.deadline_time.strftime('%A, %d %B %Y')
            body_html = f"""
            <html>
                <body>
                    <p>Dear Bapak/Ibu {user.name},</p>
                    <p>Ini adalah pengingat bahwa report "<strong>{sub.name}</strong>" harus dilengkapi sebelum hari <strong>{deadline_str}</strong>.<br/>
                    Silahkan melengkapi report tersebut dengan <a href="https://gagnikel.id/web/login" target="_blank">login melalui link berikut</a> dan masuk ke menu 'Document Monitoring' di aplikasi Odoo</p>
                                        
                    <p>Terima kasih,<br/><em>Odoo System (Automated Message)</em></p>
                </body>
            </html>
            """

            # Create the email message
            msg = MIMEText(body_html, 'html')
            msg['Subject'] = subject
            msg['From'] = mail_server.smtp_user
            msg['To'] = ", ".join(recipient_emails)

            # Send the email
            try:
                _logger.info(f"Sending email reminder for '{sub.name}' to {recipient_emails}...")
                with SMTP_SSL(mail_server.smtp_host, mail_server.smtp_port, timeout=10) as server:
                    server.login(mail_server.smtp_user, mail_server.smtp_pass)
                    server.sendmail(mail_server.smtp_user, recipient_emails, msg.as_string())

                    self.env['odm.document.mail.log'].create({
                        'configuration_id': sub.conf_id.id,
                        'user_id': user.id,
                        'email': user.partner_id.email,
                        'scheduled_time': sub.deadline_time,
                        'notification_time': fields.Datetime.now(),
                        'status': 'success',
                        'error_message': None,
                        'sent_at': fields.Datetime.now(),
                    });

                    _logger.info(f"Successfully sent email reminder for submission '{sub.name}'.")
            except Exception as e:
                self.env['odm.document.mail.log'].create({
                    'configuration_id': sub.conf_id.id,
                    'user_id': user.id,
                    'email': user.partner_id.email,
                    'scheduled_time': sub.deadline_time,
                    'notification_time': fields.Datetime.now(),
                    'status': 'failed',
                    'error_message': e,
                    'sent_at': fields.Datetime.now(),
                });
                _logger.error(f"Failed to send email for submission '{sub.name}'. Error: {e}", exc_info=True)
    def _send_email_to_reviewer(self):
        conf_id = self.conf_id
        mail_server = conf_id.mail_config_id
        reviewer = conf_id.report_ownership
        subject = f"Report Menunggu Review - {conf_id.name}"

        for user in reviewer:
            receipient = user.partner_id.email
            body = f"""
                <html>
                    <body>
                        <p>Dear Bapak/Ibu {user.name},</p>
                        <p>Report {conf_id.name} baru saja di-submit oleh {self.report_pic_id.name}. Silahkan <a href="https://gagnikel.id/web/login" target="_blank">login melalui link berikut</a> dan masuk ke menu 'Document Monitoring' untuk mereview.</p>
                                            
                        <p>Terima kasih,<br/><em>Odoo System (Automated Message)</em></p>
                    </body>
                </html>
                """
            msg = MIMEText(body, 'html')
            msg['Subject'] = subject
            msg['From'] = mail_server.smtp_user
            msg['To'] = receipient

            with SMTP_SSL(mail_server.smtp_host, mail_server.smtp_port, timeout=10) as server:
                server.login(mail_server.smtp_user, mail_server.smtp_pass)
                server.sendmail(mail_server.smtp_user, receipient, msg.as_string())

class ReportAttachmentList(models.Model):
    _name = 'odm.report.attachments'
    _description = 'Report Attachment List'

    submission_id = fields.Many2one('odm.report.submission', string='Report Name', ondelete='cascade')
    name = fields.Char(string="Description", required=True, tracking=True)
    uploaded_file = fields.Binary(string="Document Attachment", tracking=True)

    file_name = fields.Char(string="File Name", required=True)
    mimetype = fields.Char(string="MIME Type", compute="_compute_mimetype", store=True)
    download_url = fields.Char(string="Download URL", compute="_compute_download_url")
    # Field untuk thumbnail icon
    thumbnail_icon = fields.Char(string="Thumbnail Icon", compute="_compute_thumbnail_icon", store=True)
    # Field baru untuk image viewer
    uploaded_image_base64 = fields.Binary(
        string="Image Preview",
        compute="_compute_image_preview",
        store=False
    )
    # Field baru untuk menampilkan state dari submission
    state_submission  = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ], default="draft", string="Status", tracking=True)
    document_type = fields.Many2one("oa.reporting.type", string="Report Category", required=True, tracking=True)
    report_name = fields.Char(string="Report Name", tracking=True)
    report_desc = fields.Html(string="Report Description", sanitize=False)
    code_receipt = fields.Char(string="Report Code", tracking=True)
    document_sent_count = fields.Integer(
        string="Times Sent",
        compute="_compute_doc_sent_count",
        store=False
    )

    def _compute_doc_sent_count(self):
        Log = self.env["odm.email.log"]
        for rec in self:
            rec.document_sent_count = Log.search_count([
                ("attachment_id", "=", rec.id)
            ])

    @api.depends('file_name','uploaded_file')
    def _compute_mimetype(self):
        for rec in self:
            if rec.file_name:
                mime, _ = mimetypes.guess_type(rec.file_name)
            else:
                mime = None

            # Jika filename gagal deteksi, coba deteksi dari binary
            if not mime and rec.uploaded_file:
                # Guess from header of the file (lebih akurat)
                try:
                    header = base64.b64decode(rec.uploaded_file[:50])
                    if header.startswith(b'%PDF'):
                        mime = 'application/pdf'
                    elif header.startswith(b'\xFF\xD8'):
                        mime = 'image/jpeg'
                    elif header.startswith(b'\x89PNG'):
                        mime = 'image/png'
                except:
                    pass

            rec.mimetype = mime or 'application/octet-stream'

    @api.depends('file_name')
    def _compute_download_url(self):
        for rec in self:
            if rec.id:
                rec.download_url = '/odm/report/download/%s' % rec.id

        # Override create dan write untuk update state_submission
    @api.model
    def create(self, vals):
        if vals.get('submission_id'):
            submission = self.env['odm.report.submission'].browse(vals['submission_id'])
            vals['state_submission'] = submission.state
            vals['report_desc'] = submission.report_description
            vals['report_name'] = submission.name
            vals['document_type'] = submission.doc_type.id
            vals['code_receipt'] = submission.receipt_code
        return super().create(vals)

    def write(self, vals):
        # This logic is mostly for when an attachment line is edited directly
        # and the parent submission_id is changed.
        if vals.get('submission_id'):
            submission = self.env['odm.report.submission'].browse(vals['submission_id'])
            vals['state_submission'] = submission.state
            vals['report_desc'] = submission.report_description
            vals['report_name'] = submission.name
            vals['document_type'] = submission.doc_type.id # Correctly use the ID
            vals['code_receipt'] = submission.receipt_code
        
        # The logic below was faulty and redundant. The parent write method
        # already pushes the correct values to the attachments.
        # This block was incorrectly overwriting the correct doc_type ID with an object.
        #
        # elif 'submission_id' not in vals:
        #    for rec in self:
        #         vals['state_submission'] = rec.submission_id.state
        #         vals['report_desc'] = rec.submission_id.report_description
        #         vals['report_name'] = rec.submission_id.name
        #         vals['document_type'] = rec.submission_id.doc_type
        return super().write(vals)

    @api.depends('mimetype')
    def _compute_thumbnail_icon(self):
        for rec in self:
            mt = rec.mimetype or ''
            if mt.startswith('image/'):
                rec.thumbnail_icon = 'image'
            elif 'pdf' in mt:
                rec.thumbnail_icon = '/odm_report_scheduler/static/src/img/file_icons/pdf.png'
            elif 'word' in mt or 'msword' in mt:
                rec.thumbnail_icon = '/odm_report_scheduler/static/src/img/file_icons/word.png'
            elif 'excel' in mt or 'spreadsheet' in mt:
                rec.thumbnail_icon = '/odm_report_scheduler/static/src/img/file_icons/excel.png'
            else:
                rec.thumbnail_icon = '/odm_report_scheduler/static/src/img/file_icons/file.png'

    def action_open_pdf_viewer (self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'File Preview',
            'res_model': 'odm.report.attachments',
            'res_id': self.id,
            'view_mode': 'form',
            # Kita akan buat view khusus ID ini di XML nanti
            'view_id': self.env.ref('odm_report_scheduler.view_custom_document_preview_form').id,
            'target': 'new',  # Ini kuncinya: membuka sebagai POPUP / Modal
            'flags': {'mode': 'readonly'},  # Opsional: agar mode baca saja
        }

    @api.depends('uploaded_file', 'file_name')
    def _compute_image_preview(self):
        for rec in self:
            rec.uploaded_image_base64 = False
            if rec.thumbnail_icon == 'image' and rec.uploaded_file:
                rec.uploaded_image_base64 = rec.uploaded_file

    def _auto_sync_recipients(self):
        """Sinkronisasi email dari res.users.login ke docmon.mail.recipient.
           Abaikan login yang bukan format email."""

        Recipient = self.env["docmon.mail.recipient"]
        Users = self.env["res.users"].search([("login", "!=", False)])

        # regex format email
        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        for user in Users:
            email = (user.login or "").strip().lower()

            # skip jika bukan format email valid
            if not re.match(email_pattern, email):
                continue

            # cek apakah sudah ada
            exists = Recipient.search([("name", "=ilike", email)], limit=1)
            if not exists:
                Recipient.create({"name": email})

    def action_open_send_email_form(self):
        self.ensure_one()
        self._auto_sync_recipients()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Share Document By Email',
            'res_model': 'odm.send.mail.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_attachment_id': self.id,
                'default_file_name': self.file_name,
                'default_file_data' : self.uploaded_file,
                'default_subject': 'File: %s' % self.name,
                'default_body' : f"""
                                  <p>Kepada Yth. Bapak / Ibu,</p>
                                  <p>Terlampir file {self.name}. yang kami kirimkan bersamaan dengan email ini</p>
                                  
                                  
                                  
                                    <br/>
                                    Salam Hormat,<br/>
                                    <strong>{self.env.user.name}</strong>
                                 """
            }
        }

    def action_view_email_log(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Document External Sending Logs',
            'res_model': 'odm.email.log',
            'view_mode': 'tree',
            'target': 'current',
            'domain': [('attachment_id', '=', self.id)],
            'context': {'default_attachment_id': self.id},
        }

