from odoo import http
from odoo.http import request, content_disposition
import base64

class AttachmentController(http.Controller):

    @http.route('/odm/report/download/<int:attachment_id>', type='http', auth='user')
    def download_attachment(self, attachment_id):
        attachment = request.env['odm.report.attachments'].sudo().browse(attachment_id)
        if not attachment or not attachment.uploaded_file:
            return request.not_found()

        filecontent = base64.b64decode(attachment.uploaded_file)
        filename = attachment.file_name or 'attachment.bin'
        mimetype = attachment.mimetype or 'application/octet-stream'

        return request.make_response(
            filecontent,
            headers=[
                ('Content-Type', mimetype),
                ('Content-Disposition', content_disposition(filename))
            ]
        )