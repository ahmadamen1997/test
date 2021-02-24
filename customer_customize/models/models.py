# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class customer_customize(models.Model):
    _inherit = 'res.partner'

    mobile2 = fields.Char('Mobile2')
    _sql_constraints = [('mobile', 'unique (mobile)', 'This mobile number is available for another customer')]
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', default=65)
    mobile = fields.Char('Mobile', required=True)
    mobile1_boolean = fields.Boolean('Length of mobile1')
    mobile2_boolean = fields.Boolean('Length of mobile2')

    @api.constrains('mobile')
    def mobile1_valid(self):
        if self.mobile:
            if len(self.mobile) != 11 or ' ' in self.mobile:
                self.mobile1_boolean = True
            else:
                self.mobile1_boolean = False

    @api.constrains('mobile2')
    def mobile_valid(self):
        if self.mobile2:
            if len(self.mobile2) != 11 or ' ' in self.mobile2:
                # raise ValidationError(_("Mobile2 Number should contain 11 numbers"))
                self.mobile2_boolean = True
            else:
                self.mobile2_boolean = False

