from odoo import api, models, fields, _
from datetime import datetime

class MoPurchaseReq(models.Model):
    _name = "mo.purchase.req"

    pr_no = fields.Char(string="PR No.", required="True")
    request_date = fields.Date(string="Date of Request", required="True", default=lambda self: str(datetime.now()))
    user_id = fields.Many2one('res.users', string="Requested By", default=lambda self: self.env.user.id)
    satker_id = fields.Char(string="Divisi / Department", required="True")
    file = fields.Binary(string="Soft Copy Form PR", required=True)

    mine_ops_approve_by = fields.Many2one('res.users', string="Mine Operation Approved By")
    mine_ops_approve_at = fields.Date(string="Mine Operation Approved At")

    review_by = fields.Many2one('res.users', string="Reviewed & Checked By")
    review_at = fields.Date(string="Reviewed & Checked At")

    mine_mgr_approve_by = fields.Many2one('res.users', string="Approved By Mine Manager")
    mine_mgr_approve_at = fields.Date(string="Mine Manager Approved At")

    approval_step = fields.Selection([
        ('draft', 'Draft'),
        ('approval_1', 'Mine Operation'),
        ('approval_2', 'Reviewed & Checked'),
        ('approval_3', 'Approved by Mine Manager'),
    ], default="draft", string="Approval Step")

    @api.depends('approval_step')
    def _compute_approval_step_colored(self):
        for record in self:
            if record.approval_step == 'draft':
                color = 'background-color: #f0ad4e; color: white;'  # Yellow background
            elif record.approval_step == 'approval_1':
                color = 'background-color: #337ab7; color: white;'  # Blue background
            elif record.approval_step == 'approval_2':
                color = 'background-color: #5cb85c; color: white;'  # Green background
            elif record.approval_step == 'approval_3':
                color = 'background-color: #d9534f; color: white;'  # Red background
            else:
                color = 'background-color: #777; color: white;'  # Gray for undefined

            # Wrap the approval step in a styled pill (badge)
            record.approval_step_colored = (
                f'<span style="{color} padding: 3px 10px; border-radius: 15px; display: inline-block;">'
                f'{dict(record._fields["approval_step"].selection).get(record.approval_step)}</span>'
            )

    approval_step_colored = fields.Html(string="Approval Step Colored", compute='_compute_approval_step_colored')