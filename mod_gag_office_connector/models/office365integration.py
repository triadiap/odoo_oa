import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import requests

_logger = logging.getLogger(__name__)


class Office365Integration(models.Model):
    _name = 'office365.integration'
    _description = 'Office 365 Integration'

    client_id = fields.Char(string='Client ID', required=True)
    client_secret = fields.Char(string='Client Secret', required=True)
    tenant_id = fields.Char(string='Tenant ID', required=True)
    access_token = fields.Text(string='Access Token', readonly=True)
    refresh_token = fields.Text(string='Refresh Token', readonly=True)

    # Fields for sending test email
    test_email_to = fields.Char(string='Test Email Recipient', required=True)
    test_email_subject = fields.Char(string='Test Email Subject', default='Test Email from Odoo')
    test_email_body = fields.Text(string='Test Email Body', default='This is a test email sent from Odoo.')
    sender_email = fields.Char(string='Sender Email', required=True, help="Email of the user sending the message")

    def get_access_token(self):
        """
        Fetch the access token using OAuth2.
        """
        url = 'https://login.microsoftonline.com/{}/oauth2/v2.0/token'.format(self.tenant_id)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': self.client_id,
            'scope': 'https://graph.microsoft.com/.default',
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_info = response.json()
            self.access_token = token_info.get('access_token')
            return self.access_token
        else:
            raise UserError(_('Failed to fetch access token: %s') % response.content)

    def send_email(self, to_email, subject, body, user_id):
        """
                Send an email via Office 365 using the Microsoft Graph API.
                """
        token = self.get_access_token()  # Ensure you get a valid access token
        if not token:
            raise UserError(_('Failed to get access token'))

        # Define the URL for sending the email
        url = f'https://graph.microsoft.com/v1.0/users/{user_id}/sendMail'  # Use 'me' to send as the authenticated user

        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json'
        }

        # Prepare the email data
        email_data = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": body
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": to_email
                        }
                    }
                ],
            }
        }

        # Send the email request
        response = requests.post(url, headers=headers, json=email_data)
        if response.status_code != 202:
            raise UserError(_('Failed to send email: %s') % response.content)
        else:
            return True
    def action_send_test_email(self):
        """
                Trigger method to send a test email.
                """
        if not self.test_email_to:
            raise UserError(_('Please enter a recipient email address.'))
        self.send_email(
            to_email=self.test_email_to,
            subject=self.test_email_subject,
            body=self.test_email_body,
            user_id=self.sender_email
        )
        return True
    def action_test_access_token(self):
        url = "https://graph.microsoft.com/v1.0/me/sendMail"
        token = self.get_access_token()  # Ensure you get a valid access token
        headers = {
            "Authorization": 'Bearer {}'.format(token),
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)  # Use GET just to test connectivity

        print(response.status_code)
        print(response.content)