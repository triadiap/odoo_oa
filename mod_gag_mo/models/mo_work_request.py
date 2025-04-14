from odoo import api, fields, models, _
from datetime import datetime

class MoWorkRequest(models.Model):
    _name = "mo.work.request"
    _description = "MO Work Request"

    div_from = fields.Many2one("hr.department", string="From", required=True, default=lambda self: self.env.user.department_id.id)
    div_to = fields.Many2one("hr.department", string="To", required=True)
    wo_number = fields.Char(string="Originating Work Order No", required=True)
    est_cost_attch = fields.Selection([
        ("yes", "Yes"),
        ("no", "No")
    ], string="Estimated Cost Attached", default="no", required=True)
    file_attach = fields.Binary(string="Attachment")
    wr_detail_info = fields.Text(string="Work Request Detailed Description", required=True)
    notes = fields.Text(string="Note")
    req_by = fields.Many2one("res.users", string="Request By", required=True)
    req_date = fields.Date(string="Request Date", required=True, default=datetime.today())
    state = fields.Selection([
        ("draft", "Draft"),
        ("approved", "Approved"),
    ], string="Status", default="draft")
    rev_by = fields.Many2one("res.users", string="Review By")
    rev_date = fields.Date(string="Review Date")
    approved_by = fields.Many2one("res.users", string="Approved By")
    approved_date = fields.Date(string="Approved Date")
    work_by = fields.Many2one("res.users", string="Performed By")
    work_date = fields.Date(string="Performed Date")
    acc_by = fields.Many2one("res.users", string="Accepted By")
    acc_date = fields.Date(string="Accepted Date")

    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', readonly=True, tracking=True)
    existing_status = fields.Char(string="Current Status", readonly=True, tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", readonly=True, tracking=True)
    button_visible = fields.Boolean(string="BVS", compute='_compute_button_visibility', store=False)

    @api.model
    def create(self, vals):
        # UAC Find the configured approval route for the current model for new document creation
        config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
        if config:
            vals['approval_route_id'] = config.approval_route_id.id
            next_step = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)],
                                                                       limit=1).approval_route_id.step_ids.sorted(
                key='sequence')[0]
            vals['current_step_id'] = next_step.id
            vals['state'] = 'draft'
            vals['existing_status'] = 'Draft'
            vals['pending_approval_by'] = next_step.user_id.id
            vals['upcoming_status'] = next_step.id

        return super(MoWorkRequest, self).create(vals)

    def _compute_button_visibility(self):
        for record in self:
            # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.current_step_id.user_id.id == self.env.user.id)
            else:
                record.button_visible = False

    def action_approval_1(self):
        self.state = "approved"
        self.approved_by = self.env.user.id
        self.approved_date = datetime.today()