# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime, timedelta
from dateutil import relativedelta


class invoice_state_customize(models.Model):
    _inherit = 'res.country.state'

    due_date_period = fields.Integer('Due Date Period')


class InvoiceCustomize(models.Model):
    _inherit = 'account.invoice'

    printed = fields.Boolean('Printed', readonly=True, store=True)
    # user_id = fields.Many2one('res.users', string='Shipping Company', track_visibility='onchange',
    #                           readonly=True, states={'draft': [('readonly', False)]},
    #                           default=lambda self: self.env.user, copy=False)
    order_status = fields.Selection([
        ('new', 'New'),
        ('change', 'Change')
    ], default='new', string='Order Status')

    @api.onchange('order_status')
    def onch_order(self):
        if self.invoice_line_ids and self.order_status == 'change':
            for rec in self.invoice_line_ids:
                rec.write({'price_unit': 0.0})

    @api.constrains('partner_id')
    def due_date_state(self):
        if self.partner_id.state_id:
            self.payment_term_id = False
            self.date_due = datetime.now() + timedelta(days=self.partner_id.state_id.due_date_period)


class IrActionsReportx(models.Model):
    _inherit = 'ir.actions.report'

    @api.multi
    def render_qweb_pdf(self, res_ids=None, data=None):
        res = super(IrActionsReportx, self).render_qweb_pdf(res_ids, data)
        self.env['account.invoice'].search([('id', 'in', res_ids)]).write({'printed': True})
        return res

