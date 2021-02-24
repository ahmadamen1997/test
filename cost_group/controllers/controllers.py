# -*- coding: utf-8 -*-
from odoo import http

# class CostGroup(http.Controller):
#     @http.route('/cost_group/cost_group/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cost_group/cost_group/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cost_group.listing', {
#             'root': '/cost_group/cost_group',
#             'objects': http.request.env['cost_group.cost_group'].search([]),
#         })

#     @http.route('/cost_group/cost_group/objects/<model("cost_group.cost_group"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cost_group.object', {
#             'object': obj
#         })