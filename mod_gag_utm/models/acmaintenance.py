from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class AirConditioningMaintenanceRequest(models.Model):
    _name = 'oa.acmaintenance.request'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Office Automation Air Conditioning Maintenance Request Form'

    name = fields.Char(string="Deskripsi Pekerjaan", required=True, tracking=True)
    equipment_id = fields.Many2one('oa.master.equipment', string='Nama Equipment')
    brand_model_type = fields.Char(string='Merek/Tipe/Thn Pembuatan')
    serial_number = fields.Char(string='Nomor Seri')
    asset_number = fields.Char(string='Nomor Asset')
    pkt_number = fields.Char(string='Code No')
    kwh_equipment = fields.Char(string='Voltage')
    request_id = fields.Char(string="Request ID", readonly=True, copy=False, default='New')
    location_id = fields.Many2one('msdata.location', required=True, tracking=True,string="Lokasi")
    request_note = fields.Text(string="Notes", tracking=True)
    date_to_action_need = fields.Date(string="Jadwal Pekerjaan", required=True, tracking=True)
    ac_technicians = fields.Many2many('res.users', string="Teknisi Yang Ditunjuk", tracking=True)
    schedule_type = fields.Char(string="Tipe Penjadwalan")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit_request', 'Submitted'),
        ('assigned', 'Technician Assignment'),
        ('work_in_progress', 'Work In Progress'),
        ('approval_process', 'Approval Process'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancelled')
    ], default="draft", string="Status", tracking=True)
    action_priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], default='1', string="Level Prioritas", tracking=True)
    picture_before_1 = fields.Binary(string="Foto Sebelum Pengerjaan")
    picture_after_1 = fields.Binary(string="Foto Sesudah Pengerjaan")
    job_confirmation_date = fields.Date(string="Tanggal & Jam Konfirmasi Pekerjaan")
    job_finalization_date = fields.Date(string="Tanggal Selesai Pekerjaan")
    color = fields.Integer(string="Color", compute='_compute_color',store=True)

    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', tracking=True)
    existing_status = fields.Char(string="Status Terkini", tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Status Berikutnya', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Menunggu Persetujuan", readonly=True, tracking=True)
    button_visible = fields.Boolean(compute='_compute_button_visibility', store=False)
    button_done_visible = fields.Boolean(compute='_compute_done_button_visibility', store=False)
    cancel_button_visibility = fields.Boolean(compute='_compute_cancel_button_visibility', store=False)
    text_input_activation = fields.Boolean(compute='_compute_text_input_activation', store=False)

    def _compute_color(self):
        for record in self:
            if record.state == 'draft':
                record.color = 4  # Blue
            elif record.state == 'submit_request':
                record.color = 4  # Blue
            elif record.state == 'assigned':
                record.color = 4  # Blue
            elif record.state == 'work_in_progress':
                record.color = 4  # Blue
            elif record.state == 'approval_process':
                record.color = 4  # Blue
            elif record.state == 'approve':
                record.color = 10  # Green
            elif record.state == 'done':
                record.color = 10  # Green
            elif record.state == 'rejected':
                record.color = 2  # Red
            else:
                record.color = 2  # Red

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.request_id} - {record.location_id.display_name} - {record.name}"
            result.append((record.id, name))
        return result

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id:
            self.serial_number = self.equipment_id.serial_number
            self.asset_number = self.equipment_id.asset_number
            self.pkt_number = self.equipment_id.pkt_number
            self.kwh_equipment = self.equipment_id.equipment_capacity_input
            self.brand_model_type = f"{self.equipment_id.brand_name}/{self.equipment_id.equipment_model}/{self.equipment_id.manuf_year}"
        else:
            self.serial_number = None
            self.asset_number = None
            self.pkt_number = None
            self.kwh_equipment = None
            self.brand_model_type = None

    @api.model
    def create(self, vals):
        if vals.get('request_id', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('oa.acmaintenance.request') or '00000'
            vals['request_id'] = f'REQ-{sequence}'
        if vals.get('request_id'):
                equip_id = self.env['oa.master.equipment'].browse(vals['equipment_id'])
                vals.update({
                    'serial_number': equip_id.serial_number,
                    'asset_number': equip_id.asset_number,
                    'brand_model_type': f"{equip_id.brand_name}/{equip_id.equipment_model}/{equip_id.manuf_year}/",
                    'pkt_number': equip_id.pkt_number,
                    'kwh_equipment':equip_id.equipment_capacity_input
                })
        else:
                vals.update({
                    'serial_number': None,
                    'asset_number': None,
                    'brand_model_type': None,
                    'pkt_number': None,
                    'kwh_equipment': None
                })
        return super().create(vals)

    def write(self,vals):
        for record in self:
            if 'equipment_id' in vals or record.equipment_id:
                equip_id = record.equipment_id if 'equipment_id' not in vals else self.env['oa.master.equipment'].browse(
                    vals['equipment_id'])
                vals.update({
                    'serial_number': equip_id.serial_number,
                    'asset_number': equip_id.asset_number,
                    'brand_model_type': f"{equip_id.brand_name}/{equip_id.equipment_model}/{equip_id.manuf_year}",
                    'pkt_number': equip_id.pkt_number,
                    'kwh_equipment':equip_id.equipment_capacity_input,
                    'schedule_type': self.schedule_type
                })
        return super(AirConditioningMaintenanceRequest, self).write(vals)
        self._compute_color()

    def _compute_text_input_activation(self):
        for record in self:
            record.text_input_activation = (
                record.env.user == record.create_uid and record.state == 'submit_request'
            )

    def _compute_done_button_visibility(self):
        for record in self:
            record.button_done_visible = (
                record.env.user == record.create_uid and record.state == 'approve'
            )

    def _compute_cancel_button_visibility(self):
        for record in self:
            record.cancel_button_visibility = (
                record.env.user == record.create_uid and record.state in ['rejected', 'submit_request']
            )

    def _compute_button_visibility(self):
        for record in self:
            record.button_visible = record.pending_approval_by == self.env.user

    def submit_as_request(self):
        config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
        if config:
            self.write({
                'approval_route_id': config.approval_route_id.id,
                'state': 'submit_request'
            })
        else:
            raise ValidationError(_('No Approval Route Configured for this process.'))

    def submit_technician_assignment(self):
        if not self.ac_technicians:
            raise ValidationError(_('Technicians must be assigned first.'))
        self.state = 'assigned'

    def submit_job_confirmation_process(self):
        self.write({
            'job_confirmation_date': datetime.now(),
            'state': 'work_in_progress',
        })

    def technician_confirmation_as_done(self):
        if not self.approval_route_id:
            raise ValidationError(_('Approval route is not defined.'))
        next_step = self.approval_route_id.step_ids.sorted(key='sequence')[0]
        self.write({
            'current_step_id': next_step.id,
            'state': 'approval_process',
            'existing_status': _('Tasklist submitted for approval'),
            'pending_approval_by': next_step.user_id.id,
            'upcoming_status': next_step.id,
            'job_finalization_date': datetime.now(),
        })

    def request_set_as_done(self):
        self.state = 'done'
        self._compute_color()

    def action_draft(self):
        self.state = 'draft'
        self._compute_color()

    def next_maintenance_schedule_generated(self,equipment_id,job_finalization_date):
        equipmentdata = self.env['oa.master.equipment'].search([('id', '=', equipment_id.id)])
        for result in equipmentdata:
            id_equipment = result.id
            general_maintenance_frequency = result.general_maintenance_frequency
            if general_maintenance_frequency:
                next_maintenance_datetime = job_finalization_date + timedelta(days=general_maintenance_frequency)
                similar_schedule_check = self.env['oa.acmaintenance.request'].search([('name', '=', f"AC Maintenance - {equipment_id.name} / {equipment_id.location_id.location_name}"),('date_to_action_need','=',next_maintenance_datetime),('equipment_id','=',equipment_id.id)])
                if not similar_schedule_check:
                    id_ac_maintenance = self.env['ir.sequence'].next_by_code('oa.acmaintenance.request') or '00000'
                    sequence_number = f'REQ-{id_ac_maintenance}'
                    acmaintenance_taskid = self.create({
                        'request_id':sequence_number,
                        'name' : f"AC Maintenance - {result.name} / {result.location_id.location_name}",
                        'location_id' : result.location_id.id,
                        'equipment_id' : id_equipment,
                        'date_to_action_need' : next_maintenance_datetime,
                        'brand_model_type' : f"{result.brand_name}/{result.equipment_model}/{result.manuf_year}",
                        'serial_number' : result.serial_number,
                        'asset_number' : result.asset_number,
                        'pkt_number' : result.pkt_number,
                        'kwh_equipment' : result.equipment_capacity_input,
                        'schedule_type' : 'Auto'
                    })
                    group = self.env['res.groups'].search(
                        [('name', '=', 'OA-Utility And Maintenance')],
                        limit=1)
                    summary = f"REQ-{id_ac_maintenance} - {result.name} / {result.location_id.location_name}"
                    notes = f"New AC Maintenance Task Generated for {equipment_id.name}"
                    # Check if the group exists
                    if group:
                        # Get the list of users under this group
                        users = group.users
                        # Iterate over users and print their names
                        for user in users:
                            self.acmaintenance_schedule_activity(acmaintenance_taskid.id, summary, notes, next_maintenance_datetime,user)
                    else:
                        print("Group not found.")
                else:
                    raise ValidationError("Scheduled Maintenance Already Exist")
    def acmaintenance_schedule_activity(self,acmaintenance_taskid,summary,notes,task_planning_date,user):
        # Step 2: Retrieve the `res_model_id` explicitly
        model_id = self.env['ir.model']._get('oa.acmaintenance.request')  # Retrieve the model's ID
        if not model_id:
            raise ValidationError("The model 'oa.acmaintenance.request' could not be found. Ensure it is defined correctly.")
        # Step 3: Create a mail activity linked to the created record
        self.env['mail.activity'].sudo().create({
            'res_model_id': model_id.id,  # Use the retrieved model ID
            'res_id': acmaintenance_taskid,  # Use the ID of the created maintenance task
            'activity_type_id': 8,  # Replace with the correct activity type ID
            'summary': summary,
            'note': notes,
            'user_id': user.id,  # Assigned user
            'date_deadline': task_planning_date,
        })



