from odoo import api, models, fields, _
from datetime import datetime

class MoJobPending(models.Model):
    _name = "mo.job.pending"
    _description = "Model for MO Job Pending"

    tanggal = fields.Date(string="Tanggal", required=True, default=datetime.today())
    id_pegawai = fields.Many2one("res.users", string="Nama Pelapor", default=lambda self: self.env.user.id, required=True)
    jabatan = fields.Char(string="Jabatan", required=True)
    approval_1 = fields.Many2one("res.users", string="Penerima")
    state = fields.Selection([
        ("draft", "Draft"),
        ("approved", "Approved"),
    ], string="Status", default="draft")
    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', readonly=True, tracking=True)
    existing_status = fields.Char(string="Current Status", readonly=True, tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", readonly=True, tracking=True)
    button_visible = fields.Boolean(compute='_compute_button_visibility', store=False)

    id_detail = fields.One2many("mo.job.pending.detail", "id_job", string="List Pending")

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

        return super(MoJobPending, self).create(vals)

    def _compute_button_visibility(self):
        for record in self:
            # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.current_step_id.user_id.id == self.env.user.id)
            else:
                record.button_visible = False

    def action_approval_1(self):
        self.state = "approved"
        self.approval_1 = self.env.user.id

class MoJobPendingDetail(models.Model):
    _name = "mo.job.pending.detail"
    _description = "Model for MO Job Pending Detail"

    job_pending = fields.Char(string="Job Pending")
    notes = fields.Char(string="Note")

    id_job = fields.Many2one("mo.job.pending", "ID Job")