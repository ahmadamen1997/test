# -*- coding: utf-8 -*-
from odoo import http

# class InvoiceCustomize(http.Controller):
#     @http.route('/invoice_customize/invoice_customize/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_customize/invoice_customize/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_customize.listing', {
#             'root': '/invoice_customize/invoice_customize',
#             'objects': http.request.env['invoice_customize.invoice_customize'].search([]),
#         })

#     @http.route('/invoice_customize/invoice_customize/objects/<model("invoice_customize.invoice_customize"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_customize.object', {
#             'object': obj
#         })