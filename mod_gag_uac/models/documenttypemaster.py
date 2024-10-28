# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class MasterDataDocumentType(models.Model):
    _name = 'oa.document.type'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Document Type Master Data'

    name = fields.Char('Form Name', required=True, tracking=True)
    iso_code = fields.Char('ISO Code', required=True, tracking=True)
    document_desc = fields.Text('Description',tracking=True)


