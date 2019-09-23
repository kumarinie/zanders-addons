# -*- coding: utf-8 -*-
# Copyright 2018 Magnus ((www.magnus.nl).)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class Project(models.Model):
    _inherit = "project.project"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_be_approved', 'To Be Approved'),
        ('approved', 'Approved'),
    ], string='Status', readonly=True, copy=False, store=True, default='draft')

#     invoice_principle = fields.Selection([
#             ('ff','Fixed Fee'),
#             ('tm','Time and Material'),
#             ('ctm', 'Capped Time and Material')
#         ],)
#     invoice_schedule_ids = fields.One2many(
#         'invoice.schedule.lines',
#         'project_id',
#         string='Invoice Schedule')

    @api.multi
    def submit(self):
        self.write({'state':'to_be_approved'})

    @api.multi
    def approved(self):
        self.write({'state': 'approved'})

    @api.multi
    def check_context(self):
        values = ['project_creation_in_progress', 'search_default_my_tasks', 'search_default_timebox_id', 'bin_size', 'group_by_no_leaf']
        for val in values:
            if val in self.env.context:
                return True
        return False

    @api.multi
    def name_get(self):
        result = []
        if self.check_context():
            result = super(Project, self).name_get()
        else:
            for record in self:
                name = record.name
                if record.state == 'approved':
                    result.append((record.id, name))
        return result

class Task(models.Model):
    _inherit = "project.task"

    invoice_principle = fields.Selection(
        [
	    ('ff', 'Fixed Fee'),
	    ('tm', 'Time and Material'),
	    ('ctm', 'Capped Time and Material')
        ]
    )
    fixed_price_amount = fields.Float(
        string='Fixed Price Amount',
        digits=(16,2)
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_be_approved', 'To Be Approved'),
        ('split_accepted', 'Split Accepted'),
    ], string='Status', readonly=True, copy=False, store=True, default='draft')

    @api.multi
    def submit(self):
        self.write({'state': 'to_be_approved'})

    @api.multi
    def approved(self):
        self.write({'state': 'split_accepted'})

    @api.multi
    def name_get(self):
        result = []
        if 'search_default_my_tasks' in self.env.context or 'search_default_project_id' in self.env.context:
            result = super(Task, self).name_get()
        else:
            for record in self:
                name = record.name
                if record.state == 'split_accepted':
                    result.append((record.id, name))
        return result

class TaskUser(models.Model):
    _inherit = 'task.user'

    # @api.one
    # @api.depends('product_id')
    # def _default_fee_rate(self):
    #     if self.product_id:
    #         self.fee_rate = self.product_id.list_price
    #
    # @api.model
    # def _default_product(self):
    #     if self.user_id.employee_ids.product_id:
    #         return self.user_id.employee_ids.product_id.id
    #
    # @api.model
    # def _get_category_domain(self):
    #     return [('categ_id','=', self.env.ref(
    #         'magnus_timesheet.product_category_fee_rate').id)]

    # task_id = fields.Many2one(
    #     'project.task',
    #     string='Task'
    # )
    # user_id = fields.Many2one(
    #     'res.users',
    #     string='Consultants'
    # )
    # product_id = fields.Many2one(
    #     'product.product',
    #     string='Fee rate Product',
    #     default=_default_product,
    #     domain=_get_category_domain
    # )
    # fee_rate = fields.Float(
    #     default=_default_fee_rate,
    #     string='Fee Rate',
    # )
    start_date = fields.Date(
	    'Start Date'
    )
    end_date = fields.Date(
        'End Date'
    )
    allocated_percentage = fields.Float(
        string='% Distribution Key',
        digits=(5,2)
    )

    # @api.onchange('user_id')
    # def onchange_user_id(self):
    #     self.product_id = False
    #     self.fee_rate = 0
    #     if self.user_id:
    #         emp = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)])
    #         if emp:
    #             product = emp.product_id
    #             self.product_id = product.id
    #             self.fee_rate = product.lst_price

# class InvoiceScheduleLine(models.Model):
#     _name = 'invoice.schedule.lines'
#
#     project_id = fields.Many2one(
#         'project.project',
#     )
#
# class ProjectInvoicingProperties(models.Model):
#     _inherit = "project.invoicing.properties"
#
#     group_invoice = fields.Boolean('Group Invoice')
