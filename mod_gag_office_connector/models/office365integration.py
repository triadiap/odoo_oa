import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class Office365Integration(models.Model):
    _name = 'office365.integration'
    _description = 'Office 365 Integration'

    client_id = fields.Char(string='Client ID', required=True)
    client_secret = fields.Char(string='Client Secret', required=True)
    tenant_id = fields.Char(string='Tenant ID', required=True)

    def get_access_token_raw(self):
        """
        Fetches a new access token from Office 365 without saving it to avoid recursion.
        """
        token_url = f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': self.client_id,
            'scope': 'https://graph.microsoft.com/.default',
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
        }

        response = requests.post(token_url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            if access_token:
                _logger.info("Access token fetched successfully.")
                return access_token
            else:
                raise UserError(_('No access token in response'))
        else:
            error_message = response.json().get('error_description', 'No details available')
            raise UserError(_('Failed to fetch access token: %s') % error_message)

    def send_simple_email(self, to_email, subject, content):
        """
        Send a simple email using the Microsoft Graph API without relying on the access_token field.
        """
        # Retrieve access token without storing in self
        token = self.get_access_token_raw()
        if not token:
            raise UserError(_('Access token missing. Please try again.'))

        send_url = 'https://graph.microsoft.com/v1.0/me/sendMail'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        email_payload = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": content
                },
                "toRecipients": [
                    {"emailAddress": {"address": to_email}}
                ]
            }
        }

        response = requests.post(send_url, headers=headers, json=email_payload)
        if response.status_code == 202:
            _logger.info("Email sent successfully to %s", to_email)
            return True
        else:
            error_msg = response.json().get('error', {}).get('message', response.text)
            raise UserError(_('Failed to send email: %s') % error_msg)

    def action_send_test_email(self):
        """
        Test method to send an email when the button is clicked.
        """
        test_email = 'bayu.sulistiawan@gmail.com'  # Replace with the recipient's email for testing
        subject = 'Test Email from Odoo Office 365 Integration'
        content = 'This is a test email sent using the Office 365 Integration.'

        try:
            self.send_simple_email(test_email, subject, content)
        except UserError as e:
            # Log or handle specific errors if needed
            raise UserError(_('Failed to send test email: %s') % e.name)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Email Sent'),
                'message': _('Test email sent successfully to %s' % test_email),
                'type': 'success',
                'sticky': False,
            }
        }