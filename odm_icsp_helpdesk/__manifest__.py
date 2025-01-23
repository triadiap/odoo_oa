{
    'name': 'IT Helpdesk Modules',
    'version': '14.0.0.1.0',
    'summary': 'IT Helpdesk Modules',
    'sequence': -100,
    'description': """This module has been build for helpdesk services""",
    'category': 'Tools',
    'author': 'Bayu Sulistiawan',
    'maintainer': 'Internusa Cipta Solusi Perdana (ICSP)',
    'website': 'https://icsp.co.id',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/user_access_groups.xml',
        'views/form_ticketing.xml',
        'data/data.xml',
        'views/menu_views.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}