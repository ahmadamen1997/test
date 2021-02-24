# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class sale_customize(models.Model):
    _inherit = 'sale.order'

    sale_counter = fields.Integer(string="No. of Sale Orders",related='partner_id.sale_order_count', store=True, readonly=True)
    # city_customer = fields.Char(related='partner_id.city', store=True, readonly=True)
    state_customer = fields.Many2one(related='partner_id.state_id', store=True, readonly=True)
    team_id = fields.Many2one('crm.team', string='Shipping Company')

    # user_id = fields.Many2one('res.users', string='Shipping Company', index=True, track_visibility='onchange', default=lambda self: self.env.user)
    partner_id_mobile = fields.Char(related='partner_id.mobile')
    partner_id_mobile2 = fields.Char(related='partner_id.mobile2')
    waiting_list = fields.Boolean('Waiting List')
    order_status = fields.Selection([
        ('new', 'New'),
        ('change', 'Change')
        ],default='new', string='Order Status')
# class sale_report_customize(models.Model):
#     _inherit = 'sale.report'
#
#     user_id = fields.Many2one('res.users', 'Shipping Company', readonly=True)

    @api.onchange('order_status')
    def onch_order(self):
        if self.order_line and self.order_status == 'change':
            for rec in self.order_line:
                rec.write({'price_unit': 0.0})

    @api.multi
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        company_id = self.company_id.id
        journal_id = (self.env['account.invoice'].with_context(company_id=company_id or self.env.user.company_id.id)
            .default_get(['journal_id'])['journal_id'])
        if not journal_id:
            raise UserError(_('Please define an accounting sales journal for this company.'))
        invoice_vals = {
            'name': self.client_order_ref or '',
            'origin': self.name,
            'type': 'out_invoice',
            'account_id': self.partner_invoice_id.property_account_receivable_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'journal_id': journal_id,
            'currency_id': self.pricelist_id.currency_id.id,
            'comment': self.note,
            'payment_term_id': self.payment_term_id.id,
            'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
            'company_id': company_id,
            'user_id': self.user_id and self.user_id.id,
            'team_id': self.team_id.id,
            'discount_type':self.discount_type,
            'discount_rate':self.discount_rate,
            'order_status':self.order_status
        }
        return invoice_vals

    # @api.onchange('discount_type', 'discount_rate', 'order_line')
    # def set_lines_discount(self):
    #     if self.discount_type == 'percentage':
    #         for line in self.order_line:
    #             line.discount = self.discount_rate
    #     else:
    #         total = discount = 0.0
    #         for line in self.order_line:
    #             total += (line.product_uom_qty * line.price_unit)
    #         if self.discount_rate != 0:
    #             discount = (self.discount_rate / total) * 100
    #         else:
    #             discount = self.discount_rate
    #         for line in self.order_line:
    #             line.discount = discount
class sale_order_line_customize(models.Model):
    _inherit = 'sale.order.line'

    discount_amount = fields.Float(string=_('Discount amount'), default=0.0, digits=(10,2))
    discount = fields.Float(string=_('Discount (%)'), digits=(2,6), default=0.0)
    discount_show = fields.Float(string=_('Discount (%)'), digits=(2,2), default=0.0)
    disc_flag = fields.Boolean()

    @api.onchange('discount', 'product_uom_qty', 'price_unit')
    def _onchange_discount(self):
        if self.disc_flag == False:
            self.discount_amount = ((self.price_unit * self.product_uom_qty) / 100) * self.discount

        self.disc_flag = True

    @api.onchange('discount_amount')
    def _onchange_discount_amount(self):
        if ((self.price_unit * self.product_uom_qty) / 100) and self.disc_flag == False:
            self.discount = self.discount_amount / ((self.price_unit * self.product_uom_qty) / 100)
            self.discount_show = self.discount

        self.disc_flag = True
    # @api.depends('discount_value')
    # def discount_val(self):
    #
    #     self.discount = self.discount_value / self.price_subtotal

#
# class purchase_order_line_customize(models.Model):
#     _inherit = 'sale.order.line'
#
#     discount_amount = fields.Float(string=_('Discount amount'), default=0.0, digits=(10,2))
#     discount = fields.Float(string=_('Discount (%)'), digits=(2,6), default=0.0)
#     discount_show = fields.Float(string=_('Discount (%)'), digits=(2,2), default=0.0)
#     disc_flag = fields.Boolean()
#
#     @api.onchange('discount', 'product_uom_qty', 'price_unit')
#     def _onchange_discount(self):
#         if self.disc_flag == False:
#             self.discount_amount = ((self.price_unit * self.product_uom_qty) / 100) * self.discount
#
#         self.disc_flag = True
#
#     @api.onchange('discount_amount')
#     def _onchange_discount_amount(self):
#         if ((self.price_unit * self.product_uom_qty) / 100) and self.disc_flag == False:
#             self.discount = self.discount_amount / ((self.price_unit * self.product_uom_qty) / 100)
#             self.discount_show = self.discount
#
#         self.disc_flag = True
#
