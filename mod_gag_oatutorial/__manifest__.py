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
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/asset_global.xml',
        'views/tutorial_views.xml',
        'views/menu_views.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
                'web.assets_backend': [
                    'mod_gag_oatutorial/static/src/js/tree_button_tutorial.js'
                ],
        }
}