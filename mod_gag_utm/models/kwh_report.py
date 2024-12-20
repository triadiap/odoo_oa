# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError

class NewDailyKWH(models.Model):
    _name = "daily.kwh"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Daily KWH Consumption Report"

    audit_id = fields.Char(string="Inspection ID", readonly=True, copy=False, default='New')
    equipment_id = fields.Many2one('oa.master.equipment', string="Nama Mesin", required=True, tracking=True)
    checking_date = fields.Date('Tanggal Pelaporan', tracking=True, required=True)
    shift = fields.Selection([
        ('1', 'Shift 1'),
        ('2', 'Shift 2'),
        ('3', 'Shift 3')
    ], string="Shift", required=True, default='1', tracking=True)
    serial_number = fields.Char(string="Nomor Seri")
    equipment_type = fields.Char(string="Model")
    manuf_year = fields.Char(string="Tahun Pembuatan")
    id_ceklist = fields.One2many('oa.hourly.kwh', 'checklist_id', string="Lines")
    total_quantity_display = fields.Char(string="Total Quantity", compute='_compute_total_quantity_display')
    equipment_capacity = fields.Float(string="Ampere (A)")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approval_process', 'Approval Process'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancelled')
    ], default="draft", string="Status", tracking=True)
    latest_approval_commentary = fields.Text(string="Notes", tracking=True)
    jml_kwh_pershift = fields.Float(string="Total KWH Per Hours", compute='_compute_jml_kwh_per_shift', store=True)
    jml_kwh = fields.Float(string="Total KWH", compute='_compute_jml_kwh', store=True)

    # ------------------Ini Connect ke Module UAC ------------------------------------------#
    approval_route_id = fields.Many2one('approval.route', string='Approval Route', readonly=True)
    current_step_id = fields.Many2one('approval.step', string='Current Step', readonly=True)
    existing_status = fields.Char(string="Current Status", readonly=True, tracking=True)
    upcoming_status = fields.Many2one('approval.step', string='Upcoming Status', readonly=True, tracking=True)
    pending_approval_by = fields.Many2one('res.users', string="Pending Approval By", readonly=True, tracking=True)
    button_visible = fields.Boolean(compute='_compute_button_visibility', store=False)

    # -------------------------------------------------------------------------------------#

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.audit_id}"
            result.append((record.id, name))  # or any other meaningful field
            self._compute_jml_kwh_per_shift()
            self._compute_jml_kwh()
        return result


    def _compute_jml_kwh_per_shift(self):
        for rec in self:
            jml_kwh_pershift = self.env['oa.hourly.kwh'].search([('checklist_id','=',rec.id)]).mapped('jml_kwh_per_jam')
            rec.jml_kwh_pershift = float(sum(jml_kwh_pershift))


    def _compute_jml_kwh(self):
        for rec in self:
            jml_kwh = self.env['oa.hourly.kwh'].search([('checklist_id','=',rec.id)]).mapped('kwh_input')
            rec.jml_kwh = float(sum(jml_kwh))

    def action_open_budgets(self):
         print("Test")
    def action_done(self):
        self.state = 'done'
        self._compute_jml_kwh_per_shift()
        self._compute_jml_kwh()

    def action_draft(self):
        self.state = 'draft'
        self._compute_jml_kwh_per_shift()
        self._compute_jml_kwh()

    def action_cancel(self):
        self.state = 'cancel'
        self._compute_jml_kwh_per_shift()
        self._compute_jml_kwh()
    def action_approval_process(self):
        # UAC Configuration to raise document status as submitted for approval
        if not self.approval_route_id:
            raise ValidationError('Approval route is not defined.')
        next_step = self.approval_route_id.step_ids.sorted(key='sequence')[0]
        self.current_step_id = next_step
        self.state = 'approval_process'
        self.existing_status = 'Document submitted for approval'
        self.pending_approval_by = next_step.user_id
        self.upcoming_status = next_step
        self.message_post(body='Document submitted for approval.')
        self._compute_jml_kwh_per_shift()
        self._compute_jml_kwh()

    def _compute_button_visibility(self):
        for record in self:
                # Ensure pending_approval_by is a valid user and assign True/False
            if record.pending_approval_by:
                record.button_visible = (record.pending_approval_by.id == self.env.user.id)
            else:
                record.button_visible = False
        # -----------------------------------------------------------------------
        self._compute_jml_kwh_per_shift()
        self._compute_jml_kwh()

    def _compute_total_quantity_display(self):
        for record in self:
            total_jml_kwh = sum(line.jml_kwh for line in record.id_ceklist)
            record.total_quantity_display = f"Total % KWH: {(total_jml_kwh * 100) : .2f} %"

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id:
            self.serial_number = self.equipment_id.serial_number
            self.equipment_type = self.equipment_id.equipment_model
            self.manuf_year = self.equipment_id.manuf_year
            self.equipment_capacity = float(self.equipment_id.equipment_capacity)
        else:
            self.serial_number = False
            self.equipment_type = False
            self.manuf_year = False
            self.equipment_capacity = False

    def open_line_form(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add New',
            'res_model': 'oa.hourly.kwh',
            'view_mode': 'form',
            'view_id': self.env.ref('mod_gag_utm.view_from_hourly_kwh_input').id,
            'target': 'new',
            'context': {
                'default_checklist_id': self.id,  # Automatically link the line to the current model
            },
        }
    @api.model
    def create(self,vals):
        if vals.get('audit_id', 'New') == 'New':
            # Generate the sequence number
            sequence = self.env['ir.sequence'].next_by_code('daily.kwh') or '00000'
            # Combine them into the final name
            vals['audit_id'] = f'IR-{sequence}'

            # UAC Find the configured approval route for the current model for new document creation
        config = self.env['oa.document.workflow.config'].search([('model_id.model', '=', self._name)], limit=1)
        if config:
                vals['approval_route_id'] = config.approval_route_id.id
        if vals.get('audit_id'):
            equip_id = self.env['oa.master.equipment'].browse(vals['equipment_id'])
            vals.update({
                'serial_number': equip_id.serial_number,
                'equipment_type': equip_id.equipment_model,
                'manuf_year': equip_id.manuf_year,
                'equipment_capacity': equip_id.equipment_capacity
            })
        else:
            vals.update({
                'serial_number': None,
                'equipment_type': None,
                'manuf_year': None,
                'equipment_capacity': None
            })

        self._compute_jml_kwh_per_shift()
        self._compute_jml_kwh()

        return super(NewDailyKWH, self).create(vals)

    def write(self,vals):
        for record in self:
            if 'equipment_id' in vals or record.equipment_id:
                equip_id = record.equipment_id if 'equipment_id' not in vals else self.env['oa.master.equipment'].browse(
                    vals['equipment_id'])
                vals.update({
                    'serial_number': equip_id.serial_number,
                    'equipment_type': equip_id.equipment_model,
                    'manuf_year': equip_id.manuf_year,
                    'equipment_capacity': equip_id.equipment_capacity
                })
        return super(NewDailyKWH, self).write(vals)



