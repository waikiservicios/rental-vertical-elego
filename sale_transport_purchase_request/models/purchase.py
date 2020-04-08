# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
import logging

logger = logging.getLogger(__name__)


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    trans_origin_sale_line_ids = fields.Many2many(
        'sale.order.line',
        'rel_trans_sale_requisition_line',
        'requisition_line_id',
        'sale_line_id',
        copy=False,
    )
    name = fields.Char(
        'Name',
    )

    @api.multi
    def _prepare_purchase_order_line(self, name, product_qty=0.0, price_unit=0.0, taxes_ids=False):
        res = super(PurchaseRequisitionLine, self)._prepare_purchase_order_line(
            name=name, product_qty=product_qty, price_unit=price_unit, taxes_ids=taxes_ids)
        res['trans_origin_sale_line_ids'] = [
            (6, 0, self.trans_origin_sale_line_ids.ids)
        ]
        res['name'] = self.name
        res['date_planned'] = fields.Datetime.to_datetime(self.schedule_date)
        return res


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    trans_origin_sale_line_ids = fields.Many2many(
        'sale.order.line',
        'rel_trans_sale_purchase_line',
        'purchase_line_id',
        'sale_line_id',
        copy=False,
    )


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    transport_confirmed = fields.Boolean(
        'Transport Confirmed'
    )

    @api.multi
    def action_transport_confirm(self):
        self.ensure_one()
        #check if the related sale.order.line has already the same confirmed service
        sos = self.env['sale.order'].browse()
        for line in self.order_line:
            for sol in line.trans_origin_sale_line_ids:
                for pol in sol.trans_purchase_line_ids:
                    if pol.id != line.id \
                            and pol.product_id == line.product_id \
                            and pol.order_id.transport_confirmed:
                        raise exceptions.UserError(
                            _('You have already confirm the "%s" in Order "%s".') %(
                                pol.product_id.name,
                                pol.order_id.name
                            )
                        )
        self.write({'transport_confirmed': True})