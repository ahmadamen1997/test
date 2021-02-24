# -*- coding: utf-8 -*-
from odoo import http

# class CustomerCustomize(http.Controller):
#     @http.route('/customer_customize/customer_customize/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_customize/customer_customize/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_customize.listing', {
#             'root': '/customer_customize/customer_customize',
#             'objects': http.request.env['customer_customize.customer_customize'].search([]),
#         })

#     @http.route('/customer_customize/customer_customize/objects/<model("customer_customize.customer_customize"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_customize.object', {
#             'object': obj
#         })