from odoo import api, models, fields, _

class HcTicketing(models.Model):
    _name = "hc.ticketing"
    _description = "Model for HC Ticketing"

    name = fields.Char(string="No. Nota Dinas", required=True)
    req_date = fields.Date(string="Tanggal",required=True)
    file = fields.Binary(string="Soft Copy Nota Dinas", required=True)
    ticket_total = fields.Integer(string="Ticket Total", compute="_compute_tasklist_done_count")
    ticket_done = fields.Integer(string="Ticket Done", compute="_compute_tasklist_done_count")
    ticket_progres = fields.Char(string="Selesai Diproses", compute="_compute_tasklist_progress")

    ticket_item = fields.One2many("hc.ticketing.items", "id_nota_dinas", string="Ticket")

    @api.depends('ticket_item.state')
    def _compute_tasklist_done_count(self):
        for task in self:
            task.ticket_done = len(task.ticket_item.filtered(lambda t: t.state == 'done'))
            task.ticket_total = len(task.ticket_item)

    @api.depends('ticket_done', 'ticket_total')
    def _compute_tasklist_progress(self):
        for task in self:
            task.ticket_progres = f"{task.ticket_done} / {task.ticket_total}"


class HcTicketingItems(models.Model):
    _name = "hc.ticketing.items"
    _description = "Model for HC Ticketing Items"

    name = fields.Char(string="Nama Karyawan", required=True)
    divisi = fields.Char(string="Divisi", required=True)
    tanggal = fields.Date(string="Tanggal", required=True)
    keterangan = fields.Selection([
        ("on", "On"),
        ("off", "Off")
    ], string="Keterangan", required=True)
    tujuan = fields.Char(string="Tujuan", required=True)
    state = fields.Selection([
        ("pending", "Pending"),
        ("done", "Done"),
    ], string="Status", default="pending")

    id_nota_dinas = fields.Many2one("hc.ticketing", string="Nota Dinas")

    def set_done(self):
        for record in self:
            self.state = "done"