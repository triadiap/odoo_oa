from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from datetime import date
class MoCutiRosterStruktural(models.Model):
    _name = "mo.cuti.roster.struktural"

    id_pegawai = fields.Many2one("res.users", string="Nama Pegawai", required=True)
    npp = fields.Char(string="NPP / NIK")
    divisi = fields.Char(string="Jabatan / Divisi")

    cuti_mulai = fields.Date(string="Mulai Cuti", required=True)
    cuti_selesai = fields.Date(string="Selesai", required=True)
    lama_cuti = fields.Integer(string="Lama Cuti", compute='_compute_lama_cuti', store=True)

    alasan = fields.Char(string="Alasan/Keperluan", required=True)
    alamat = fields.Char(string="Alamat selama cuti", required=True)
    poh = fields.Char(string="POH", required=True)
    no_hp = fields.Char(string="No. HP", required=True)

    karyawan_1 = fields.Many2one("res.users", string="Karyawan Pengganti 1", required=True)
    karyawan_2 = fields.Many2one("res.users", string="Karyawan Pengganti 2", required=True)

    approval_1 = fields.Many2one("res.users", string="SPV / Atasan")
    approval_2 = fields.Many2one("res.users", string="Manager Divisi")
    approval_3 = fields.Many2one("res.users", string="GM / KTT")
    approval_4 = fields.Many2one("res.users", string="HC Dept")

    state = fields.Selection([
        ("draft", "Draft"),
        ("approval_1", "Approved By Spv / Atasan"),
        ("approval_2", "Approved By Manager Divisi"),
        ("approval_3", "Approved By GM / KTT"),
        ("approval_4", "Approved By HC Dept"),
        ("rejected", "Rejected")
    ], string="Status", default="draft")

    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', readonly=True, tracking=True)
    existing_status = fields.Char(string="Current Status", readonly=True, tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", readonly=True, tracking=True)
    button_visible = fields.Boolean(compute='_compute_button_visibility', store=False)

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

        return super(MoCutiRosterStruktural, self).create(vals)

    def _compute_button_visibility(self):
        for record in self:
            # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.current_step_id.user_id.id == self.env.user.id)
            else:
                record.button_visible = False

    @api.depends('cuti_mulai', 'cuti_selesai')
    def _compute_lama_cuti(self):
        for record in self:
            if record.cuti_mulai and record.cuti_selesai:
                # Calculate the difference in days
                delta = (record.cuti_selesai - record.cuti_mulai).days
                # Ensure the days difference is non-negative
                record.lama_cuti = max(delta, 0)
            else:
                record.lama_cuti = 0

    @api.constrains("cuti_mulai")
    def _check_cuti_mulai(self):
        for record in self:
            if record.cuti_mulai and record.cuti_mulai < date.today():
                raise ValidationError("Tanggal mulai cuti tidak boleh kurang dari hari ini")

    @api.constrains("cuti_selesai")
    def _check_cuti_selesai(self):
        for record in self:
            if record.cuti_selesai and record.cuti_selesai < record.cuti_mulai:
                raise ValidationError("Tanggal selesai cuti tidak boleh kurang dari tanggal mulai cuti")

    def action_approval_1(self):
        for record in self:
            record.approval_1 = self.env.user.id
            record.state = "approval_1"
            next_step = self.approval_route_id.get_next_step(self.current_step_id)
            if next_step:
                vals = {
                    'current_step_id': next_step,
                    'pending_approval_by': next_step.user_id,
                    'upcoming_status': next_step,
                }
            records = self.env['mo.cuti.roster.struktural'].browse(self.id)
            records.write(vals)

    def action_approval_2(self):
        for record in self:
            record.approval_2 = self.env.user.id
            record.state = "approval_2"
            next_step = self.approval_route_id.get_next_step(self.current_step_id)
            if next_step:
                vals = {
                    'current_step_id': next_step,
                    'pending_approval_by': next_step.user_id,
                    'upcoming_status': next_step,
                }
            records = self.env['mo.cuti.roster.struktural'].browse(self.id)
            records.write(vals)

    def action_approval_3(self):
        for record in self:
            record.approval_3 = self.env.user.id
            record.state = "approval_3"
            next_step = self.approval_route_id.get_next_step(self.current_step_id)
            if next_step:
                vals = {
                    'current_step_id': next_step,
                    'pending_approval_by': next_step.user_id,
                    'upcoming_status': next_step,
                }
            records = self.env['mo.cuti.roster.struktural'].browse(self.id)
            records.write(vals)

    def action_approval_4(self):
        for record in self:
            record.approval_4 = self.env.user.id
            record.state = "approval_4"
            next_step = self.approval_route_id.get_next_step(self.current_step_id)
            if next_step:
                vals = {
                    'current_step_id': next_step,
                    'pending_approval_by': next_step.user_id,
                    'upcoming_status': next_step,
                }
                records = self.env['mo.cuti.roster.struktural'].browse(self.id)
                records.write(vals)
            else:
                return True