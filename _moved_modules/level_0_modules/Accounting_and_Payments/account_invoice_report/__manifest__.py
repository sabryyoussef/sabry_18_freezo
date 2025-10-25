{
    'name': "account_invoice_report",
    'author': "Beshoy Wageh",
    'depends': ['base', 'account','l10n_ae','sale','account_reports'],
    'data': [
        'views/views.xml',
        'views/invoices.xml',
        'views/statement_report.xml',
        'views/sales.xml',
        'views/receipt_voucher.xml',
        'views/receipt_voucher_invoices.xml',
    ],
}
