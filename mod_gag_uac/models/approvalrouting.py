# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class ApprovalRoute(models.Model):
    _name = 'approval.route'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Approval Route Configuration'

    name = fields.Char('Route Name', required=True, tracking=True)
    step_ids = fields.One2many('approval.step', 'route_id', string='Approval Steps')
    model_name = fields.Char('Related Model', help='Define the model this approval route is used for.', tracking=True)

    @api.model
    def get_next_step(self, current_step):
        """ Get the next step in the approval process """
        steps = self.step_ids.sorted(key=lambda step: step.sequence)
        for step in steps:
            if step.sequence > current_step.sequence:
                return step
        return None

class ApprovalStep(models.Model):
    _name = 'approval.step'
    _description = 'Approval Step Configuration'

    name = fields.Char('Step Name', required=True)
    route_id = fields.Many2one('approval.route', string='Approval Route', required=True)
    user_id = fields.Many2one('res.users', string='Approver', required=True)
    sequence = fields.Integer('Step Sequence', help="Defines the order of the approval step.", default=10)
    required_approval = fields.Boolean('Requires Approval', default=True)