class NewDetailKwhChecklist(models.Model):
    _name = "oa.hourly.kwh"
    _Description = "Detail KWH checklist perday perhour"

    operational_time = fields.Float(string="Time", help="Time in hours and minutes format.")
    volt_r_n = fields.Integer(string="R-N", required=True, tracking=True)
    volt_s_n = fields.Integer(string="S-N", required=True, tracking=True)
    volt_t_n = fields.Integer(string="T-N", required=True, tracking=True)
    arus_r = fields.Integer(string="R", required=True, tracking=True)
    arus_s = fields.Integer(string="S", required=True, tracking=True)
    arus_t = fields.Integer(string="T", required=True, tracking=True)
    freq_hz = fields.Float(string="Freq (Hz)",required=True, tracking=True)
    oil_pressure = fields.Float(string="Oil Pressure", required=True, tracking=True)
    water_temperature = fields.Float(string="Water Temperature", required=True, tracking=True)
    battery = fields.Float(string="Battery", required=True, tracking=True)
    kw_l1 = fields.Float(string="L1", compute='_compute_r_n_dikali_r', tracking=True,store=True)
    kw_l2 = fields.Float(string="L2", compute='_compute_s_n_dikali_s', tracking=True,store=True)
    kw_l3 = fields.Float(string="L3", compute='_compute_t_n_dikali_t', tracking=True,store=True)
    jml_kw = fields.Float(string="Jml Kw", compute='_compute_total_kw_li_l2_l3',tracking=True,store=True)
    jml_daya = fields.Float(string="Jml Daya %", compute='_compute_jml_kw_dibagi_capacity_dikali_100', tracking=True,store=True)
    jml_kwh_per_jam = fields.Float(string="Jml Kwh/Jam")
    checklist_id = fields.Many2one('daily.kwh', string='Hourly Checklist')
    kwh_input = fields.Float(string="KWH")

    @api.depends('volt_r_n', 'arus_r')
    def _compute_r_n_dikali_r(self):
        for rec in self:
            rec.kw_l1 = float(rec.volt_r_n * rec.arus_r * 0.0009)

    @api.depends('volt_s_n', 'arus_s')
    def _compute_s_n_dikali_s(self):
        for rec in self:
            rec.kw_l2 = float(rec.volt_s_n * rec.arus_s * 0.0009)

    @api.depends('volt_t_n', 'arus_t')
    def _compute_t_n_dikali_t(self):
        for rec in self:
            rec.kw_l3 = float(rec.volt_t_n * rec.arus_t * 0.0009)

    @api.depends('kw_l1', 'kw_l3','kw_l2')
    def _compute_total_kw_li_l2_l3(self):
        for rec in self:
           rec.jml_kw = float(rec.kw_l1 + rec.kw_l2 + rec.kw_l3)
           rec.jml_kwh_per_jam = float(rec.kw_l1 + rec.kw_l2 + rec.kw_l3)

    @api.depends('jml_kw', 'checklist_id.equipment_capacity')
    def _compute_jml_kw_dibagi_capacity_dikali_100(self):
        for rec in self:
            if rec.checklist_id and rec.checklist_id.equipment_capacity:
                try:
                    # Convert equipment_capacity from char to float
                    equipment_capacity_float = float(rec.checklist_id.equipment_capacity)
                    rec.jml_daya = float(rec.jml_kw / equipment_capacity_float * 100)
                except ValueError:
                    # If conversion fails, set the result to 0.0
                    rec.jml_daya = 0.0
            else:
                rec.jml_daya = 0.0  # Default to 0 if no capacity is provided

    @api.onchange('operational_time')
    def _onchange_time_field(self):
        if self.operational_time:
            hours = int(self.operational_time)
            minutes = int((self.operational_time - hours) * 60)
            self.operational_time = hours + (minutes / 60.0)
    #
    # @api.onchange('kwh_3')
    # def CalculatePercentageOfKwh(self):
    #     if self.kwh_3:
    #         self.jml_kwh = self.kwh_3 / 100
    #     else:
    #         self.jml_kwh = False

