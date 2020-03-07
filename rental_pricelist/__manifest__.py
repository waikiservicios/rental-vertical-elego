# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Pricelist',
    'summary': 'Enables the user to define different rental prices with time uom ("Month", "Day" and "Hour").',
    'description': '''
Rental prices are usually scaled prices based on a time unit, typically day, sometimes months or hour.
This modules integrates the standard Odoo pricelists into rental use cases and allows the user an
easy way to specify the prices in a product tab as well as to use all the enhanced pricelist features.
''',
    'version': '12.0.1.0.0',
    'category': 'sale',
    'author': 'Elego Software Solutions Gmbh',
    'depends': [
        'rental_base',
    ],
    'data': [
        'data/product_uom_data.xml',
        'views/sale_view.xml',
        'views/product_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'application': True,
    'license': 'LGPL-3',
}