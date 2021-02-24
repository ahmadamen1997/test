# -*-coding: utf-8 -*-
{
    'name': "Stock card",

    'summary': "Add an report stock card in inventory",

    'description': """
        Print stock card.

        Print a stock card for a location wether it is for a internal,
        view, inventory, production or scrapped location. This module
        will give you the in, out and the balance of location between
        a period.
    """,

    'author': "Zero Systems",
    'website': "https://erpzero.com",
    'category': 'Warehouse',
    'version': '12.0.2',

    'depends': ['stock', 'web'],

    'data': [

        # reports
        'reports/stock_card_report.xml',
        'reports/stock_card_details_report.xml',

        # wizards
        'wizards/stock_card_wizard_views.xml'
    ],
    'demo': [],
    'installable': True,
    'images': ['static/images/main_screenshot.png']
}
