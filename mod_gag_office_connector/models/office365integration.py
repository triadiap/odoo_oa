import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError,ValidationError
import logging
import requests
from datetime import datetime
import base64
import mimetypes




class Office365Integration(models.Model):
    _name = 'office365.integration'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Office 365 Integration'


    name = fields.Char(string="Connection Name",required=True,tracking=True)
    client_id = fields.Char(string='Client ID', required=True,tracking=True)
    client_secret = fields.Char(string='Client Secret', required=True,tracking=True)
    tenant_id = fields.Char(string='Tenant ID', required=True,tracking=True)
    access_token = fields.Text(string='Access Token', readonly=True)
    onedrive_file_ids = fields.One2many('onedrive.file', 'integration_id', string="OneDrive Files")
    calendar_sync_ids = fields.One2many('oa.calendar.sync','calendar_integration_id', string="Calendar")

    # Fields for sending test email
    test_email_to = fields.Char(string='Test Email Recipient', required=True,tracking=True)
    test_email_subject = fields.Char(string='Test Email Subject', default='Test Email from Odoo',tracking=True)
    test_email_body = fields.Text(string='Test Email Body', default='This is a test email sent from Odoo.',tracking=True)
    sender_email = fields.Char(string='Sender Mail', required=True, help="Email of the user sending the message",tracking=True)

    # Fields for file upload to OneDrive
    file_id = fields.Char("OneDrive File ID", readonly=True)
    upload_date = fields.Datetime("Upload Date", readonly=True)
    file_url = fields.Char("File URL", readonly=True)
    file_data = fields.Binary("File Data")
    file_name = fields.Char("File Name")

    #fields for calendar synchronization
    calendar_name = fields.Char("Event Name", required=True,default='Event Testing')
    calendar_start_datetime = fields.Datetime("Start DateTime", required=True,default=fields.Date.context_today)
    calendar_end_datetime = fields.Datetime("End DateTime", required=True,default=fields.Date.context_today)
    calendar_location = fields.Char("Location")
    calendar_description = fields.Text("Description")
    outlook_event_id = fields.Char("Outlook Event ID")  # Store the event ID from Outlook


    def get_access_token(self):
        """
        Fetch the access token using OAuth2.
        """
        url = 'https://login.microsoftonline.com/{}/oauth2/v2.0/token'.format(self.tenant_id)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': self.client_id,
            'scope': 'https://graph.microsoft.com/.default',  # Updated scope,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
            'tenant_id': self.tenant_id
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_info = response.json()
            self.access_token = token_info.get('access_token')
            return self.access_token
        else:
            raise UserError(_('Failed to fetch access token: %s') % response.content)

    def update_mailbox_settings(self, sender_email):
        # Memperbarui pengaturan kotak surat sebelum mengirim email
        access_token = self.get_access_token()
        url = f"https://graph.microsoft.com/v1.0/users/{sender_email}/mailboxSettings"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "timeZone": "Pacific Standard Time"
        }
        response = requests.patch(url, headers=headers, json=data)

        # Tambahkan log error untuk debugging
        if response.status_code != 200:
            raise Exception(
                f"Failed to update mailbox settings. Status code: {response.status_code}, Response: {response.content}")

        return response

    def send_email(self, to_email, subject, body, sender_email):

        token = self.get_access_token()  # Ensure you get a valid access token
        if not token:
            raise UserError(_('Failed to get access token'))

        # Define the URL for sending the email
        url = f'https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail'

        headers = {
            'Authorization': f'Bearer {token}',
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
                ]
            }
        }

        # Send the email request
        response = requests.post(url, headers=headers, json=email_data)
        if response.status_code == 202:
            raise UserError(_('Email Sent!\n\nTest email sent successfully to %s' % to_email))
        else:
            raise UserError(_('Failed to send email: %s') % response.content)
    def action_send_test_email(self):
        if not self.test_email_to:
            raise UserError(_('Please enter a recipient email address.'))
        self.send_email(
            to_email=self.test_email_to,
            subject=self.test_email_subject,
            body=self.test_email_body,
            sender_email=self.sender_email
        )
        return True

    def sync_contacts(self):
        # Call Microsoft Graph API to retrieve contacts
        contacts_data = self.fetch_contacts_from_graph()

        if not contacts_data:
            raise UserError(_('No contacts retrieved from Microsoft Graph.'))
            return

        # Iterate through each contact and process it
        for contact in contacts_data.get('value', []):
            self.create_or_update_contact(contact)
        raise UserError(_('Contact synchronization completed.'))

    def fetch_contacts_from_graph(self):
        # This function calls the Graph API and retrieves all contacts
        token = self.get_access_token()  # Ensure you get a valid access token
        user_id = self.sender_email
        # Get contacts from Microsoft 365
        url =f'https://graph.microsoft.com/v1.0/users/{user_id}/contacts'
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise UserError(_('Failed to fetch contacts: %s') % response.content)
            return None

    def create_or_update_contact(self, contact):
        contact_name = contact.get('displayName', 'No Name')
        email_addresses = contact.get('emailAddresses', [])
        contact_email = email_addresses[0].get('address') if email_addresses else None

        print(f"Syncing contact: Name={contact_name}, Email={contact_email}")

        if contact_email:
            existing_contact = self.env['res.partner'].search([('email', '=', contact_email)], limit=1)
            if existing_contact:
                existing_contact.write({'name': contact_name,
                                        'phone': contact.get('businessPhones', [''])[0] if contact.get('businessPhones') else '',
                                        'mobile': contact.get('mobilePhone', ''),
                                        'company_name': contact.get('companyName'),
                                        'website': contact.get('personalNotes')
                                        })
            else:
                self.env['res.partner'].create({'name': contact_name,
                                                'email': contact_email,
                                                'phone': contact.get('businessPhones', [''])[0] if contact.get('businessPhones') else '',
                                                'mobile': contact.get('mobilePhone', ''),
                                                'company_name': contact.get('companyName'),
                                                'website': contact.get('personalNotes')
                                                })
        else:
            raise UserError(_('Skipped contact with no email address.'))

    def sync_contact_to_microsoft(self):
        token = self.get_access_token()
        user_id = self.sender_email

        if not token:
            raise UserError(_('Failed to get access token'))

        ms_graph_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/contacts"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        partners = self.env['res.partner'].search([])
        success_count = 0
        failure_count = 0

        for partner in partners:
            if not partner.email:
                print(f"Skipping contact '{partner.name}' due to missing email.")
                continue  # Skip if there's no email

                # Check for existing contact by email
            existing_contacts = requests.get(
                    f"{ms_graph_url}?$filter=emailAddresses/any(a:a/address eq '{partner.email}')",
                    headers=headers
                )
            if existing_contacts.status_code == 200:
                existing_contacts_data = existing_contacts.json()
                if existing_contacts_data.get('value'):
                    # Contact already exists, log and skip
                    print(f"Contact '{partner.name}' already exists in Outlook. Skipping synchronization.")
                    continue

            data = {
                "givenName": partner.name or '',
                "surname": partner.name or '',
                "emailAddresses": [{"address": partner.email, "name": partner.name}],
                "businessPhones": [partner.phone or ''],
                "mobilePhone": partner.mobile or '',
                "companyName": partner.company_id.name if partner.company_id else ''
            }

            response = requests.post(ms_graph_url, headers=headers, json=data)

            if response.status_code == 201:
                success_count += 1
            else:
                failure_count += 1

        self.env['mail.message'].create({
            'body': f"Contact synchronization completed. Total successes: {success_count}, Total failures: {failure_count}.",
            'model': self._name,
            'res_id': self.id,
            })

    def fetch_onedrive_files(self):
        token = self.get_access_token()
        user_id = self.sender_email  # Replace with actual user ID or email

        if not token:
            raise UserError(_('Failed to get access token'))

        list_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/root/children"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(list_url, headers=headers)

        if response.status_code == 200:
            files = response.json().get('value', [])
            self.onedrive_file_ids.unlink()  # Clear existing records

            for file in files:
                self.env['onedrive.file'].create({
                    'integration_id': self.id,
                    'name': file.get('name'),
                    'file_id': file.get('id'),
                    'created_date': datetime.strptime(file.get('createdDateTime'),'%Y-%m-%dT%H:%M:%SZ'),
                    'modified_date': datetime.strptime(file.get('lastModifiedDateTime'),'%Y-%m-%dT%H:%M:%SZ'),
                    'size': file.get('size'),
                    'web_url': file.get('webUrl'),
                    'owner': file.get('createdBy', {}).get('user', {}).get('displayName', '')
                })
        else:
            raise UserError(_("Failed to fetch files from OneDrive: %s") % response.text)

    def upload_file_to_onedrive(self):
        """Upload a file from Odoo to OneDrive."""
        if not self.file_data:
            raise UserError("Please select a file to upload.")

        # Ensure `file_name` is defined, or use a default name with extension
        file_name = self.file_name if self.file_name else "default_name"
        extension = self.determine_file_extension(file_name)

        # Check if the file name has an extension; if not, append it
        if not '.' in file_name:
            file_name += extension

        token = self.get_access_token()
        if not token:
            raise UserError("Failed to get access token for OneDrive.")

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/octet-stream'
        }
        upload_url = f"https://graph.microsoft.com/v1.0/users/{self.sender_email}/drive/root:/OdooUploads/{file_name}:/content"

        # Decode the file data from base64
        try:
            file_content = base64.b64decode(self.file_data)
        except Exception as e:
            raise UserError(f"Failed to decode file data: {str(e)}")

        # Upload the file to OneDrive
        response = requests.put(upload_url, headers=headers, data=file_content)

        # Check the response status and handle accordingly
        if response.status_code in [201, 200]:  # 201 is for created, 200 is for successful updates
            file_info = response.json()
            self.write({
                'file_id': file_info.get('id'),
                'upload_date': fields.Datetime.now(),
                'file_url': file_info.get('webUrl'),
            })
            return True
        else:
            error_message = response.json().get('error', {}).get('message', 'Unknown error')
            raise UserError(f"Failed to upload file: {error_message} (Status Code: {response.status_code})")

    def determine_file_extension(self,file_name):
        # First, try to get the MIME type based on the filename
        mime_type, encoding = mimetypes.guess_type(file_name)

        if mime_type:
            # If MIME type is detected, attempt to get the file extension
            extension = mimetypes.guess_extension(mime_type)
            if extension:
                return extension  # Return the detected extension
        # Fallback if no MIME type or extension was detected
        return ".bin"  # Use '.bin' as the default extension

    def delete_onedrive_parameter(self):
        self.upload_date = None
        self.file_id = None
        self.file_url = None
        self.file_data = None
        self.file_name = None

    def sync_to_outlook_calendar(self):
        token = self.get_access_token()
        user_id = self.sender_email  # Replace with actual user ID or email

        # Prepare the event data in Microsoft Graph API format
        event_data = {
            "subject": self.calendar_name,
            "body": {
                "contentType": "HTML",
                "content": self.calendar_description or ""
            },
            "start": {
                "dateTime": self.calendar_start_datetime.isoformat(),
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": self.calendar_end_datetime.isoformat(),
                "timeZone": "UTC"
            },
            "location": {
                "displayName": self.calendar_location or ""
            }
        }
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # URL for creating events in the primary calendar
        url = f"https://graph.microsoft.com/v1.0/users/{user_id}/events"
        response = requests.post(url, headers=headers, json=event_data)

        if response.status_code in [200,201]:
            event_info = response.json()
            self.outlook_event_id = event_info["id"]  # Save the Outlook Event ID
            # Store the log in oa.calendar.sync
            self.env['oa.calendar.sync'].create({
                     'name': self.calendar_name,
                     'start_datetime': self.calendar_start_datetime,
                     'end_datetime': self.calendar_end_datetime,
                     'location': self.calendar_location,
                     'description': self.calendar_description,
                     'event_outlook_id': self.outlook_event_id,
                     'calendar_integration_id': self.id,
            })
            return True
        else:
            # Log the error and raise an exception
            raise ValueError(f"Error synchronizing event: {response.status_code} {response.text}")

    def delete_calendar_parameter(self):
        self.calendar_location = None
        self.calendar_description = None
        self.outlook_event_id = None

class OneDriveFile(models.Model):
    _name = 'onedrive.file'
    _description = 'OneDrive File'

    name = fields.Char("File Name")
    file_id = fields.Char("File ID")
    created_date = fields.Datetime("Created Date")
    modified_date = fields.Datetime("Last Modified Date")
    size = fields.Integer("Size (Bytes)")
    web_url = fields.Char("Web URL")
    owner = fields.Char("Owner")
    integration_id = fields.Many2one('office365.integration', string="Integration")

class CalendarSyncLog(models.Model):
    _name = 'oa.calendar.sync'
    _description = 'Outlook Calendar Sync'

    name = fields.Char("Event Name", required=True)
    start_datetime = fields.Datetime("Start DateTime", required=True)
    end_datetime = fields.Datetime("End DateTime", required=True)
    location = fields.Char("Location")
    description = fields.Text("Description")
    event_outlook_id = fields.Char("Outlook Event ID")  # Store the event ID from Outlook
    calendar_integration_id = fields.Many2one('office365.integration', string="Integration")