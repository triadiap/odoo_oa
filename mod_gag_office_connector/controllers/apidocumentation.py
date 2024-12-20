from odoo import http
from odoo.http import request
import os

class APIDocumentationController(http.Controller):

    @http.route('/path/to/serve/<string:image_filename>', type='http', auth="public")
    def serve_image(self, image_filename, **kwargs):
        image_path = f'/mod_gag_office_connector/static/src/img/{image_filename}'

        if os.path.exists(image_path):
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            return request.make_response(image_data, [('Content-Type', 'image/png')])  # Adjust content type based on image
        else:
            return request.not_found()
