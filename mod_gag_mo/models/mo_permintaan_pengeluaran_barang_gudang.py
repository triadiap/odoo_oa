from odoo import api, fields, models, _
from datetime import datetime

class MoPermintaanPengeluaranBarangGudang(models.Model):
    _name = "mo.permintaan.pengeluaran.barang"
    _description = "Model for MO Permintaan Pengeluaran Barang Gudang"

    req_by = fields.Many2one("res.users", string="Nama", required=True)
    bagian = fields.Char(string="Bagian", required=True)
    tanggal = fields.Date(string="Tanggal", required=True, default=datetime.today())
    state = fields.Selection([
        ("draft", "Draft"),
        ("approval_1", "Telah Diketahui Petugas"),
        ("approval_2", "Disetujui"),
        ("approval_3", "Approved By Petugas Gudang")
    ], string="Status", default="draft")
    approval_1 = fields.Many2one("res.users", string="Diketahui Oleh")
    approval_2 = fields.Many2one("res.users", string="Disetujui Oleh")
    approval_3 = fields.Many2one("res.users", string="Petugas Gudang")

    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', readonly=True, tracking=True)
    existing_status = fields.Char(string="Current Status", readonly=True, tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", readonly=True, tracking=True)
    button_visible = fields.Boolean(string="BVS", compute='_compute_button_visibility', store=False)

    id_item = fields.One2many("mo.permintaan.pengeluaran.barang.item", "id_request", string="Jumlah Barang")

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

        return super(MoPermintaanPengeluaranBarangGudang, self).create(vals)

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
        next_step = self.approval_route_id.get_next_step(self.current_step_id)
        if next_step:
            vals = {
                'current_step_id': next_step,
                'pending_approval_by': next_step.user_id,
                'upcoming_status': next_step,
            }
            records = self.env['mo.permintaan.pengeluaran.barang'].browse(self.id)
            records.write(vals)

    def action_approval_2(self):
        self.state = "approval_2"
        self.approval_2 = self.env.user.id
        next_step = self.approval_route_id.get_next_step(self.current_step_id)
        if next_step:
            vals = {
                'current_step_id': next_step,
                'pending_approval_by': next_step.user_id,
                'upcoming_status': next_step,
            }
            records = self.env['mo.permintaan.pengeluaran.barang'].browse(self.id)
            records.write(vals)

    def action_approval_3(self):
        self.state = "approval_3"
        self.approval_3 = self.env.user.id
        next_step = self.approval_route_id.get_next_step(self.current_step_id)
        if next_step:
            vals = {
                'current_step_id': next_step,
                'pending_approval_by': next_step.user_id,
                'upcoming_status': next_step,
            }
            records = self.env['mo.permintaan.pengeluaran.barang'].browse(self.id)
            records.write(vals)
        else:
            return True

class MoPermintaanBarangItem(models.Model):
    _name = "mo.permintaan.pengeluaran.barang.item"
    _description = "Model for MO Permintaan Pengeluaran Barang Item"

    name = fields.Char(string="Nama Barang", required=True)
    jumlah = fields.Float(string="Jumlah", required=True)
    unit = fields.Char(string="Unit", required=True)
    keterangan = fields.Char(string="Keterangan")

    id_request = fields.Many2one("mo.permintaan.pengeluaran.barang", string="ID Request")