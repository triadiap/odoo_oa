# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class SCMNomorSurat(models.Model):
    _name = 'gag.oa.scm.document.number'
    _description = 'Office Automation Nomor Surat'

    no_surat = fields.Char(string="Nomor Surat", required=True)
    keterangan = fields.Char(string="Keterangan", required=True)
    tanggal  = fields.Date(string="Tanggal Surat", required=True)