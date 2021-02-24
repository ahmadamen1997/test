# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import Warning
import datetime
from datetime import datetime
import pytz

FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
ERREUR_FUSEAU = _("Set your timezone in preferences")


class StockCardWizard(models.TransientModel):
    u"""."""

    _name = "wizard.stock_card_wizard"

    details = fields.Boolean(
        string="Detailed report",
        default=False)

    date_start = fields.Datetime(
        string="Start date",
        required=True)

    date_end = fields.Datetime(
        string="End date",
        required=True)

    location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
        required=True)

    @api.model
    def convert_UTC_TZ(self, UTC_datetime):
        if not self.env.user.tz:
            raise Warning(ERREUR_FUSEAU)
        local_tz = pytz.timezone(self.env.user.tz)
        date = datetime.strptime(UTC_datetime, FORMAT_DATE)
        date = pytz.utc.localize(date, is_dst=None).astimezone(local_tz)
        return date.strftime(FORMAT_DATE)

    @api.multi
    def print_card(self):
        """Print the stock card."""
        self.ensure_one()

        location = self.location_id
        warehouse = self.env['stock.warehouse'].search([
            ('view_location_id.parent_left', '<=', location.parent_left),
            ('view_location_id.parent_right', '>=', location.parent_left)],
            limit=1)

        datas = {}
        datas['date_start'] = self.convert_UTC_TZ(self.date_start)
        datas['date_end'] = self.convert_UTC_TZ(self.date_end)
        datas['start'] = self.date_start
        datas['end'] = self.date_end
        datas['location_id'] = location.id
        datas['location_name'] = location.name
        datas['warehouse_name'] = warehouse.name
        datas['details'] = self.details

        report_name = 'hyd_stock_card.stock_card_report'
        if self.details:
            report_name = 'hyd_stock_card.stock_card_details_report'

        return self.env.ref(report_name).report_action(self, data=datas)
