from odoo import api, models, fields, _

class MoBargingMaterialMovement(models.Model):
    _name = "mo.barging.material.movement"
    _description = "Model for MO Barging Material Movement"

    mitra = fields.Many2one("res.partner", string="Mitra", required=True)
    shift = fields.Selection([
        ("shift_1", "Shift 1"),
        ("shift_2", "Shift 2"),
    ], string="Shift", required=True)
    cp = fields.Selection([
        ("eto", "ETO"),
        ("sh_jt", "SH_JT"),
    ], string="CP", required=True)
    tb = fields.Char(string="TB")
    eto = fields.Char(string="ETO")
    loader = fields.Char(string="Loader")
    bg = fields.Char(string="BG")
    hauler = fields.Char(string="Hauler")
    trim = fields.Char(string="Trim")
    tanggal = fields.Date(string="Tanggal", required=True)
    notes = fields.Text(string="Catatan")
    total_movement = fields.Integer(string='Total Movement', compute='_compute_totals', store=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("approval_1", "Approved By Checker"),
        ("approval_2", "Approved By Pengawas MOP"),
    ], string="Status", default="draft")
    approval_1 = fields.Many2one("res.users", string="Checker")
    approval_2 = fields.Many2one("res.users", string="Pengawas MOP")

    barge_item = fields.One2many("mo.barging.material.movement.item", "id_barge", string="Movement")

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

        return super(MoBargingMaterialMovement, self).create(vals)

    def _compute_button_visibility(self):
        for record in self:
            # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.current_step_id.user_id.id == self.env.user.id)
            else:
                record.button_visible = False

    @api.depends('barge_item.f1','barge_item.f2','barge_item.f3','barge_item.f4')
    def _compute_totals(self):
        for record in self:
            if record.shift == "shift_1":
                periods = ['1', '2', '3', '4', '5', '6', '13', '14', '15', '16', '17', '18']
            else:
                periods = ['7', '8', '9', '10', '11', '12', '19', '20', '21', '22', '23', '24']

            # Count non-empty fields for first half
            filtered_movement = record.barge_item.filtered(lambda l: l.hrs_selection in periods)
            total_movement = sum(1 for line in filtered_movement if line.f1) + \
                               sum(1 for line in filtered_movement if line.f2) + \
                               sum(1 for line in filtered_movement if line.f3) + \
                               sum(1 for line in filtered_movement if line.f4)

            # Set computed totals
            record.total_movement = total_movement * 2

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
                records = self.env["mo.barging.material.movement"].browse(self.id)
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
                records = self.env["mo.barging.material.movement"].browse(self.id)
                records.write(vals)
            else:
                return True
class MoBmmItems(models.Model):
    _name = "mo.barging.material.movement.item"
    _description = "Model for MO Barging Material Movement Item"

    hauler = fields.Char(string="Hauler", required=True)
    hrs_selection = fields.Selection([
        ("1", "07-08"),
        ("2", "08-09"),
        ("3", "09-10"),
        ("4", "10-11"),
        ("5", "11-12"),
        ("6", "12-13"),
        ("7", "13-14"),
        ("8", "14-15"),
        ("9", "15-16"),
        ("10", "16-17"),
        ("11", "17-18"),
        ("12", "18-19"),
        ("13", "19-20"),
        ("14", "20-21"),
        ("15", "21-22"),
        ("16", "22-23"),
        ("17", "23-00"),
        ("18", "00-01"),
        ("19", "01-02"),
        ("20", "02-03"),
        ("21", "03-04"),
        ("22", "04-05"),
        ("23", "05-06"),
        ("24", "06-07"),
    ], string="Periode", required=True)
    f1 = fields.Char(string="1")
    f2 = fields.Char(string="2")
    f3 = fields.Char(string="3")
    f4 = fields.Char(string="4")

    id_barge = fields.Many2one("mo.barging.material.movement", string="ID Barge")

