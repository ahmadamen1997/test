# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class stock_customize(models.Model):
    _inherit = 'stock.picking'

    qty_total = fields.Float('Total Product Quantity',compute='_onchan_mv_line')
    qty_done = fields.Float('Total Done Quantity',compute='_onchan_mv_line')
    shipping_company = fields.Many2one('crm.team', string='Shipping Company')
    mobile = fields.Char(related='partner_id.mobile')
    city = fields.Many2one('res.country.state',related='partner_id.state_id')
    address = fields.Char(related='partner_id.street')
    total_price = fields.Float(compute='_total_price')
    exported = fields.Boolean('Exported')
    exported_date = fields.Datetime('Exported Date')
    products_id = fields.Many2many('product.product',compute='product_stockx')
    returned = fields.Boolean('Returned',store=True, readonly=True)
    initial_demand = fields.Float('Total initial Demand',compute='_onchan_mv_line')
    def _onchan_mv_line(self):
        for record in self:
            qty_list = []
            initial_list = []
            for rec in record.move_lines:
                qty_list.append(rec.quantity_done)
                initial_list.append(rec.product_uom_qty)
            record.qty_done = sum(qty_list)
            record.qty_total = len(record.move_lines)
            record.initial_demand = sum(initial_list)

    @api.constrains('origin')
    def const_orig(self):
        if self.origin:

            if 'Return' in self.origin:
                self.returned = True
            if self.env['sale.order'].search([('name','=',self.origin)]):
                self.shipping_company = self.env['sale.order'].search([('name','=',self.origin)]).team_id.id
                self.note = self.env['sale.order'].search([('name','=',self.origin)]).note

    def _total_price(self):
        for rec in self:
            if rec.origin:
                rec.total_price = self.env['sale.order'].search([('name','=',rec.origin)]).amount_total


    @api.depends('move_lines')
    def product_stockx(self):
        for rec in self:
            pro = []
            if rec.origin:
                sale_order_lines = self.env['sale.order.line'].search([('order_id.name', '=', rec.origin)]).mapped('product_id')

                for recx in rec.move_lines:
                    pro.append(recx.product_id.id)
                if sale_order_lines:
                    for record in sale_order_lines:
                        if record.type == 'service':
                            if record.id not in pro:
                                pro.append(record.id)
                rec.products_id = pro
