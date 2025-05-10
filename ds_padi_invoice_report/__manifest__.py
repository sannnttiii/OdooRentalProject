# -*- encoding: utf-8 -*-
# Part of DS. See LICENSE file for full copyright and licensing details.
{
    'name': 'DS Padi - Invoice Report',
    'version': '1.0.0',
    'author': 'DS',
    'summary': 'Padi Rent Custom Invoice Report',
    'description':
    """ 
    DS Padi - Invoice Report
    This module is used to create a custom report for Padi Rent Invoice.
    """,
    "depends": ['base', 'sale', 'account',],
    'data': [
        # "security/security.xml",
        # "security/ir.model.access.csv",
        'views/view.xml',

    ],
    'installable': True,
    'license': 'LGPL-3',
}
