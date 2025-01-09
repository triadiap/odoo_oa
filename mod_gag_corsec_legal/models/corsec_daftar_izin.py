from odoo import api, models, fields, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
class CorsecDaftarIzin(models.Model):
    _name = "corsec.daftar.izin"
    _description = "CORSEC Daftar Izin"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    name = fields.Char(string="Nama Dokumen", required=True)
    nama_izin = fields.Char(string="Nama Izin", required=True)
    penerbit = fields.Char(string="Instansi Penerbit", required=True)
    tanggal = fields.Date(string="Tanggal Izin", required=True)
    no_izin = fields.Char(string="Nomor Izin", required=True)
    keterangan = fields.Text(string="Keterangan")
    jangka_waktu = fields.Char(string="Jangka Waktu")
    berakhir_pada = fields.Date(string="Berakhir Pada")
    status = fields.Selection([
        ("status_1", "Pembuatan SK Tim"),
        ("status_2", "Pemenuhan Data Administrasi"),
        ("status_3", "Persetujuan Manager"),
        ("status_4", "Persetujuan GM"),
        ("status_5", "Persetujuan Direksi"),
        ("status_6", "Proses Corsec & Legal"),
        ("status_7", "Pengiriman Kementrian Terkait"),
        ("status_8", "Revisi Kementrian"),
        ("status_9", "Pengajuan Ulang"),
        ("status_10", "Done"),
    ])
    lampiran = fields.Binary(string="Lampiran Soft Copy")

    list_syarat = fields.One2many("corsec.dokumen.persyaratan", "id_izin", string="Dokumen Persyaratan")

    def _get_notification_periods(self):
        """Returns a list of tuples containing (months/weeks ahead, description)"""
        return [
            (6, 'months', '6 months'),
            (3, 'months', '3 months'),
            (1, 'months', '1 month'),
            (1, 'weeks', '1 week')
        ]

    def send_expiry_notification(self, time_amount, time_unit, description):
        """
        Send notification to users about document expiration
        """
        # Get the date to check against
        today = fields.Date.today()
        if time_unit == 'months':
            target_date = today + relativedelta(months=time_amount)
        else:  # weeks
            target_date = today + relativedelta(weeks=time_amount)

        # Find documents expiring on the target date
        documents = self.search([
            ('berakhir_pada', '=', target_date)
        ])

        # Get users who should receive the notification (you can modify this as needed)
        user_ids = self.env['res.groups'].search([
                    ('name', '=', 'OA Jakarta')
                ]).users


        # Create notifications for each document
        for document in documents:
            message = f"⚠️ REMINDER: Document '{document.name}' will expire in {description} (on {document.berakhir_pada})"

            # Post the message in the chatter
            document.message_post(
                body=message,
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
                partner_ids=user_ids.mapped('partner_id').ids,
            )

            # Create an activity for better visibility
            self.env['mail.activity'].create({
                'activity_type_id': 4,
                'note': message,
                'user_id': user_ids[0].id,  # Assign to the first user in the group
                'res_id': document.id,
                'res_model_id': self.env['ir.model'].search([('model', '=', self._name)]).id,
            })

    @api.model
    def _cron_check_document_expiry(self):
        """
        Cron job method to check for expiring documents and send notifications
        """
        for time_amount, time_unit, description in self._get_notification_periods():
            self.send_expiry_notification(time_amount, time_unit, description)

class PersyaratanDokumenIzin(models.Model):
    _name = "corsec.dokumen.persyaratan"
    _description = "Model for Daftar Dokumen Persyaratan Pengajuan Izin"

    name = fields.Char(string="Nama Dokumen", required=True)
    file = fields.Binary(string="Lampiran Dokumen", required=True)

    id_izin = fields.Many2one("corsec.daftar.izin", string="ID Izin")