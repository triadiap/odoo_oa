{
    'name': 'PTGN Connector',
    'version': '14.0.0.1.0',
    'summary': 'Office Automation Connector',
    'sequence': -100,
    'description': """This module has been build for PT GAG Nikel Office Automation Project""",
    'category': 'Productivity',
    'author': 'Internusa Cipta Solusi Perdana (ICSP)',
    'maintainer': 'Internusa Cipta Solusi Perdana (ICSP)',
    'website': 'https://icsp.co.id',
    'depends': ['mail','mod_gag_uac','base'],
    'data': [
       'security/ir.model.access.csv',
       'views/office_connector_view.xml',
       'views/master_trading_partner.xml',
       'views/api_documentation_form.xml',
        'views/office365_form.xml',
       'views/menu_views.xml'
    ],
     'assets': {
        'web.assets_backend': [
            'mod_gag_office_connector/static/src/img/*'
        ],
    },
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}