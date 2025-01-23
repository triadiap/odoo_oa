from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class ProblemTicketingManagement(models.Model):
    _name = 'oa.issue.ticketing'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'User Issue Ticketing Management And Resolve'

    name =  fields.Char(string="Ticket ID", readonly=True, copy=False, default='New')
    issue_title = fields.Char(string="Title",required=True,tracking=True)
    issue_description = fields.Html(string="Description",sanitize=False,required=True,tracking=True)
    menu_id = fields.Many2one('ir.ui.menu', string="Menu / Module Name", domain=[('parent_id', '=', False)], required=True)
    child_menu_id = fields.Many2one(
        'ir.ui.menu',
        string="Sub Menu",
        domain=[]  # The domain will be set dynamically
    )
    state = fields.Selection([
        ('submitted', 'Submitted'),
        ('inprogress', 'In Progress'),
        ('done', 'Done'),
        ('resolved', 'Resolved'),
        ('cancel', 'Cancelled')
    ], default="submitted", string="Status", tracking=True)
    request_type = fields.Selection([
        ('normal', 'Normal'),
        ('high', 'High')
    ],default="normal", string="Urgency Level", tracking=True,required=True)
    id_attachment = fields.One2many('oa.ticket.attachment', 'attachment_id', string="Attachments")
    button_inprogress_visible = fields.Boolean(compute='_compute_button_visibility', store=False, sanitize=False)
    button_resolve_visible = fields.Boolean(compute='_compute_button_visibility', store=False, sanitize=False)
    button_cancel_visible = fields.Boolean(compute='_compute_button_visibility', store=False, sanitize=False)
    button_revoke_visible = fields.Boolean(compute='_compute_button_visibility', store=False, sanitize=False)
    button_done_visible = fields.Boolean(compute='_compute_button_visibility', store=False, sanitize=False)
    hide_css = fields.Html(string='CSS', compute='_compute_button_visibility', sanitize=False, store=False)

    def _compute_button_visibility(self):
        current_user = self.env.user
        user_groups = current_user.groups_id.mapped('name')
        for record in self:
            record.button_inprogress_visible = False
            record.button_done_visible = False
            record.button_resolve_visible = False
            record.button_cancel_visible = False
            record.button_revoke_visible = False
            # Check conditions and update visibility
            if "Helpdesk-Officer" in user_groups:
                if record.state == "submitted":
                    record.button_inprogress_visible = True
                    record.hide_css = False
                elif record.state == "done":
                    record.button_resolve_visible = True
                    record.hide_css = ('''
                                            <style>
                                              .o_form_button_edit {display:none !important;}
                                            </style>
                                        '''
                                       )
                elif record.state == "inprogress":
                     record.button_cancel_visible = True
                     record.button_done_visible = True
                     record.hide_css = False
                elif record.state == "cancel":
                     record.button_revoke_visible = True
                     record.hide_css = False
            else:
                if record.state == "submitted" and "Helpdesk-Officer" not in user_groups:
                    record.hide_css = False
                else:
                    record.hide_css = ('''
                                            <style>
                                                .o_form_button_edit {display:none !important;}
                                            </style>
                                        ''')
    def action_resolve(self):
        self.state="inprogress"
    def action_back_to_submit(self):
        self.state="submitted"
    def action_done(self):
        self.state = 'done'
    def action_inprogress(self):
        self.state = 'inprogress'
    def action_cancel(self):
        self.state="cancel"

    @api.onchange('menu_id')
    def _onchange_menu_id(self):
        """Dynamically update the domain of child_menu_id based on menu_id."""
        if self.menu_id:
            self.child_menu_id = False  # Reset the value when menu_id changes
            return {
                'domain': {
                    'child_menu_id': [('parent_id', '=', self.menu_id.id)],
                }
            }
        else:
            self.child_menu_id = False
            return {
                'domain': {
                    'child_menu_id': [],
                }
            }

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            current_date = datetime.now()
            # Extract the month,day,and year
            month_number = current_date.month
            day_number = current_date.day
            year = current_date.year
            # Generate the sequence number
            sequence = self.env['ir.sequence'].next_by_code('oa.issue.ticketing') or '00000'
            # Combine them into the final name
            vals['name'] = f'HLP-{sequence}/{month_number}/{day_number}/{year}'
        return super(ProblemTicketingManagement, self).create(vals)

class TicketAttachments(models.Model):
    _name = "oa.ticket.attachment"
    _description = "List Of Attachments"

    name = fields.Char(string="File Name",required=True)
    attachment_id = fields.Many2one('oa.issue.ticketing',string="Attachment ID",ondelete='cascade')
    file_field = fields.Binary(string="File or Document (Upload Here)")

