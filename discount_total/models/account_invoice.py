from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # @api.one
    # @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
    #              'currency_id', 'company_id', 'date_invoice', 'type')
    # def compute_discount(self):
    #     round_curr = self.currency_id.round
    #     self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
    #     self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
    #     self.amount_total = self.amount_untaxed + self.amount_tax
    #     discount = 0
    #     for line in self.invoice_line_ids:
    #         discount += (line.price_unit * line.quantity * line.discount) / 100
    #     self.discount = discount
    #     amount_total_company_signed = self.amount_total
    #     amount_untaxed_signed = self.amount_untaxed
    #     if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
    #         currency_id = self.currency_id.with_context(date=self.date_invoice)
    #         amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
    #         amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
    #     sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
    #     self.amount_total_company_signed = amount_total_company_signed * sign
    #     self.amount_total_signed = self.amount_total * sign
    #     self.amount_untaxed_signed = amount_untaxed_signed * sign
    #
    # @api.one
    # @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
    #              'currency_id', 'company_id', 'date_invoice', 'type')
    # def _compute_amount(self):
    #     round_curr = self.currency_id.round
    #     self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
    #     self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
    #     self.amount_total = self.total_before_discount + self.amount_tax - self.discount
    #     amount_total_company_signed = self.amount_total
    #     amount_untaxed_signed = self.amount_untaxed
    #     if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
    #         currency_id = self.currency_id.with_context(date=self.date_invoice)
    #         amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
    #         amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
    #     sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
    #     self.amount_total_company_signed = amount_total_company_signed * sign
    #     self.amount_total_signed = self.amount_total * sign
    #     self.amount_untaxed_signed = amount_untaxed_signed * sign
    #


    @api.one
    @api.depends('invoice_line_ids')
    def compute_total_before_discount(self):
        total = 0
        for line in self.invoice_line_ids:
            total += line.price
        self.total_before_discount = total

    discount_type = fields.Selection([('percentage', 'Percentage'), ('amount', 'Amount')], string='Discount Type',
                                     readonly=True, states={'draft': [('readonly', False)]}, default=False)
    discount_rate = fields.Float(string='Discount Rate', digits=(16, 2),
                                 readonly=True, states={'draft': [('readonly', False)]}, default=0.0)
    discount = fields.Monetary(string='Discount', digits=(16, 2), default=0.0,
                               store=True, compute='set_lines_discount', track_visibility='always')
    total_before_discount = fields.Monetary(string='Total Before Discount', digits=(16, 2), store=True, compute='compute_total_before_discount')
    amount_total = fields.Monetary(string='Total',
                                   store=True, readonly=True, compute='_compute_amount')


        # if self.discount_type == 'percentage':
        #
        #     for line in self.invoice_line_ids:
        #         print('line',line)
        #         line.discount = self.discount_rate
        # else:
        #     total = []
        #     for line in self.invoice_line_ids:
        #         total.append(line.quantity * line.price_unit)
        #     print('total',total)
        #     if self.discount_rate != 0 and total:
        #         discount = (self.discount_rate / sum(total)) * 100
        #     else:
        #         discount = self.discount_rate
        #     for line in self.invoice_line_ids:
        #         line.discount = discount

    @api.depends('invoice_line_ids.discount_amount')
    def set_lines_discount(self):
        discount_list = []
        for rec in self.invoice_line_ids:
            discount_list.append(rec.discount_amount)
        self.discount = sum(discount_list)


    @api.onchange('discount_rate','discount_type')
    def onch_disc(self):
        not_serv_list = []
        for line in self.invoice_line_ids:
            if line.product_id.type != "service":
                not_serv_list.append(line)
        for line in self.invoice_line_ids:
            if line.product_id.type != "service":
                if self.discount_rate>0:
                    if self.discount_type == 'percentage':
                        line.discount = self.discount_rate
                        line.discount_amount = line.discount * ((line.price_unit * line.quantity) / 100)

                    if self.discount_type == 'amount':
                        line.discount_amount = self.discount_rate / len(not_serv_list)
                        if (line.price_unit * line.quantity) / 100:
                            line.discount = line.discount_amount / ((line.price_unit * line.quantity) / 100)


    @api.model
    def create(self, vals):
        res  = super(AccountInvoice, self).create(vals)
        not_serv_list = []
        for line in res.invoice_line_ids:
            if line.product_id.type != "service":
                not_serv_list.append(line)

        for line in res.invoice_line_ids:
            if line.product_id.type != "service":
                if res.discount_rate > 0:
                    if res.discount_type == 'percentage':
                        line.discount = res.discount_rate
                        line.discount_amount = line.discount * ((line.price_unit * line.quantity) / 100)

                    if res.discount_type == 'amount':
                        line.discount_amount = res.discount_rate / len(not_serv_list)
                        if (line.price_unit * line.quantity) / 100:
                            line.discount = line.discount_amount / ((line.price_unit * line.quantity) / 100)
        return res

    @api.constrains('invoice_line_ids')
    def const_invoice_id(self):
        not_serv_list = []
        for line in self.invoice_line_ids:
            if line.product_id.type != "service":
                not_serv_list.append(line)

        if self.discount_rate>0:
            for line in self.invoice_line_ids:
                if line.product_id.type != "service":
                    if self.discount_type == 'percentage':
                        line.discount = self.discount_rate
                        line.discount_amount = line.discount * ((line.price_unit * line.quantity) / 100)

                    if self.discount_type == 'amount':
                        line.discount_amount = self.discount_rate / len(not_serv_list)
                        if (line.price_unit * line.quantity) / 100:
                            line.discount = line.discount_amount / ((line.price_unit * line.quantity) / 100)



class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    discount = fields.Float(string='Discount (%)', digits=(2,6))
    discount_amount = fields.Float(string='Discount amount', default=0.0,digits=(2,6))

    price = fields.Float(string='Price', digits=(16, 2), store=True,compute='compute_line_price')

    @api.constrains('discount', 'quantity', 'price_unit')
    # @api.onchange('discount', 'quantity', 'price_unit')
    def _onchange_discount(self):
        if self.price_unit * self.quantity != 0:
            self.discount_amount = self.discount * ((self.price_unit * self.quantity) / 100)

    @api.onchange('discount_amount', 'quantity', 'price_unit')
    def _onchange_discount_amount(self):
        if self.price_unit * self.quantity != 0:
            self.discount = self.discount_amount / ((self.price_unit * self.quantity) / 100)

    @api.one
    @api.depends('price_unit','quantity')
    def compute_line_price(self):
        self.price = self.quantity * self.price_unit



