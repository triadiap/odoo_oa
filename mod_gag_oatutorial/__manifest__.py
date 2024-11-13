{
    'name': 'PTGN Tutorial',
    'version': '14.0.0.1.0',
    'summary': 'Office Automation Tutorial',
    'sequence': -100,
    'description': """This module has been build for PT GAG Nikel Office Automation Project""",
    'category': 'Productivity',
    'author': 'Internusa Cipta Solusi Perdana (ICSP)',
    'maintainer': 'Internusa Cipta Solusi Perdana (ICSP)',
    'website': 'https://icsp.co.id',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_ui_menu_security.xml',
        'views/tutorial_views.xml',
        'views/menu_views.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}