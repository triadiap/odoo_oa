# `-*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


class DocmonMailRecipient(models.Model):
    _name = 'docmon.mail.recipient'
    _description = 'Email Recipient List'

    name = fields.Char("Name", required=True)

    # ---------------------------------------------------------
    # Clean value
    # ---------------------------------------------------------
    @api.model
    def _clean_values(self, vals):
        """Membersihkan input dan normalisasi."""
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].strip().lower()
        return vals

    # ---------------------------------------------------------
    # Validasi format email (name = email)
    # ---------------------------------------------------------
    def _validate_email_format(self, email):
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, email):
            raise ValidationError(_("Format email '%s' tidak valid!") % email)

    # ---------------------------------------------------------
    # Validasi duplikasi email
    # ---------------------------------------------------------
    def _validate_email_duplicate(self, vals):
        email = vals.get('name')
        if email:
            exist = self.search([
                ('name', '=ilike', email),
                ('id', '!=', self.id or 0)
            ], limit=1)

            if exist:
                raise ValidationError(_("Email '%s' sudah terdaftar!") % email)

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    @api.model
    def create(self, vals):
        vals = self._clean_values(vals)

        if 'name' in vals:
            self._validate_email_format(vals['name'])

        self._validate_email_duplicate(vals)

        return super(DocmonMailRecipient, self).create(vals)

    # ---------------------------------------------------------
    # WRITE
    # ---------------------------------------------------------
    def write(self, vals):
        vals = self._clean_values(vals)

        if 'name' in vals:
            self._validate_email_format(vals['name'])

        merged_vals = dict(self.read()[0], **vals)
        self._validate_email_duplicate(merged_vals)

        return super(DocmonMailRecipient, self).write(vals)