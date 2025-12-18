from odoo import models, fields, _

class OdmEmailLog(models.Model):
    _name = "odm.email.log"
    _description = "Email Sending Log"
    _order = "send_date desc"

    # Relasi ke dokumen asal
    attachment_id = fields.Many2one(
        "odm.report.attachments",
        string="Document",
        ondelete="cascade",
    )

    # Informasi email
    email_to = fields.Text("Send To")
    email_cc = fields.Text("CC")
    subject = fields.Char("Subject")
    body = fields.Html("Body Message")

    # Informasi file
    file_name = fields.Char("File Name")
    file_data = fields.Binary("File Data")
    namareport = fields.Char(related="attachment_id.submission_id.name",store="True")
    documenttype = fields.Char(related="attachment_id.submission_id.doc_type.name",store="True")

    # Tanggal kirim
    send_date = fields.Datetime(
        "Send Date",
        default=lambda self: fields.Datetime.now()
    )

    # User yang mengirim
    user_id = fields.Many2one(
        "res.users",
        string="Sent By",
        default=lambda self: self.env.user,
        readonly=True
    )

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.documenttype} - {record.namareport} - {record.file_name}"
            result.append((record.id, name))  # or any other meaningful field
        return result

    def action_print_receipt(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/print/external_receipt/%s' % self.id,
            'target': 'new',
        }