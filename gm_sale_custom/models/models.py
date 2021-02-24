# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class GMSaleCustom(models.Model):
    _inherit = 'res.partner'

    mobile = fields.Char(string='Mobile1', size=11, required=True)
    mobile2 = fields.Char(string='Mobile2', size=11, required=True)

    _sql_constraints = [
        ("unique_mobile", "UNIQUE (mobile)", _("عفوا لايمكن تكرار رقم الموبيل")),
        ("unique_mobile2", "UNIQUE (mobile2)", _("عفوا لايمكن تكرار رقم الموبيل"))
    ]

    @api.constrains('mobile', 'mobile2')
    def check_phone(self):
        if len(self.mobile) != 11 or not self.mobile.isdigit() or len(self.mobile2) != 11 or not self.mobile2.isdigit():
            raise ValidationError(_("عفوا رقم الموبيل يجب ان يكون 11 رقم"))
        all_mobiles = self.env['res.partner'].search([('id', '!=', self.id)]).mapped('mobile')
        all_mobiles2 = self.env['res.partner'].search([('id', '!=', self.id)]).mapped('mobile2')
        if self.mobile in all_mobiles:
            raise ValidationError(_("عفوا لايمكن تكرار رقم الموبيل"))
        if self.mobile2 in all_mobiles2:
            raise ValidationError(_("عفوا لايمكن تكرار رقم الموبيل"))


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    user_id = fields.Many2one('res.users', string='Payment Method', index=True, track_visibility='onchange',
                              default=lambda self: self.env.user)

    number_of_orders = fields.Integer(string='Number Of Orders', compute='calc_orders')

    @api.multi
    @api.depends('partner_id')
    @api.onchange('partner_id')
    def calc_orders(self):
        for rec in self:
            if rec.partner_id:
                self._cr.execute(
                    """
                    select count(*) as the_count from sale_order where partner_id = %s
                    """ % rec.partner_id.id
                )
                res = self._cr.fetchall()
                if res:
                    rec.number_of_orders = res[0][0]


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    notes_client = fields.Text(string='NOTES')
