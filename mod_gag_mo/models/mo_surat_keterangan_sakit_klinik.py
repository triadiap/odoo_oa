from odoo import api, fields, models, _

class MoSuratKeteranganSakitKlinik(models.Model):
    _name = "mo.sk.sakit.klinik"
    _description = "Model for MO Surat Keterangan Sakit Klinik module"

    nama_pegawai = fields.Many2one("res.users", string="Nama", required=True)
    usia = fields.Integer(string="Usia", required=True)
    jenis_kelamin = fields.Selection([
        ("laki_laki", "Laki-Laki"),
        ("perempuan", "Perempuan"),
    ], string="Jenis Kelamin", required=True)
    divisi = fields.Char(string="Divisi", required=True)
    waktu_berobat = fields.Datetime(string="Waktu & Jam Berobat", requiired=True)
    tipe_perawatan = fields.Selection([
        ("jalan", "Rawat Jalan"),
        ("inap", "Rawat Inap"),
    ], string="Tipe Perawatan", required=True)
    diagnosa = fields.Char(string="Diagnosa", required=True)
    lama_istirahat = fields.Integer(string="Lama Istirahat (hari)", required=True)
    tanggal_mulai = fields.Date(string="Tanggal Mulai Istirahat", required=True)
    tanggal_selesai = fields.Date(string="Tanggal Selesai", required=True)
    keterangan = fields.Text(string="Keterangan")
    file_surat = fields.Binary(string="Hasil Scan Surat Klinik", required=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("approval_1", "Approved")
    ], string="Status", default="draft")
    approval_1 = fields.Many2one("res.users", string="Manager Divisi")

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

        return super(MoSuratKeteranganSakitKlinik, self).create(vals)

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