# -*- coding: utf-8 -*-
{
    'name': "Sale Order line Report",

    'summary': """
        Sale order Line report""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Eslam Tharwat",
    'website': "eslam.tharwaat@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','sale_customize'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'data/data.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}