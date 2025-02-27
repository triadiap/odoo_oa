from odoo import api, fields, models, _
from datetime import date

class MoPermintaanApd(models.Model):
    _name = "mo.permintaan.apd"
    _description = "Main model for MO Permintaan APD module"

    req_by = fields.Many2one("res.users", string="Nama", required=True, default=lambda self:self.env.user.id)
    req_date = fields.Date(string="Tanggal", required=True, default="")
    lokasi = fields.Char(string="Lokasi", required=True)
    jabatan = fields.Char(string="Jabatan", required=True)
    divisi = fields.Char(string="Divisi / Bagian", required=True)
    jenis_pengajuan = fields.Selection([
        ("permintaan_awal", "Permintaan Awal APD"),
        ("penggantian", "Penggantian APD"),
        ("permintaan_karena_hilang", "Permintaan APD karena kehilangan")
    ], string="Jenis Pengajuan", required=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("approval_1", "Approved By Pengawas Lapangan"),
        ("approval_2", "Approved By Manager"),
        ("approval_3", "Approved By Petugas Safety"),
    ], string="Status", default="draft")
    approval_1 = fields.Many2one("res.users", string="Pengawas Lapangan")
    approval_2 = fields.Many2one("res.users", string="Manager")
    approval_3 = fields.Many2one("res.users", string="Petugas Safety")

    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', readonly=True, tracking=True)
    existing_status = fields.Char(string="Current Status", readonly=True, tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", readonly=True, tracking=True)
    button_visible = fields.Boolean(string="BVS", compute='_compute_button_visibility', store=False)

    id_item = fields.Many2many("mo.master.apd", string="Jenis APD yang diajukan")

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

        return super(MoPermintaanApd, self).create(vals)

    def _compute_button_visibility(self):
        for record in self:
            # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.current_step_id.user_id.id == self.env.user.id)
            else:
                record.button_visible = False

    def action_approval_1(self):
        for record in self:
            record.state = "approval_1"
            record.approval_1 = self.env.user.id
            next_step = self.approval_route_id.get_next_step(self.current_step_id)
            if next_step:
                vals = {
                    'current_step_id': next_step,
                    'pending_approval_by': next_step.user_id,
                    'upcoming_status': next_step,
                }
                records = self.env['mo.permintaan.apd'].browse(self.id)
                records.write(vals)

    def action_approval_2(self):
        for record in self:
            record.state = "approval_2"
            record.approval_2 = self.env.user.id
            next_step = self.approval_route_id.get_next_step(self.current_step_id)
            if next_step:
                vals = {
                    'current_step_id': next_step,
                    'pending_approval_by': next_step.user_id,
                    'upcoming_status': next_step,
                }
                records = self.env['mo.permintaan.apd'].browse(self.id)
                records.write(vals)

    def action_approval_3(self):
        for record in self:
            record.state = "approval_3"
            record.approval_3 = self.env.user.id
            next_step = self.approval_route_id.get_next_step(self.current_step_id)
            if next_step:
                vals = {
                    'current_step_id': next_step,
                    'pending_approval_by': next_step.user_id,
                    'upcoming_status': next_step,
                }
                records = self.env['mo.permintaan.apd'].browse(self.id)
                records.write(vals)
            else:
                return True
