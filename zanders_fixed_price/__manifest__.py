# -*- coding: utf-8 -*-
# Copyright 2019 Willem Hulshof Magnus (www.magnus.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "zanders_fixed_price",

    'summary': """
        This module extends the magnus_invoicing module by adding fields to 
        task.user  """,

    'description': """
        This module extends the magnus_invoicing module by adding fields to 
        task.user for start-/end-dates per consultant and % revenue allocated for
        fixed price tasks. 
    """,

    'author': "Magnus",
    'website': "http://www.magnus.nl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'module_category_specific_industry_applications',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['magnus_invoicing'
                ],

    # always loaded
    'data': [
        'security/zander_security.xml',
        'views/task_view.xml',
        'views/hr_timesheet_assets.xml',
        'views/project_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}