# -*- coding: utf-8 -*-
from odoo import http

# class GmSaleCustom(http.Controller):
#     @http.route('/gm_sale_custom/gm_sale_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gm_sale_custom/gm_sale_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gm_sale_custom.listing', {
#             'root': '/gm_sale_custom/gm_sale_custom',
#             'objects': http.request.env['gm_sale_custom.gm_sale_custom'].search([]),
#         })

#     @http.route('/gm_sale_custom/gm_sale_custom/objects/<model("gm_sale_custom.gm_sale_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gm_sale_custom.object', {
#             'object': obj
#         })