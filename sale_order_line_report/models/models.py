# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InvoiceLineReport(models.Model):
    _inherit = "account.invoice.line"

    confirmed_date = fields.Datetime('Confirmed Date', store=True)
    state = fields.Many2one('res.country.state', store=True)
    category = fields.Many2one('product.category',store=True)
    variant = fields.Many2many('product.attribute.value', store=True)
    # delivered_quantity = fields.Integer('Delivered Quantity',  store=True)
    # delivered_quantity_price = fields.Float('Delivered Subtotal', store=True)
    # returned_quantity = fields.Integer('Returned Quantity', store=True)
    # returned_quantity_price = fields.Integer('Returned Quantity Price',store=True)
    delivered_quantity = fields.Integer('Delivered Quantity',compute='_compute_quantity')
    delivered_quantity_price = fields.Float('Delivered Subtotal',compute='_compute_quantity')
    returned_quantity = fields.Integer('Returned Quantity',compute='_compute_quantity')
    returned_quantity_price = fields.Integer('Returned Quantity Price',compute='_compute_quantity')
    # @api.depends('origin')
    # def get_conf_date(self):
    #     for rec in self.env['account.invoice.line'].search([('invoice_id.state','=','paid')]):
    #         sale_order = self.env['sale.order'].search([('name', '=', rec.origin)])
    #         returned_sale_order = self.env['stock.picking'].search([('sale_id', '=', sale_order.id),
    #                                                                ('origin', 'like', 'Return'),('picking_type_code','=','incoming')])
    #         if sale_order:
    #             rec.confirmed_date = sale_order.confirmation_date
    #             rec.state = sale_order.state_customer.id
    #             for record in returned_sale_order:
    #                 ret_list = []
    #
    #                 for ret in record.move_lines:
    #                     ret_list.append(ret.quantity_done)
    #                 rec.returned_quantity = sum(ret_list)
    #
    #             for line in sale_order.order_line:
    #                 rec.delivered_quantity = sum(line.search([('order_id.name', '=', rec.origin),('product_id','=',rec.product_id.id)]).mapped('qty_delivered'))
    #             rec.returned_quantity_price = rec.product_id.lst_price * rec.returned_quantity
    #             rec.delivered_quantity_price = rec.product_id.lst_price * rec.delivered_quantity

    @api.multi
    @api.depends('origin')
    def _compute_quantity(self):
        for rec in self:
            #for rec in data.env['account.invoice.line'].search([('invoice_id.state','=','paid'),('invoice_id.type','=','out_invoice')]):
            sale_order = self.env['sale.order'].search([('name', '=', rec.origin)])
            returned_sale_order = self.env['stock.picking'].search([('sale_id', '=', sale_order.id),
                                                                   ('origin', 'like', 'Return'),('picking_type_code','=','incoming')])
            if sale_order:
                rec.confirmed_date = sale_order.confirmation_date
                rec.state = sale_order.state_customer.id
                for record in returned_sale_order:
                    ret_list = []

                    for ret in record.move_lines:
                        if ret.product_id.id == rec.product_id.id:
                            ret_list.append(ret.quantity_done)
                    rec.returned_quantity = sum(ret_list)

                for line in sale_order.order_line:
                    rec.delivered_quantity = sum(line.search([('order_id.name', '=', rec.origin),('product_id','=',rec.product_id.id)]).mapped('qty_delivered'))
                rec.delivered_quantity_price = rec.price
                for refund in self.env['account.invoice.line'].search(
                        [('invoice_id.origin', '=', rec.invoice_id.number),('invoice_id.state', '=', 'paid'), ('invoice_id.type', '=', 'out_refund'),('product_id','=',rec.product_id.id)]):
                    rec.returned_quantity_price = refund.price



    @api.depends('product_id')
    def get_category(self):
        for rec in self:
            rec.category = rec.product_id.categ_id.id
            rec.variant = rec.product_id.attribute_value_ids.ids
