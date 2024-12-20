# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import os


class ApiDocumentation(models.Model):
    _name = 'oa.api.documentation'
    _description = 'Office Controller API Documentation'

    name = fields.Char(string='Name', required=True)
    description = fields.Html(string='Description', help="Write the API documentation here in HTML format.")
    example_code = fields.Text(string='Code Example', help="Provide sample request/response code.")
    image = fields.Binary(string='Image', attachment=True)
    image_path = fields.Char(string='Image Path')

    @api.model
    def _save_image_to_folder(self, image_data, record_id):
        """ Saves the uploaded image to a folder inside the module """
        # Define the module's static folder path to save the image
        module_path = os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(module_path, '../static/src/img/')
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        # File name based on record ID and extension (you can customize the naming convention)
        file_name = f'documentation_image_{record_id}.png'
        file_path = os.path.join(image_folder, file_name)

        # Write the binary data to the file system
        with open(file_path, 'wb') as file:
            file.write(base64.b64decode(image_data))

        # Return the relative path (so you can store it in the database)
        return f'/static/src/img/{file_name}'

    @api.model
    def create(self, vals):
        # Handle image saving on creation
        image_data = vals.get('image')
        new_record = super(ApiDocumentation, self).create(vals)

        if image_data:
            # Save the image to the file system and update the image path
            image_path = self._save_image_to_folder(image_data, new_record.id)
            new_record.image_path = image_path

        return new_record

    def write(self, vals):
        # Handle image saving on update
        res = super(ApiDocumentation, self).write(vals)
        image_data = vals.get('image')

        if image_data:
            # Save the new image to the file system and update the image path
            image_path = self._save_image_to_folder(image_data, self.id)
            self.image_path = image_path

        return res