# -*- coding: utf-8 -*-
{
    'name': "GM_customize",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Maged Ibrahem",
    'website': "maged@gmail.com",

    # Categories can be used to filter modules in modules listing
    'category': 'GM',
    'version': '11.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        'views/stock_view.xml',
        #'views/templates.xml',
         'report/barcode_reports.xml',
        'report/account_assets_templates.xml',       
    ],

}