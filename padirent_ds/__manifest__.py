{
    "name": "Padi Rent",
    "author": "Santi Daniel",
    "version": "18.0.0.0",
    "category": "",
    "depends": [
        'base','sale_management', 'purchase', 'account'
    ],
    "data": [
        'views/sale_view.xml',
        'views/res_partner_view.xml',
        'views/account_move_view.xml',
        'report/report_invoice_merge.xml',
    ],
    
    'installable': True
}
