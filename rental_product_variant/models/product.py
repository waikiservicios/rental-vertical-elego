# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    show_vehicle_number = fields.Boolean("Show Vehicle Identification Number")
    show_license_plate = fields.Boolean("Show License Plate")
    show_init_regist = fields.Boolean('Show Initial Registration')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    further_ref = fields.Char("Further Reference")
    qr_code = fields.Char('QR-Code')
    manu_year = fields.Char('Year of Manufacture')
    manu_id = fields.Many2one('product.manufacturer', 'Manufacturer') #Marke
    manu_type_id = fields.Many2one('product.manufacturer.type', 'Type', ondelete='set null') #Marke Typ
    fleet_type_id = fields.Many2one('fleet.type', 'Fleet Type', ondelete='set null') #Flottentyp

    #Category special fields
    vehicle_number = fields.Char("Vehicle Identification Number")
    license_plate = fields.Char("License Plate")
    init_regist = fields.Date('Initial Registration')
    show_vehicle_number = fields.Boolean("Show Vehicle Identification Number", related="categ_id.show_vehicle_number")
    show_license_plate = fields.Boolean("Show License Plate", related="categ_id.show_license_plate")
    show_init_regist = fields.Boolean('Show Initial Registration', related="categ_id.show_init_regist")

    #sol_ids = fields.One2many('sale.order.line', 'product_id', string='Sale Order Lines')
    #inv_line_ids = fields.One2many('account.invoice.line', 'product_id', string='Invoice Lines')
    #po_line_ids = fields.One2many('purchase.order.line', 'product_id', string='Purchase Order Lines')
    rental_order_ids = fields.One2many('sale.rental', 'rented_product_id', string='Rental Orders')
    stock_move_ids = fields.One2many('stock.move', 'product_id', string='Stock Moves')
    additional_info = fields.Html('Additional Infomation')
    dimension = fields.Char('Dimension')

    @api.multi
    def _get_sale_order_ids(self, type_id):
        self.ensure_one()
        sols = self.env['sale.order.line'].search([
            ('product_id','=',self.id)])
        return list(set([l.order_id.id for l in sols if l.order_id.type_id == type_id]))

    @api.multi
    def action_view_sale_order(self):
        self.ensure_one()
        type_id = self.env.ref('sale_order_type.normal_sale_type')
        record_ids = self._get_sale_order_ids(type_id)
        for rental_service in self.rental_service_ids:
            record_ids += rental_service._get_sale_order_ids(type_id)
        record_ids = list(set(record_ids))
        action = self.env.ref('rental_base.action_normal_orders').read([])[0]
        action['domain'] = [('id','in', record_ids)]
        return action

    @api.multi
    def action_view_rental_order(self):
        self.ensure_one()
        type_id = self.env.ref('rental_base.rental_sale_type')
        record_ids = self._get_sale_order_ids(type_id)
        for rental_service in self.rental_service_ids: 
            record_ids += rental_service._get_sale_order_ids(type_id)
        record_ids = list(set(record_ids))
        action = self.env.ref('rental_base.action_rental_orders').read([])[0]
        action['domain'] = [('id','in', record_ids)]
        return action

    @api.multi
    def action_view_all_purchase_order(self):
        self.ensure_one()
        pols = self.env['purchase.order.line'].search([('product_id', '=', self.id)])
        record_ids = list(set([l.order_id.id for l in pols]))
        view_id = self.env.ref("purchase.purchase_order_tree").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Purchase Orders'),
            'target': 'current',
            'view_mode': "tree",
            'view_id': view_id,
            'res_model': 'purchase.order',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            }

    @api.multi
    def action_view_all_invoice(self):
        self.ensure_one()
        invls = self.env['account.invoice.line'].search([('product_id', '=', self.id)])
        record_ids = list(set([l.invoice_id.id for l in invls]))
        view_id = self.env.ref("account.invoice_tree").id
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Invoices'),
            'target': 'current',
            'view_mode': "tree",
            'view_id': view_id,
            'res_model': 'account.invoice',
            'domain': "[('id','in',[" + ','.join(map(str, record_ids)) + "])]",
            }


class ProductManufacturer(models.Model):
    _name = 'product.manufacturer'
    _description = 'Product Manufacturer'

    name = fields.Char('Name')
    manufacturer_type_ids = fields.One2many('product.manufacturer.type', 'manufacturer_id')


class ProductManufacturerType(models.Model):
    _name = 'product.manufacturer.type'
    _description = 'Product Manufacturer Type'

    name = fields.Char('Name')
    manufacturer_id = fields.Many2one('product.manufacturer', 'Manufacturer')


class FleetType(models.Model):
    _name = 'fleet.type'
    _description = 'Fleet Type'

    name = fields.Char('Name')