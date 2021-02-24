# -*-coding: utf-8 -*-
from odoo import api, fields, models, _
from openerp.exceptions import Warning
from datetime import datetime
import pytz

FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
ERREUR_FUSEAU = _("Set your timezone in preferences")


def convert_UTC_TZ(self, UTC_datetime):
    if not self.env.user.tz:
        raise Warning(ERREUR_FUSEAU)
    local_tz = pytz.timezone(self.env.user.tz)
    date = datetime.strptime(UTC_datetime, FORMAT_DATE)
    date = pytz.utc.localize(date, is_dst=None).astimezone(local_tz)
    return date.strftime(FORMAT_DATE)


class StockCardDetailsReport(models.AbstractModel):
    _name = 'report.hyd_stock_card.stock_card_details_template'

    @api.multi
    def get_report_values(self, docids, data=None):

        quant_obj = self.env["stock.quant"]
        products = self.env['product.product']

        start = data['start']
        end = data['end']
        date_start = data['date_start']
        date_end = data['date_end']
        location_id = data['location_id']

        quants = quant_obj.search([('location_id', 'child_of', location_id)])
        products |= quants.mapped('product_id')

        moves = self.env['stock.move'].search([
            ('date', '>=', start),
            ('date', '<=', end),
            ('state', '=', 'done'),
            '|',
            ('location_dest_id', 'child_of', location_id),
            ('location_id', 'child_of', location_id)])
        moves_to_now = self.env['stock.move'].search([
            ('date', '>=', end),
            ('date', '<=', fields.Datetime.now()),
            ('state', '=', 'done'),
            '|',
            ('location_dest_id', 'child_of', location_id),
            ('location_id', 'child_of', location_id)])

        location = self.env['stock.location'].browse(location_id)
        location_ids = self.env['stock.location'].search([
            ('parent_left', '>=', location.parent_left),
            ('parent_right', '<=', location.parent_right)])

        mv_in = moves.filtered(
            lambda x: x.location_dest_id.id in location_ids.ids)
        mv_out = moves.filtered(
            lambda x: x.location_id.id in location_ids.ids)
        mv_tonow_in = moves_to_now.filtered(
            lambda x: x.location_dest_id.id in location_ids.ids)
        mv_tonow_out = moves_to_now.filtered(
            lambda x: x.location_id.id in location_ids.ids)

        products |= mv_in.mapped("product_id")
        products |= mv_out.mapped("product_id")

        datas = {}
        datas['warehouse'] = data['warehouse_name']
        datas['location'] = data['location_name']
        datas['date_from'] = date_start
        datas['date_to'] = date_end

        result = []
        for product in products:
            line = {}
            line['name'] = product.name
            line['ref'] = product.default_code
            line['uom'] = product.uom_id.name

            mv_in_pro = mv_in.filtered(
                lambda x: x.product_id.id == product.id)
            mv_out_pro = mv_out.filtered(
                lambda x: x.product_id.id == product.id)
            mv_tonow_in_pro = mv_tonow_in.filtered(
                lambda x: x.product_id.id == product.id)
            mv_tonow_out_pro = mv_tonow_out.filtered(
                lambda x: x.product_id.id == product.id)

            product_uom = product.uom_id
            tot_in = 0
            for elt in mv_in_pro:
                if product_uom.id != elt.product_uom.id:
                    factor = product_uom.factor / elt.product_uom.factor
                else:
                    factor = 1.0
                tot_in += elt.product_uom_qty * factor

            tot_out = 0
            for elt in mv_out_pro:
                if product_uom.id != elt.product_uom.id:
                    factor = product_uom.factor / elt.product_uom.factor
                else:
                    factor = 1.0
                tot_out += elt.product_uom_qty * factor

            tot_tonow_in = 0
            for elt in mv_tonow_in_pro:
                if product_uom.id != elt.product_uom.id:
                    factor = product_uom.factor / elt.product_uom.factor
                else:
                    factor = 1.0
                tot_tonow_in += elt.product_uom_qty * factor

            tot_tonow_out = 0
            for elt in mv_tonow_out_pro:
                if product_uom.id != elt.product_uom.id:
                    factor = product_uom.factor / elt.product_uom.factor
                else:
                    factor = 1.0
                tot_tonow_out += elt.product_uom_qty * factor

            actual_qty = product.with_context(
                {'location': location_id}).qty_available
            actual_qty += tot_tonow_out - tot_tonow_in

            line['si'] = actual_qty - tot_in + tot_out
            line['in'] = tot_in
            line['out'] = tot_out
            line['bal'] = tot_in - tot_out
            line['fi'] = actual_qty
            result.append(line)

            move_in_show = mv_in_pro - mv_tonow_in_pro
            move_out_show = mv_out_pro - mv_tonow_out_pro

            move_to_show = self.env['stock.move']
            move_to_show |= move_in_show
            move_to_show |= move_out_show
            move_to_show.sorted(lambda r: r.date)
            line['lines'] = []
            val_in = actual_qty - tot_in + tot_out
            val_fin = val_in
            for mv in move_to_show:

                src = mv.location_id.id
                dst = mv.location_dest_id.id
                qty = mv.product_uom_qty

                val_in = qty if dst in location_ids.ids else 0
                val_out = qty if src in location_ids.ids else 0
                val_bal = val_in - val_out
                val_fin += val_bal

                mvdate = convert_UTC_TZ(self, mv.date) if mv.date else ""

                elt = {}
                elt['mv'] = mv.reference or "-"
                elt['date'] = str(mvdate) or "-"
                elt['in'] = val_in
                elt['out'] = val_out
                elt['bal'] = val_bal
                elt['fi'] = val_fin
                line['lines'].append(elt)

        datas['lines'] = result

        return {'doc_ids': docids, 'data': datas}
