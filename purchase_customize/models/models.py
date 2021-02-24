# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError

class purchase_order_line_customize(models.Model):
    _inherit = 'purchase.order.line'

    discount_amount = fields.Float(string=_('Discount amount'), default=0.0, digits=(10,2))
    discount = fields.Float(string=_('Discount (%)'), digits=(2,6), default=0.0)
    discount_show = fields.Float(string=_('Discount (%)'), digits=(2,2), default=0.0)
    disc_flag = fields.Boolean()
    #
    # @api.one
    # @api.depends('product_qty', 'price_unit')
    # def compute_line_price(self):
    #     self.price = self.product_qty * self.price_unit
    #
    # price = fields.Float(string='Price', digits=(16, 2), store=True, compute='compute_line_price')

    @api.onchange('discount', 'product_qty', 'price_unit')
    def _onchange_discount(self):
        if self.disc_flag == False:
            # print(self.price_subtotal)
            self.discount_amount = ((self.price_unit * self.product_qty) / 100) * self.discount

        self.disc_flag = True

    @api.onchange('discount_amount')
    def _onchange_discount_amount(self):
        if ((self.price_unit * self.product_qty) / 100) and self.disc_flag == False:
            self.discount = self.discount_amount / ((self.price_unit * self.product_qty) / 100)
            self.discount_show = self.discount

        self.disc_flag = True

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'discount')
    def _compute_amount(self):
        for line in self:
            # print(line.price_subtotal)
            taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': line.product_qty * line.price_unit - (line.discount * (line.product_qty * line.price_unit) / 100),
            })

class purchase_order_customize(models.Model):
    _inherit = 'purchase.order'

    discount_type = fields.Selection([('percentage', 'Percentage'), ('amount', 'Amount')], string='Discount Type',
                                     readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, default='amount')
    discount_rate = fields.Float(string='Discount Rate', digits=(16, 2), store=True,
                                 readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, default=0.0)

    @api.onchange('discount_rate','discount_type')
    @api.constrains('discount_rate','discount_type')
    def _onchage_disc(self):
        total_list = []
        for rec in self.order_line:
            total_list.append(rec.price_subtotal)

        if self.discount_type == 'amount':
            self.update({
                'amount_total': (sum(total_list) - self.discount_rate)
            })
            self.amount_total = (sum(total_list) - self.discount_rate)

        if self.discount_type == 'percentage':
            self.update({
                'amount_total': (sum(total_list) - (sum(total_list)*(self.discount_rate/100)))
            })
            self.amount_total = (sum(total_list) - (sum(total_list)*(self.discount_rate/100)))