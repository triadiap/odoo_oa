from odoo import api, models, fields, _

class HcTicketing(models.Model):
    _name = "hc.ticketing"
    _description = "Model for HC Ticketing"

    name = fields.Char(string="No. Nota Dinas", required=True)
    req_date = fields.Date(string="Tanggal",required=True)
    file = fields.Binary(string="Soft Copy Nota Dinas", required=True)
    ticket_total = fields.Integer(string="Ticket Total", compute="_compute_tasklist_done_count")
    ticket_total_on = fields.Integer(string="Ticket Total", compute="_compute_tasklist_done_count_on")
    ticket_done = fields.Integer(string="Ticket Done", compute="_compute_tasklist_done_count")
    ticket_progres = fields.Char(string="Off Site Ticket Diproses", compute="_compute_tasklist_progress")
    ticket_done_on = fields.Integer(string="Ticket Done", compute="_compute_tasklist_done_count_on")
    ticket_progres_on = fields.Char(string="On Site Ticket Diproses", compute="_compute_tasklist_progress_on")

    ticket_item = fields.One2many("hc.ticketing.items", "id_nota_dinas", string="Ticket")
    ticket_item_on = fields.One2many("hc.ticketing.items.on", "id_nota_dinas_on", string="Ticket")

    @api.depends('ticket_item.state')
    def _compute_tasklist_done_count(self):
        for task in self:
            task.ticket_done = len(task.ticket_item.filtered(lambda t: t.state == 'done'))
            task.ticket_total = len(task.ticket_item)

    @api.depends('ticket_done', 'ticket_total')
    def _compute_tasklist_progress(self):
        for task in self:
            task.ticket_progres = f"{task.ticket_done} / {task.ticket_total}"

    @api.depends('ticket_item_on.state')
    def _compute_tasklist_done_count_on(self):
        for task in self:
            task.ticket_done_on = len(task.ticket_item_on.filtered(lambda t: t.state == 'done'))
            task.ticket_total_on = len(task.ticket_item_on)

    @api.depends('ticket_done_on', 'ticket_total_on')
    def _compute_tasklist_progress_on(self):
        for task in self:
            task.ticket_progres_on = f"{task.ticket_done_on} / {task.ticket_total_on}"


class HcTicketingItems(models.Model):
    _name = "hc.ticketing.items"
    _description = "Model for HC Ticketing Items"

    leave_id = fields.Many2one('hr.leave', string="Ref. Cuti", domain=[('state', '=', 'validate'), ('holiday_status_id', '=', 1)])
    name = fields.Char(string="Nama Karyawan", related="leave_id.employee_id.name", readonly=True, store=True)
    divisi = fields.Char(string="Divisi", related="leave_id.employee_id.department_id.name", readonly=True, store=True)
    tanggal = fields.Date(string="Tanggal", related="leave_id.request_date_from", readonly=True, store=True)
    keterangan = fields.Char(string="Keterangan", default="Off", readonly=True)
    tujuan = fields.Char(string="Tujuan", required=True)
    state = fields.Selection([
        ("pending", "Pending"),
        ("done", "Done"),
    ], string="Status", default="pending")

    id_nota_dinas = fields.Many2one("hc.ticketing", string="Nota Dinas")

    def set_done(self):
        for record in self:
            self.state = "done"

class HcTicketingItemsOn(models.Model):
    _name = "hc.ticketing.items.on"
    _description = "Model for HC Ticketing Items On Site"

    employee_id = fields.Many2one("hr.employee", string="Nama Karyawan", store=True)
    divisi = fields.Char(string="Divisi", related="employee_id.department_id.name", readonly=True, store=True)
    tanggal = fields.Date(string="Tanggal", store=True)
    keterangan = fields.Char(string="Keterangan", default="On", readonly=True)
    tujuan = fields.Char(string="Tujuan", required=True)
    state = fields.Selection([
        ("pending", "Pending"),
        ("done", "Done"),
    ], string="Status", default="pending")

    id_nota_dinas_on = fields.Many2one("hc.ticketing", string="Nota Dinas")

    def set_done(self):
        for record in self:
            self.state = "done"