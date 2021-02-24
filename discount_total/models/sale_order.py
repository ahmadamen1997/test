# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError

class purchase_order_line_customize(models.Model):
    _inherit = 'sale.order.line'

    discount_amount = fields.Float(string=_('Discount amount'), default=0.0, digits=(10,2))
    discount = fields.Float(string=_('Discount (%)'), digits=(2,6), default=0.0)
    discount_show = fields.Float(string=_('Discount (%)'), digits=(2,2), default=0.0)
    disc_flag = fields.Boolean()
    #
    # @api.one
    # @api.depends('product_uom_qty', 'price_unit')
    # def compute_line_price(self):
    #     self.price = self.product_uom_qty * self.price_unit
    #
    # price = fields.Float(string='Price', digits=(16, 2), store=True, compute='compute_line_price')

    @api.onchange('discount', 'product_uom_qty', 'price_unit')
    def _onchange_discount(self):
        if self.disc_flag == False:
            # print(self.price_subtotal)
            self.discount_amount = ((self.price_unit * self.product_uom_qty) / 100) * self.discount

        self.disc_flag = True

    @api.onchange('discount_amount')
    def _onchange_discount_amount(self):
        if ((self.price_unit * self.product_uom_qty) / 100) and self.disc_flag == False:
            self.discount = self.discount_amount / ((self.price_unit * self.product_uom_qty) / 100)
            self.discount_show = self.discount

        self.disc_flag = True

    @api.depends('product_uom_qty', 'price_unit', 'tax_id', 'discount')
    def _compute_amount(self):
        for line in self:
            # print(line.price_subtotal)
            taxes = line.tax_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': line.product_uom_qty * line.price_unit - (line.discount * (line.product_uom_qty * line.price_unit) / 100),
            })

class purchase_order_customize(models.Model):
    _inherit = 'sale.order'

    discount_type = fields.Selection([('percentage', 'Percentage'), ('amount', 'Amount')], string='Discount Type',
                                     readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, default='amount')
    discount_rate = fields.Float(string='Discount Rate', digits=(16, 2), store=True,
                                 readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, default=0.0)
    discount = fields.Monetary(string='Discount', digits=(16, 2), default=0.0,compute='_com_disc',
                               store=True, track_visibility='always')

    @api.depends('order_line.discount_amount')
    def _com_disc(self):
        total_disc = []
        for line in self.order_line:
            total_disc.append(line.discount_amount)
        self.discount = sum(total_disc)

    @api.onchange('discount_rate','discount_type')
    @api.constrains('discount_rate','discount_type')
    def onc_disc(self):
        total_list = []
        not_serv_list = []
        for rec in self.order_line:
            if rec.product_id.type != 'service':
                not_serv_list.append(rec)
        for rec in self.order_line:
            if rec.product_id.type != 'service':
                total_list.append(rec.discount_amount)
                if self.discount_rate > 0:
                    if self.discount_type == 'percentage':
                        rec.discount = self.discount_rate
                        rec.discount_amount = rec.discount * ((rec.price_unit * rec.product_uom_qty) / 100)

                    if self.discount_type == 'amount':
                        rec.discount_amount = self.discount_rate / len(not_serv_list)
                        if (rec.price_unit * rec.product_uom_qty) / 100:
                            rec.discount = rec.discount_amount / ((rec.price_unit * rec.product_uom_qty) / 100)

        # print('total_list',total_list)
        # self.discount = sum(total_list)

            # # print('disc',disc)
            # if recx.discount_type == 'amount':
            #     recx.update({
            #         'amount_total': (sum(total_list) + recx.amount_tax - recx.discount_rate)
            #     })
            #     recx.amount_total = (sum(total_list) + recx.amount_tax - recx.discount_rate)
            #     recx.discount = abs(recx.amount_total - recx.amount_untaxed + recx.amount_tax) + sum(disc)
            #
            # if recx.discount_type == 'percentage':
            #     recx.update({
            #         'amount_total': (sum(total_list) - (sum(total_list)*(recx.discount_rate/100))) + recx.amount_tax
            #     })
            #     recx.amount_total = (sum(total_list) - (sum(total_list)*(recx.discount_rate/100))) + recx.amount_tax
            #     recx.discount = abs(recx.amount_total - recx.amount_untaxed + recx.amount_tax ) + sum(disc)
