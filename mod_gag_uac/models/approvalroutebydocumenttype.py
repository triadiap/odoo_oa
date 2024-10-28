# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class MappingApprovalFlowByDocumentType(models.Model):
    _name = 'oa.documenttype.approvalroute'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Approval Route Configuration Per Document Type Per Group'

    name = fields.Char('Route Name', required=True, tracking=True)
    group_id = fields.Many2one('res.groups', string="User Groups", tracking=True, required=True)
    document_type_id = fields.Many2one('oa.document.type', string="Document Name", tracking=True, required=True)
    step_ids = fields.One2many('oa.documenttype.approvalstep', 'oa_document_type_route_id', string='Approval Steps')

class MappingApprovalStepByDocumentType(models.Model):
    _name = 'oa.documenttype.approvalstep'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Approval Step Configuration Per Document Type Per Group'

    name = fields.Char('Step Name', required=True)
    oa_document_type_route_id = fields.Many2one('oa.documenttype.approvalroute', string='Approval Route', required=True)
    user_id = fields.Many2one('res.users', string='Approver', required=True)
    sequence = fields.Integer('Step Sequence', help="Defines the order of the approval step.", default=10)
    required_approval = fields.Boolean('Requires Approval', default=True)

