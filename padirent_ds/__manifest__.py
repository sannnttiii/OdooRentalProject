{
    "name": "Padi Rent",
    "author": "Santi Daniel",
    "version": "18.0.0.0",
    "category": "",
    "depends": [
        'base', 'sale', 'sale_management', 'purchase', 'account', 'base_accounting_kit', 'base_account_budget', 'dynamic_accounts_report',
    ],
    "data": [
        'security/security.xml',
        'views/sale_view.xml',
        'views/res_partner_view.xml',
        'views/account_move_view.xml',
        'views/menus.xml',
        'report/report_invoice_merge.xml',
    ],
    
    'installable': True
}
