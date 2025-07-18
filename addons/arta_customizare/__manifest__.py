{
    'name': 'Auto Lot Reception',
    'version': '1.0',
    'summary': 'Generare loturi si alte sustomizari Arta',
    'author': 'Viorel Dragos',
    'category': 'Inventory',
    'depends': ['stock', 'mrp', 'stock_account','sale','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'reports/production_report_template.xml',
        'views/production_report_views.xml',
        'views/stock_move_line_views.xml',
        'views/cofetarie_intercompany_views.xml',
    ],
    'installable': True,
    'application': True,
}