class ChartElectricityConsumptionPerYearPerUnit(models.Model):
    _name = "oa.yearly.electricity"
    _Description = "Electricity Output Per Year Per Diesel Unit"
    _auto = False

    id = fields.Char('ID', readonly=True)
    month_number = fields.Char(string="Month Number")
    month_name = fields.Char(string="Month Name")
    checkingyear = fields.Integer(string="Year")
    equipment_id = fields.Char(string="Equipment ID")
    equipment_name = fields.Char(string="Equipment Name")
    kwh_pershift = fields.Float(string="Kwh/Hour")
    jml_kwh =  fields.Float(string="KWH")

    def init(self):
        tools.drop_view_if_exists(self._cr, 'oa_yearly_electricity')
        self._cr.execute("""
                   CREATE OR REPLACE VIEW oa_yearly_electricity AS(
                        SELECT
                              row_number() OVER () AS id,
                               b.audit_id AS audit_id,
                               b.checking_date AS checking_date,
                               m.month_number,
                               m.month_name,
                               COALESCE(b.checkingyear,EXTRACT(YEAR FROM NOW())) AS checkingyear,
                               b.equipmentid AS equipment_id,
                               COALESCE(b.equipment_name,'Others') AS equipment_name,
                               COALESCE(b.kwh_pershift,0) AS kwh_pershift,
                               COALESCE(b.jmlkwh,0) AS jml_kwh
                              
                        FROM
                            (SELECT
                                 1 AS month_number, '01-Jan' AS month_name
                                 UNION ALL SELECT 2, '02-Feb'
                                 UNION ALL SELECT 3, '03-Mar'
                                 UNION ALL SELECT 4, '04-Apr'
                                 UNION ALL SELECT 5, '05-May'
                                 UNION ALL SELECT 6, '06-Jun'
                                 UNION ALL SELECT 7, '07-Jul'
                                 UNION ALL SELECT 8, '08-Aug'
                                 UNION ALL SELECT 9, '09-Sep'
                                 UNION ALL SELECT 10, '10-Oct'
                                 UNION ALL SELECT 11, '11-Nov'
                                 UNION ALL SELECT 12, '12-Dec') AS m
                        LEFT JOIN(
                                SELECT
                                    b.audit_id AS audit_id,
                                    b.checking_date AS checking_date,
                                    EXTRACT(MONTH FROM b.checking_date) AS month_number,
                                    EXTRACT(YEAR FROM b.checking_date) AS checkingyear,
                                    b.equipment_id as equipmentid,
                                    CONCAT(c.name,'-',c.serial_number) AS equipment_name,
                                    SUM(b.jml_kwh_pershift) AS kwh_pershift,
                                    SUM(b.jml_kwh) AS jmlkwh
                                FROM
                                    daily_kwh b
                                JOIN 
                                    oa_master_equipment c ON b.equipment_id = c.id
                                GROUP BY EXTRACT(MONTH FROM b.checking_date),EXTRACT(YEAR FROM b.checking_date),b.equipment_id,CONCAT(c.name,'-',c.serial_number),b.audit_id,b.checking_date
                                )b ON m.month_number = b.month_number
                        ORDER BY m.month_number, COALESCE(b.checkingyear,EXTRACT(YEAR FROM NOW()))
                       )
               """)





