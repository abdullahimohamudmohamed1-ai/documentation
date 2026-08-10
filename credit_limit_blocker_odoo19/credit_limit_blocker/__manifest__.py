{
    "name": "Credit Limit Blocker",
    "version": "19.0.1.0.0",
    "category": "Accounting",
    "summary": "Hard credit-limit blocking for Sales Orders and Customer Invoices",
    "author": "Custom",
    "license": "LGPL-3",
    "depends": ["sale_management", "account"],
    "data": [
        "security/credit_limit_groups.xml",
        "views/res_partner_views.xml"
    ],
    "installable": True,
    "application": False
}
