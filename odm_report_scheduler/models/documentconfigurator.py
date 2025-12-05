# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from calendar import monthrange
from pytz import timezone
from datetime import date, datetime, timedelta

import json
import logging
_logger = logging.getLogger(__name__)

WEEKDAY_MAPPING = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}

class DocumentConfiguration(models.Model):
    _name = 'odm.document.configuration'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Document expiry and timeline configuration setup feature'

    name = fields.Char(string="Report Name", required=True, tracking=True)
    config_description = fields.Text(string="Description",tracking=True)
    reporting_period = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly','Quarterly'),
        ('semester','Semester'),
        ('yearly','Yearly')
    ],string="Period",required=True,tracking=True)
    document_type = fields.Many2one("oa.reporting.type",string="Report Type",required=True,tracking=True)
    remaining_time = fields.Integer(string="Remaining Time", required=True, tracking=True)
    report_activation = fields.Boolean(string="Activation Status",required=True,default=True,tracking=True)
    report_ownership = fields.Many2many("res.users",required=True,string="Ownership",tracking=True)
    department_ids = fields.Many2many("hr.department", string="Departments", tracking=True)
    mail_config_id = fields.Many2one("docmon.mail.server", string="Mail Configuration", default=lambda self: self._default_mail_config(), tracking=True)

    @api.model
    def _default_mail_config(self):
        return self.env['docmon.mail.server'].search([], order='sequence asc', limit=1)
    count_success = fields.Integer(compute='_compute_status_counts', string="Success Status Count")
    count_failed = fields.Integer(compute='_compute_status_counts', string="Failed Status Count")
    report_hour = fields.Selection(
        [(str(h), f"{h:02d}:00") for h in range(0, 24)],
        string="Deadline Time",tracking=True)
    mail_log_ids = fields.One2many(
        'odm.document.mail.log',
        'configuration_id',
        string='Log Pengiriman Email'
    )
    report_day = fields.Selection(
        [('monday', 'Senin'),
         ('tuesday', 'Selasa'),
         ('wednesday', 'Rabu'),
         ('thursday', 'Kamis'),
         ('friday', 'Jumat'),
         ('saturday', 'Sabtu'),
         ('sunday', 'Minggu')],
        string="Deadline Day",tracking=True)

    report_month = fields.Selection(
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
        string="Deadline Month",tracking=True)

    report_date = fields.Integer(string="Deadline Date",tracking=True)

    @api.depends('mail_log_ids.status')
    def _compute_status_counts(self):
        for record in self:
            logs = record.mail_log_ids
            record.count_success = logs.filtered(lambda l: l.status == 'success').mapped('id').__len__()
            record.count_failed = logs.filtered(lambda l: l.status == 'failed').mapped('id').__len__()

    def method_testing(self):
       for record in self:
           if record.report_activation:
               listuser = record.report_ownership
               for userlist in  listuser:
                   print("ID User",userlist.id)
                   print("Name", userlist.name)
                   print("Login", userlist.login)
           else:
               print("Status is inactive")

    def send_email_notification(self,emailto,mail_subject,mail_body,log_data=None):
        # Get the mail server
        mail_server = self.mail_config_id

        if not mail_server:
            raise ValidationError("No outgoing mail server configured for this document configuration!")

        # cara direct
        smtp_server = mail_server.smtp_host
        smtp_port = mail_server.smtp_port
        smtp_user = mail_server.smtp_user
        smtp_password = mail_server.smtp_pass

        email_from = smtp_user
        email_to = emailto
        subject = mail_subject
        body = mail_body

        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = email_to
        status = 'failed'
        error_message = None

        try:
            # Use SMTP_SSL for a secure and direct connection
            with SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_user, smtp_password)
                server.sendmail(email_from, [email_to], msg.as_string())
            status = 'success'
            print("Email sent successfully")
        except Exception as e:
            error_message = str(e)
            print(f"Failed to send email: {error_message}")
            # Buat log email
        if log_data:
            self.env['odm.document.mail.log'].create({
                    'configuration_id': log_data.get('configuration_id'),
                    'user_id': log_data.get('user_id'),
                    'email': emailto,
                    'scheduled_time': log_data.get('scheduled_time'),
                    'notification_time': log_data.get('notification_time'),
                    'status': status,
                    'error_message': error_message,
            })

    @api.onchange('reporting_period')
    def _onchange_reporting_period(self):
        """Clear irrelevant fields based on selected reporting period"""
        if self.reporting_period != 'daily':
            self.report_hour = False
        if self.reporting_period != 'weekly':
            self.report_day = False
        if self.reporting_period not in ['monthly','yearly','tree_month','semester','quarterly']:
            self.report_date = False
        if self.reporting_period not in ['yearly']:
            self.report_month = False

    @api.onchange('report_month')
    def _onchange_report_month(self):
        """Update max day limit for report_date based on report_month"""
        if self.report_month:
            try:
                month = int(self.report_month)
                year = fields.Date.today().year  # default ke tahun sekarang
                last_day = monthrange(year, month)[1]  # ambil jumlah hari di bulan tsb
                # Optional: reset nilai jika lebih dari batas hari
                if self.report_date and self.report_date > last_day:
                    self.report_date = False
                self._context = dict(self._context or {}, max_report_date=last_day)
            except Exception:
                self.report_date = False

    @api.constrains('report_month', 'report_date')
    def _check_valid_report_date(self):
        for rec in self:
            if rec.reporting_period in ['monthly', 'yearly', 'tree_month', 'semester', 'quarterly'] and rec.report_month and rec.report_date:
                month = int(rec.report_month)
                year = date.today().year
                max_day = monthrange(year, month)[1]
                if rec.report_date < 1 or rec.report_date > max_day:
                    raise ValidationError(f"Tanggal {rec.report_date} tidak valid untuk bulan tersebut.")

    def manual_notification_process(self):
        configuration_list = self.env['odm.document.configuration'].search([('report_activation','=','true')])
        for listconf in configuration_list:
            departments = listconf.department_ids or self.env['hr.department'].search([]) # Get departments for this config

            for dept in departments: # Iterate through departments
                generatetasklist = False
                scheduled_time, notification_time = False, False

                if listconf.reporting_period =='daily':
                    scheduled_time, notification_time = self.get_next_notification_time(reporting_period=listconf.reporting_period,report_hour=listconf.report_hour,remaining_time=listconf.remaining_time)
                if listconf.reporting_period == 'weekly':
                    scheduled_time, notification_time = self.get_next_notification_time(reporting_period=listconf.reporting_period,report_day=listconf.report_day,remaining_time=listconf.remaining_time)
                if listconf.reporting_period == 'monthly':
                    scheduled_time, notification_time = self.get_next_notification_time(reporting_period=listconf.reporting_period,report_date=listconf.report_date,remaining_time=listconf.remaining_time)
                if listconf.reporting_period == 'tree_month':
                    scheduled_time, notification_time = self.get_next_notification_time(reporting_period=listconf.reporting_period,report_date=listconf.report_date,remaining_time=listconf.remaining_time)
                if listconf.reporting_period == 'quarterly':
                    scheduled_time, notification_time = self.get_next_notification_time(reporting_period=listconf.reporting_period,report_date=listconf.report_date,remaining_time=listconf.remaining_time)
                if listconf.reporting_period == 'semester':
                    scheduled_time, notification_time = self.get_next_notification_time(reporting_period=listconf.reporting_period,report_date=listconf.report_date,remaining_time=listconf.remaining_time)
                if listconf.reporting_period == 'yearly':
                    scheduled_time, notification_time = self.get_next_notification_time(reporting_period=listconf.reporting_period,report_date=listconf.report_date,remaining_time=listconf.remaining_time,report_month=listconf.report_month)

                if notification_time and notification_time.date() == fields.Date.today():
                    generatetasklist = self.env['odm.report.submission'].generate_report(
                        listconf.id,
                        listconf.name,
                        listconf.reporting_period,
                        listconf.document_type.id,
                        scheduled_time.strftime('%Y-%m-%d %H:%M:%S'),
                        listconf.report_day,
                        listconf.report_month,
                        dept.id # Pass department_id here
                    )
                if generatetasklist:
                    for listofrespondent in listconf.report_ownership:
                        if listofrespondent.email:
                                subject = f"Reminder: {listconf.name} - {listconf.reporting_period.title()} Report - Deadline {scheduled_time.strftime('%d %B %Y %H:%M')}"
                                body = f"""
                                            <p>Halo Bapak / Ibu {listofrespondent.name},</p>
                                            <p>Ini adalah pesan otomatis untuk mengingatkan Bapak / Ibu {listofrespondent.name} dari departemen <strong>{dept.name}</strong> bahwa laporan <strong>{listconf.name}</strong> harus segera disiapkan.</p>
                                            <li><p><strong>Kategori Dokumen:</strong> {listconf.document_type.name or 'Tidak ada kategori'}</p></li>
                                <li><p><strong>Deskripsi:</strong> {listconf.config_description or 'Tidak ada deskripsi'}</p></li>
                                <li><p><strong>Periode:</strong> {listconf.reporting_period}</p></li>
                                <li><p><strong>Deadline:</strong> {scheduled_time.strftime('%d %B %Y %H:%M')} WIB</p></li>
                                <p>Selanjutnya Bapak / Ibu bisa melakukan pengisian laporan melalui menu Document Monitoring yang ada di halaman ERP PT.GAG Nikel yang bisa diakses dengan menekan tautan <a href="https://gagnikel.id/web/login" target="_blank">ini</a>.Dan abaikan pesan ini jika pengisian laporan sudah dilakukan</p>
                                <br/>
                                <p>Terima kasih,</p>
                                <p><em>Document Monitoring Scheduler Bot</em></p>
                                """
                        self.env['odm.report.submission'].browse(generatetasklist).message_post(
                            body=f"""
                                 <p>Halo Bapak / Ibu {listofrespondent.name},</p>
                                 <p>Ini adalah pesan otomatis untuk mengingatkan Bapak / Ibu {listofrespondent.name} dari departemen <strong>{dept.name}</strong> bahwa laporan <strong>{listconf.name}</strong> harus segera disiapkan.</p>
                            """,
                            subject=subject,
                            message_type="notification",  # agar muncul di Discuss Inbox
                            partner_ids=[listofrespondent.partner_id.id],  # ← ini harus list of integers
                        )

                        self.send_email_notification(listofrespondent.email,
                                        subject,
                                        body,
                                        log_data = {
                                                'configuration_id': listconf.id,
                                                'user_id': listofrespondent.id,
                                                'scheduled_time': scheduled_time.replace(tzinfo=None) if scheduled_time else None,
                                                'notification_time': notification_time.replace(tzinfo=None) if notification_time else None,
                                                    }
                                            )

    def get_next_notification_time(self, reporting_period=None, report_hour=None, report_day=None,
                                   report_date=None, report_month=None, remaining_time=0):
        """
        Hitung waktu notifikasi berikutnya berdasarkan parameter dan waktu lokal user (WIB).
        """
        user_tz = self.env.user.tz or 'Asia/Jakarta'
        now_utc = datetime.utcnow()
        now = fields.Datetime.context_timestamp(self, now_utc)

        scheduled_time = None
        hour = int(report_hour or 0)

        # --- DAILY ---
        if reporting_period == 'daily':
            # Target selalu hari esok
            next_day = now + timedelta(days=1)
            candidate = next_day.replace(hour=hour, minute=0, second=0, microsecond=0)

            # Lewati Sabtu dan Minggu
            while candidate.weekday() >= 5:  # 5 = Sabtu, 6 = Minggu
                candidate += timedelta(days=1)

            scheduled_time = candidate

        # --- WEEKLY ---
        elif reporting_period == 'weekly':
            if not report_day:
                return False
            weekday_target = WEEKDAY_MAPPING.get(str(report_day).lower())
            if weekday_target is None:
                return False
            days_ahead = (weekday_target - now.weekday() + 7) % 7
            if days_ahead == 0 and now.hour >= hour:
                days_ahead = 7
            next_date = now + timedelta(days=days_ahead)
            scheduled_time = next_date.replace(hour=hour, minute=0, second=0, microsecond=0)

        # --- MONTHLY ---
        elif reporting_period == 'monthly':
            if not report_date:
                return False
            for i in range(2):
                year = now.year + (now.month + i > 12)
                month = (now.month + i - 1) % 12 + 1
                max_day = monthrange(year, month)[1]
                day = min(report_date, max_day)
                candidate = datetime(year, month, day, hour)
                candidate = timezone(user_tz).localize(candidate)
                if candidate > now:
                    scheduled_time = candidate
                    break

        # --- YEARLY ---
        elif reporting_period == 'yearly':
            if not report_month or not report_date:
                return False
            for i in range(2):
                year = now.year + i
                month = int(report_month)
                max_day = monthrange(year, month)[1]
                day = min(report_date, max_day)
                candidate = datetime(year, month, day, hour)
                candidate = timezone(user_tz).localize(candidate)
                if candidate > now:
                    scheduled_time = candidate
                    break

        # --- 3 MONTHS ---
        elif reporting_period == 'tree_month':
            months = [3, 6, 9, 12]
            scheduled_time = self._get_next_periodic_date(now, months, report_date, hour, user_tz)

        # --- SEMESTER ---
        elif reporting_period == 'semester':
            months = [6, 12]
            scheduled_time = self._get_next_periodic_date(now, months, report_date, hour, user_tz)

        # --- QUARTERLY ---
        elif reporting_period == 'quarterly':
            months = [4, 8, 12]
            scheduled_time = self._get_next_periodic_date(now, months, report_date, hour, user_tz)

        # --- OUTPUT FINAL ---
        if scheduled_time:
            notification_time = scheduled_time - timedelta(days=remaining_time)
            return scheduled_time, notification_time
        return False

    def _get_next_periodic_date(self, now, month_list, day, hour, user_tz):
        """
        Ambil tanggal terdekat dari bulan tertentu (3 bulanan, semester, quarterly) dalam zona waktu user.
        """
        day = day or 1
        for i in range(2):  # Coba tahun ini dan tahun depan
            year = now.year + i
            for month in sorted(month_list):
                if year == now.year and month < now.month:
                    continue
                max_day = monthrange(year, month)[1]
                target_day = min(day, max_day)
                try:
                    candidate = datetime(year, month, target_day, hour)
                    candidate = timezone(user_tz).localize(candidate)
                    if candidate > now:
                        return candidate
                except Exception:
                    continue
        return None

    def _generate_future_submissions(self):
        _logger.info("Starting future submission generation for %s configs.", len(self))
        for config in self:
            _logger.info("Processing config: %s (ID: %s)", config.name, config.id)
            # Hapus schedule yang belum submitted
            future_submissions = self.env['odm.report.submission'].search([
                ('conf_id', '=', config.id),
                ('deadline_time', '>', fields.Datetime.now()),
                ('state', '!=', 'completed')
            ])
            if future_submissions:
                _logger.info("Deleting %s outdated future submissions for config %s.", len(future_submissions), config.name)
                future_submissions.unlink()

            # Tentukan departemen
            departments = config.department_ids or self.env['hr.department'].search([])
            _logger.info("Generating submissions for %s department(s).", len(departments))

            # Buat jadwal baru
            for dept in departments:
                # Define the end of the current year for the generation limit
                current_year_end = datetime(fields.Datetime.now().year, 12, 31, 23, 59, 59) # End of current year

                # Use a "cursor" to keep track of where we are in time for generation
                last_deadline = fields.Datetime.now()

                # Define how many submissions to generate to cover roughly 1 year
                num_submissions_to_generate = {
                    'daily': 365,
                    'weekly': 52,
                    'monthly': 12,
                    'quarterly': 4,
                    'semester': 2,
                    'yearly': 1,
                }.get(config.reporting_period, 0)

                if num_submissions_to_generate == 0:
                    _logger.warning("Unsupported reporting period '%s' for config '%s'. Skipping generation.", config.reporting_period, config.name)
                    continue

                for _ in range(num_submissions_to_generate):
                    next_deadline = None
                    year, month = last_deadline.year, last_deadline.month

                    if config.reporting_period == 'daily':
                        hour = int(config.report_hour or 0) # Moved here
                        current_date = last_deadline.date()
                        while True:
                            current_date += timedelta(days=1)
                            if current_date.weekday() < 5: # Monday to Friday
                                next_deadline = datetime.combine(current_date, datetime.min.time()).replace(hour=hour)
                                break
                    
                    elif config.reporting_period == 'weekly':
                        if not config.report_day:
                            _logger.warning("Weekly report '%s' is missing a 'report_day', cannot generate schedule.", config.name)
                            break
                        target_weekday = WEEKDAY_MAPPING.get(config.report_day)
                        days_ahead = (target_weekday - last_deadline.weekday() + 7) % 7
                        if days_ahead == 0:
                            days_ahead = 7
                        next_date = last_deadline.date() + timedelta(days=days_ahead)
                        next_deadline = datetime.combine(next_date, datetime.min.time()) # Defaults to midnight

                    elif config.reporting_period == 'monthly':
                        # Check current month first
                        candidate_year, candidate_month = last_deadline.year, last_deadline.month
                        day = min(config.report_date or 1, monthrange(candidate_year, candidate_month)[1])
                        candidate_deadline = datetime(candidate_year, candidate_month, day)
                        
                        if candidate_deadline > last_deadline:
                            next_deadline = candidate_deadline
                        else:
                            # If deadline for current month has passed, move to the next month
                            month = last_deadline.month + 1
                            year = last_deadline.year
                            if month > 12:
                                month = 1
                                year += 1
                            day = min(config.report_date or 1, monthrange(year, month)[1])
                            next_deadline = datetime(year, month, day)

                    elif config.reporting_period in ['quarterly', 'semester', 'tree_month']:
                        months_map = {
                            'quarterly': [3, 6, 9, 12], 
                            'semester': [6, 12],
                            'tree_month': [4, 8, 12]
                        }
                        possible_months = months_map[config.reporting_period]
                        
                        found_next = False
                        # Check for a valid month in the current year
                        for m in possible_months:
                            if m >= last_deadline.month:
                                day = min(config.report_date or 1, monthrange(last_deadline.year, m)[1])
                                candidate_deadline = datetime(last_deadline.year, m, day)
                                if candidate_deadline > last_deadline:
                                    next_deadline = candidate_deadline
                                    found_next = True
                                    break
                        
                        if not found_next: 
                            # If no valid month in the current year, find the first valid month in the next year
                            year = last_deadline.year + 1
                            m = possible_months[0]
                            day = min(config.report_date or 1, monthrange(year, m)[1])
                            next_deadline = datetime(year, m, day)
                    
                    elif config.reporting_period == 'yearly':
                        year = last_deadline.year if last_deadline.month < (int(config.report_month) if config.report_month else 1) else last_deadline.year + 1
                        try:
                            month = int(config.report_month) if config.report_month else 1
                            day = min(config.report_date or 1, monthrange(year, month)[1])
                            next_deadline = datetime(year, month, day)
                        except (ValueError, TypeError):
                            _logger.error("Invalid date/month configuration for yearly report %s", config.name)
                            break

                    if next_deadline:
                        # Stop if the next deadline is beyond the current year
                        if next_deadline > current_year_end:
                            break

                        if next_deadline > fields.Datetime.now():
                            self.env['odm.report.submission'].create({
                                'conf_id': config.id,
                                'name': config.name,
                                'submission_freq': config.reporting_period,
                                'doc_type': config.document_type.id,
                                'deadline_time': next_deadline,
                                'department_id': dept.id,
                                # 'realization_date': next_deadline.date() #Removed
                            })
                        last_deadline = next_deadline
                    else:
                        break # Stop if no more deadlines can be generated
        _logger.info("Finished future submission generation.")

    @api.model
    def _cron_generate_all_future_submissions(self):
        _logger.info("Starting cron job: Generate All Future Submissions")
        active_configs = self.env['odm.document.configuration'].search([('report_activation', '=', True)])
        _logger.info("Found %s active configurations to process.", len(active_configs))
        active_configs._generate_future_submissions()
        _logger.info("Cron job: Generate All Future Submissions finished.")

    @api.model
    def create(self, vals):
        res = super(DocumentConfiguration, self).create(vals)
        res._generate_future_submissions()
        return res

    def write(self, vals):
        res = super(DocumentConfiguration, self).write(vals)
        if any(field in vals for field in ['reporting_period', 'report_date', 'department_ids']):
            self._generate_future_submissions()
        return res

class DocumentMailLog(models.Model):
    _name = 'odm.document.mail.log'
    _description = 'Log Pengiriman Email Dokumentasi'

    configuration_id = fields.Many2one('odm.document.configuration', string='Configuration', ondelete='cascade')
    user_id = fields.Many2one('res.users', string='User')
    email = fields.Char(string='Email Tujuan')
    scheduled_time = fields.Datetime(string='Scheduled Time')
    notification_time = fields.Datetime(string='Notification Time')
    status = fields.Selection([
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string='Status Pengiriman')
    error_message = fields.Text(string='Pesan Kesalahan (Jika Ada)')
    sent_at = fields.Datetime(string='Tanggal Pengiriman', default=fields.Datetime.now)
