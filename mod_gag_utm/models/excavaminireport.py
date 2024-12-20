from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class ExcavaMiniDailyChcklistReport(models.Model):
    _name = 'oa.excavaminidaily.report'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Excavator Mini Daily Checklist Report'

    name = fields.Char(string="ID Report", required=True, tracking=True,copy=False, default='New')
    excavamini_report_date = fields.Date(string="Hari / Tanggal",tracking=True,required=True)
    excavamini_equip_id =  fields.Many2one('oa.master.equipment', string='Nama Equipment',required=True)
    excavamini_operator_name = fields.Char(string="Operator / Driver",required=True,tracking=True)
    excavamini_hm_unit = fields.Float(string="Hour Meter (HM) UNIT",required=True,tracking=True)
    excavamini_serial_number = fields.Char(string="Nomor Seri",tracking=True)
    excavamini_model = fields.Char(string="Model",tracking=True)
    excavamini_power = fields.Char(string="Power (Hp)",tracking=True)
    excavamini_shift = fields.Selection([
        ('1','Shift 1'),
        ('2', 'Shift 2'),
        ('3', 'Shift 3'),
    ],default='1',string="Shift", tracking=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('submitted','Submitted'),
        ('approved','Approved'),
        ('rejected','Rejected')
    ],default='draft',string="State", tracking=True)

    id_report = fields.One2many('oa.excavaminidetail.checklist', 'report_id', string="Detail Checklist")
    count_xxx = fields.Integer(compute='_compute_status_counts', string="Kondisi xxx")
    count_xx = fields.Integer(compute='_compute_status_counts', string="Kondisi xx")
    count_x = fields.Integer(compute='_compute_status_counts', string="Kondisi x")

    hide_css = fields.Html(string='CSS', compute='_compute_done_button_visibility', sanitize=False, store=False)
    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', tracking=True)
    existing_status = fields.Char(string="Status Terkini", tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Status Berikutnya', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Menunggu Persetujuan", readonly=True, tracking=True)
    button_visible = fields.Boolean(compute='_compute_button_visibility', store=False)
    button_done_visible = fields.Boolean(compute='_compute_done_button_visibility', store=False)
    cancel_button_visibility = fields.Boolean(compute='_compute_cancel_button_visibility', store=False)
    text_input_activation = fields.Boolean(compute='_compute_text_input_activation', store=False)
    approver_notes = fields.Text(string="Approver Notes",tracking=True)

    def generate_excavamini_tasklist(self,equip_id):
        latest_hm_excavamini_check = self.env['oa.excavaminidaily.report'].search(
            [('excavamini_equip_id', '=', equip_id.id)],
            limit=1,
            order='excavamini_hm_unit desc'
        )
        second_latest_hm_excavamini_check = self.env['oa.excavaminidaily.report'].search(
            [('excavamini_equip_id', '=', equip_id.id)],
            limit=1,
            offset=1,
            order='excavamini_hm_unit desc'
        )
        if latest_hm_excavamini_check:
            second_hm_value = second_latest_hm_excavamini_check.excavamini_hm_unit if second_latest_hm_excavamini_check else 0
            daily_hm_cumulative_value = latest_hm_excavamini_check.excavamini_hm_unit - second_hm_value
            getexcavaminipartchecklist = self.env['oa.master.equipment'].search([('id', '=', equip_id.id)])
            for result_a in getexcavaminipartchecklist:
                related_maintenance_records = result_a.id_detail_maintenance
                if related_maintenance_records:
                    for maintenance_part in related_maintenance_records:
                        if daily_hm_cumulative_value >= maintenance_part.maintenance_freq:
                            sub_group = None
                            get_existing_maintenance_tasklist = self.env['oa.machine.maintenance'].search(
                                [('equip_id', '=', equip_id.id),
                                 ('maintenance_asset_group', '=', equip_id.group_id.id),
                                 ('task_planning_date', '=', fields.Datetime.now()),
                                 ('job_type', '=', "excavamini_checklist"),
                                 ('maintenance_part_name', '=', maintenance_part.part_name)]
                                )
                            if not get_existing_maintenance_tasklist:
                                self.env['oa.machine.maintenance'].generate_maintenance_task(
                                    equip_id,
                                    equip_id.group_id.id,
                                    sub_group,
                                    fields.Datetime.now(),
                                    maintenance_part.id_maintenance_type,
                                    maintenance_part.part_name,
                                    "excavamini_checklist"
                                )


    def action_draft(self):
        for record in self:
            record.state = 'draft'
    def _compute_text_input_activation(self):
        for record in self:
            if record.env.user == record.create_uid:
                if record.state == 'submitted':
                   record.text_input_activation = True
                else:
                    record.text_input_activation = False
            else:
                record.text_input_activation = False
    def _compute_cancel_button_visibility(self):
        for record in self:
            if record.state == 'rejected' or record.state == 'submitted':
                record.cancel_button_visibility = True
            else:
                record.cancel_button_visibility = False
    @api.depends('state','create_uid')
    def _compute_done_button_visibility(self):
        for record in self:
            # Default values
            record.hide_css = ""
            record.button_done_visible = False

            if record.env.user == record.create_uid:
                if record.state == 'draft':
                    record.button_done_visible = True
                else:
                    record.hide_css = ('''
                                        <style>.o_form_button_edit {display: none !important;}</style>
                                        '''
                                       )
                    record.button_done_visible = False
            else:
                record.button_done_visible = False
    def _compute_button_visibility(self):
        for record in self:
            if record.pending_approval_by and record.state == 'submitted':
                record.button_visible = (record.pending_approval_by.id == self.env.user.id)
            else:
                record.button_visible = False
    def submit_as_request(self):
        config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
        if not self.approval_route_id:
            raise ValidationError(_('Approval route is not defined.'))
        next_step = self.approval_route_id.step_ids.sorted(key='sequence')[0]
        if config:
            self.write({
                'current_step_id': next_step.id,
                'approval_route_id': config.approval_route_id.id,
                'state': 'submitted',
                'existing_status':'Report submitted for approval',
                'pending_approval_by': next_step.user_id.id,
                'upcoming_status': next_step.id
            })
        else:
            raise ValidationError(_('No Approval Route Configured for this process.'))

    @api.depends('id_report.kode_bahaya')
    def _compute_status_counts(self):
        for record in self:
            logs = record.id_report
            record.count_xxx = logs.filtered(lambda l: l.kode_bahaya == '3').mapped('id').__len__()
            record.count_xx = logs.filtered(lambda l: l.kode_bahaya == '2').mapped('id').__len__()
            record.count_x = logs.filtered(lambda l: l.kode_bahaya == '1').mapped('id').__len__()

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            today = datetime.today()
            current_month = today.month
            current_year = today.year
            sequence = self.env['ir.sequence'].next_by_code('oa.excavaminidaily.report') or '00000'
            vals['name'] = f'EXC-{sequence}/{current_month}/{current_year}'
        if vals.get('name'):
            equip_id = self.env['oa.master.equipment'].browse(vals['excavamini_equip_id'])
            vals.update({
                'excavamini_serial_number': equip_id.serial_number,
                'excavamini_model': equip_id.equipment_model,
                'excavamini_power': equip_id.equipment_power
            })
        else:
            vals.update({
                'excavamini_serial_number': None,
                'excavamini_model': None,
                'excavamini_power': None
            })
        # UAC Find the configured approval route for the current model for new document creation
        config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
        if config:
                vals['approval_route_id'] = config.approval_route_id.id

        return super().create(vals)

    def write(self,vals):
        for record in self:
            if 'excavamini_equip_id' in vals or record.excavamini_equip_id:
                equip_id = record.excavamini_equip_id if 'excavamini_equip_id' not in vals else self.env['oa.master.equipment'].browse(
                    vals['excavamini_equip_id'])
                config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
                vals.update({
                'excavamini_serial_number': equip_id.serial_number,
                'excavamini_model': equip_id.equipment_model,
                'excavamini_power': equip_id.equipment_power,
                'approval_route_id' : config.approval_route_id.id
                })

        return super(ExcavaMiniDailyChcklistReport, self).write(vals)

    @api.onchange('excavamini_equip_id')
    def _onchange_equipment_id(self):
        if self.excavamini_equip_id:
            self.excavamini_serial_number = self.excavamini_equip_id.serial_number
            self.excavamini_model = self.excavamini_equip_id.equipment_model
            self.excavamini_power = self.excavamini_equip_id.equipment_power
        else:
            self.excavamini_serial_number = None
            self.excavamini_model = None
            self.excavamini_power = None
    def action_get_excavamini_checklist(self):
        getallchecklistmasterdata = self.env['oa.excavaceklist.indikator'].search([])
        checkexistingdata = self.env['oa.excavaminidetail.checklist'].search([('report_id.id', '=', self.id)])
        if checkexistingdata:
            # Unlink (delete) the record
            checkexistingdata.unlink()
            for result in getallchecklistmasterdata:
                vals = {
                    'report_id': self.id,  # Use the extracted ID
                    'name': result.id
                }
                self.env['oa.excavaminidetail.checklist'].create(vals)
        else:
            for result in getallchecklistmasterdata:
                vals = {
                    'report_id': self.id,  # Use the extracted ID
                    'name': result.id
                }
                self.env['oa.excavaminidetail.checklist'].create(vals)


class ExcavaMiniDailyReportDetailChecklist(models.Model):
    _name = 'oa.excavaminidetail.checklist'
    _inherit = ["mail.thread", "mail.activity.mixin", "oa.detailed.maintenance"]
    _description = 'Excavator Mini Detail Daily Checklist Report'

    name = fields.Many2one('oa.excavaceklist.indikator',tracking=True,required=True,string="Indikator Yang Diperiksa")
    kode_bahaya = fields.Selection([
        ('1', 'x'),
        ('2', 'xx'),
        ('3', 'xxx'),
    ], default='1', string="Kode", tracking=True, required=True)
    report_id = fields.Many2one('oa.excavaminidaily.report', string='Detail Checklist',ondelete='cascade')
    equipment_id = fields.Many2one(related='report_id.lv_equip_id', string="Equipment", store=False)
    report_code = fields.Char(related='report_id.name', string="ID Report", store=False)
    excavamini_indicator = fields.Selection([
        ('1','Baik'),
        ('2','Rusak')
    ],default='1',string="Kondisi",tracking=True,required=True)
    excavamini_checklist_remark = fields.Text(string="Keterangan",tracking=True)
    sequence = fields.Integer(string='No', compute='_compute_sequence', store=False)
    equipment_id = fields.Many2one(related='report_id.excavamini_equip_id', string="Equipment", store=False)
    btn_set_schedule = fields.Boolean(compute='_compute_btn_visibility', store=False)
    schedule_set_btn = fields.Boolean(compute='_compute_btn_schedule_visibility', store=False)
    routine_schedule_conf = fields.Boolean(string="Set Routine Activity", default=False, required=True, tracking=True)
    maintenance_schedule_conf = fields.Boolean(string="Set Maintenance Schedule", default=False, required=True,
                                               tracking=True)
    asset_group = fields.Many2one(related="report_id.excavamini_equip_id.group_id",string="Asset Group",store=False)
    maintenance_schedule_date = fields.Date(string="Tanggal Perbaikan / Maintenance")
    measurement_unit = fields.Selection([
        ('hour_meter', 'Hour Meter (HM)'),
        ('kilometer', 'Kilometer (Km)'),
        ('meter', 'Meter (M)')
    ], default='hour_meter', string="Unit Of Measures (UOM) / Satuan", tracking=True)
    maintenance_freq = fields.Float(string="Maintenance Frequency", tracking=True)
    excavamini_maintenance_type = fields.Selection([
        ('top_over_haul', 'TOP OVER HAUL'),
        ('minor_over_haul', 'MINOR OVER HAUL'),
        ('general_over_haul', 'GENERAL OVER HAUL'),
        ('services', 'SERVICES'),
        ('greasing', 'GREASING'),
        ('body_repair', 'BODY REPAIR'),
        ('corrective_maintenance', 'CORRECTIVE MAINTENANCE'),
        ('breakdown_maintenance', 'BREAKDOWN MAINTENANCE')
    ], default="top_over_haul", string="Maintenance Type", tracking=True)
    # Helper field for unrelated tree view
    excavamini_detailed_maintenance_ids = fields.One2many(
        comodel_name='oa.detailed.maintenance',
        inverse_name='id',  # Dummy relation since no real link exists
        string='Detailed Maintenance',
        compute='_compute_excavamini_detailed_maintenance',
        store=False
    )

    @api.depends()
    def _compute_excavamini_detailed_maintenance(self):
        for record in self:
            # Ensure `record.equipment_id` exists to avoid errors
            if record.equipment_id:
                record.excavamini_detailed_maintenance_ids = self.env['oa.detailed.maintenance'].search([
                    ('maintenance_detail_id', '=', record.equipment_id.id)
                ])
            else:
                record.excavamini_detailed_maintenance_ids = self.env['oa.detailed.maintenance']
    @api.onchange('maintenance_schedule_conf')
    def _compute_btn_schedule_visibility(self):
        for record in self:
            record.schedule_set_btn = record.maintenance_schedule_conf
    @api.onchange('routine_schedule_conf')
    def _compute_btn_visibility(self):
        for record in self:
            record.btn_set_schedule = record.routine_schedule_conf


    def _compute_sequence(self):
        for index, record in enumerate(self, start=1):
            record.sequence = index

    def unlink(self):
        # Delete the record
        result = super(ExcavaMiniDailyReportDetailChecklist, self).unlink()

        # Recompute the sequence for remaining records
        self._compute_sequence()
        return result

    def write(self,vals):
        result = super(ExcavaMiniDailyReportDetailChecklist, self).write(vals)
        for record in self:
            if record.routine_schedule_conf:
                # Search for existing data in `oa.detailed.maintenance`
                existing_maintenance_perpart = self.env['oa.detailed.maintenance'].search([
                    ('maintenance_detail_id', '=', record.equipment_id.id),
                    ('part_name', '=', record.name.name)
                ])
                if existing_maintenance_perpart:
                    # Update existing record
                    existing_maintenance_perpart.write({
                        'maintenance_detail_id': record.equipment_id.id,
                        'maintenance_freq': record.maintenance_freq,
                        'part_name': record.name.name,
                        'unit_of_measure': record.measurement_unit,
                        'id_maintenance_type':record.excavamini_maintenance_type
                    })
                else:
                    # Create a new record
                    self.env['oa.detailed.maintenance'].create({
                        'maintenance_detail_id': record.equipment_id.id,
                        'maintenance_freq': record.maintenance_freq,
                        'part_name': record.name.name,
                        'unit_of_measure': record.measurement_unit,
                        'id_maintenance_type': record.excavamini_maintenance_type
                    })

            if record.maintenance_schedule_conf:
                existing_maintenance_schedule = self.env['oa.machine.maintenance'].search([
                    ('equip_id', '=', record.equipment_id.id),
                    ('task_planning_date', '=', record.maintenance_schedule_date),
                    ('maintenance_task_type', '=', record.excavamini_maintenance_type),
                    ('maintenance_part_name','=',record.name.name)
                ])
                if existing_maintenance_schedule:
                    print("Task Already Exist")
                else:
                    sub_group = None
                    self.env['oa.machine.maintenance'].generate_maintenance_task(
                        record.equipment_id,
                        record.asset_group.id,
                        sub_group,
                        record.maintenance_schedule_date,
                        record.excavamini_maintenance_type,
                        record.name.name,
                        "excavamini_checklist"
                    )

        return result


