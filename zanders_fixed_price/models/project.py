# -*- coding: utf-8 -*-
# Copyright 2018 Magnus ((www.magnus.nl).)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from datetime import datetime


class Project(models.Model):
    _inherit = "project.project"

    state = fields.Selection(
        [('draft', 'Draft'),
        ('to_be_approved', 'To Be Approved'),
        ('approved', 'Approved')],
        string='Status',
        readonly=True,
        copy=False,
        store=True,
        default='draft'
    )
    rev_split_lines = fields.One2many(
        'revenue.split.line',
        'project_id',
        'Revenue Split lines'
    )

    @api.multi
    def submit(self):
        self.write({'state':'to_be_approved'})

    @api.multi
    def approved(self):
        self.write({'state': 'approved'})

    @api.multi
    def check_context(self):
        values = ['project_creation_in_progress', 'search_default_my_tasks', 'search_default_timebox_id', 'bin_size', 'group_by_no_leaf', 'search_default_project_id']
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
        [('ff', 'Fixed Fee'),
	    ('tm', 'Time and Material'),
	    ('ctm', 'Capped Time and Material')]
    )
    fixed_price_amount = fields.Float(
        string='Fixed Price Amount',
        digits=(16,2)
    )

    state = fields.Selection(
        [('draft', 'Draft'),
        ('to_be_approved', 'To Be Approved'),
        ('split_accepted', 'Split Accepted')],
        string='Status',
        readonly=True,
        copy=False,
        store=True,
        default='draft'
    )

    @api.multi
    def submit_task(self):
        self.write({'state': 'to_be_approved'})

    @api.multi
    def approve_task(self):
        self.write({'state': 'split_accepted'})

    @api.multi
    def name_get(self):
        result = []
        if 'search_default_my_tasks' in self.env.context or 'search_default_project_id' in self.env.context:
            result = super(Task, self).name_get()
        elif 'filter_on_task_user_dates' in self.env.context and 'sheet_week_from' in self.env.context and 'sheet_week_to' in self.env.context:
            date_from = datetime.strptime(self.env.context['sheet_week_from'], '%Y-%m-%d %H:%M:%S').date()
            date_to = datetime.strptime(self.env.context['sheet_week_to'], '%Y-%m-%d %H:%M:%S').date()
            task_ids = self.search([('project_id', '=', self.env.context['default_project_id'])])
            task_users = self.env['task.user'].search(
                [('task_id', 'in', task_ids.ids), ('start_date', '<=', date_from), ('end_date', '>=', date_to)])
            tasks = []
            for record in task_users:
                task = record.task_id
                if task.id not in tasks:
                    tasks.append(task.id)
                    name = task.name
                    if task.state == 'split_accepted':
                        result.append((task.id, name))
        else:
            for record in self:
                name = record.name
                if record.state == 'split_accepted':
                    result.append((record.id, name))
        return result

class TaskUser(models.Model):
    _inherit = 'task.user'

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

class RevenueSplitLine(models.Model):
    _name = 'revenue.split.line'

    project_id = fields.Many2one(
        'project.project',
    )
    user_id = fields.Many2one(
        'res.users',
        string='Consultants'
    )
    allocated_percentage = fields.Float(
        string='% Distribution Key',
        digits=(5, 2)
    )
