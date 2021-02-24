# -*- coding: utf-8 -*-
from odoo import http

# class SaleOrderLineReport(http.Controller):
#     @http.route('/sale_order_line_report/sale_order_line_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_line_report/sale_order_line_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_line_report.listing', {
#             'root': '/sale_order_line_report/sale_order_line_report',
#             'objects': http.request.env['sale_order_line_report.sale_order_line_report'].search([]),
#         })

#     @http.route('/sale_order_line_report/sale_order_line_report/objects/<model("sale_order_line_report.sale_order_line_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_line_report.object', {
#             'object': obj
#         })