from odoo import api, models, fields, _

class MoDaftarHadirMain(models.Model):
    _name = "mo.daftarhadir.main"

    _description = "Model for MO Daftar Hadir"

    tanggal = fields.Date(string="Tanggal", required=True)
    shift = fields.Selection([
        ('1', 'Shift 1'),
        ('2', 'Shift 2'),
    ], string="Shift", default="1", required=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("approval_1", "Approved"),
    ], string="Status", default="draft")
    approval_1 = fields.Many2one("res.users", string="Approval")

    anggota = fields.One2many("mo.daftarhadir.anggota", "id_anggota", string="Jumlah Anggota")

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

        return super(MoDaftarHadirMain, self).create(vals)

    def _compute_button_visibility(self):
        for record in self:
            # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.current_step_id.user_id.id == self.env.user.id)
            else:
                record.button_visible = False

    def action_approval_1(self):
        self.state = "approval_1"
        self.approval_1 = self.env.user.id

class MoDaftarHadirItem(models.Model):
    _name = "mo.daftarhadir.anggota"

    _description = "Model for MO Daftar Hadir Anggota"

    nama_anggota = fields.Many2one('res.users', string="Nama Pekerja")
    jam_masuk = fields.Datetime(string="Jam Masuk", required=True)
    jam_pulang = fields.Datetime(string="Jam Pulang", required=True)
    overtime = fields.Integer(string="Overtime", default=0)

    id_anggota = fields.Many2one("mo.daftarhadir.main", string="Base Table")