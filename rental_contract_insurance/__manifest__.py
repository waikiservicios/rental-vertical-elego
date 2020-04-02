# Part of rental-vertical See LICENSE file for full copyright and licensing details.

{
    'name': 'Rental Contract Insurance',
    'summary': 'Rental Contract Insurance',
    'version': '12.0.1.0.0',
    'category': 'rental',
    'author': 'OCA/Elego Software Solutions GmbH',
    'depends': [
        'rental_contract_month',
        'rental_product_insurance',
    ],
    'data': [
        'data/contract_template_data.xml',
        'data/product_data.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'auto_install': False,
    'license': 'LGPL-3',
}