odoo.define('zanders_fixed_price.sheet', function (require) {
    'use strict';

    var core = require('web.core');
    var Model = require('web.DataModel');
    var form_common = require('web.form_common');
    var QWeb = core.qweb;
    var hr_timesheet_task = require('hr_timesheet_task.sheet');

    core.form_custom_registry.get('weekly_timesheet').include({

        onchange_project_id: function() {
            var self = this;
            var project_id = self.project_m2o.get_value();
            self.task_m2o.node.attrs.domain = [
                // show only tasks linked to the selected project
                ['project_id','=',project_id],
                // ignore tasks already in the timesheet
                ['id', 'not in', _.pluck(self.projects, 'task')],
            ];

            self.task_m2o.set_value(false);
            var Tasks = new Model('project.task');
            Tasks.query(['id']).filter([["project_id", "=", project_id], ["standard", "=", "True"]]).limit(1).all().then(function (standard_task){
                if (standard_task.length === 1) {
                    self.task_m2o.set_value(standard_task[0].id);
                }
            });
            Tasks.query(['id', 'name']).filter([["project_id", "=", project_id]]).all().then(function (task){
                if (task.length === 1) {
                    self.task_m2o.set_value(task[0].id);
                }
            });

            self.task_m2o.node.attrs.context = {'default_project_id': project_id, 'filter_on_task_user_dates':true, 'sheet_week_from':this.get('date_from'), 'sheet_week_to':this.get('date_to')};
            self.task_m2o.render_value();
        },

    });
});