from odoo import http
from odoo.http import request

class UserInputController(http.Controller):
    @http.route('/user_input/submit_user_input', type='json', auth='user')
    def submit_user_input(self, **kwargs):
        # request.env['user.input'].sudo().create({
        #     'name': name,
        #     'email': email
        # })
        try:
            record = request.env['user.input'].create({
                'name':kwargs.get('name'),
                'email': kwargs.get('address')
            })
            return {'status': record.id}
        except Exception as e:
            return {'status': 'failed'}

    @http.route('/user_input/submit_user_input', type='json', auth='user')
    def submit_user_input(self, **kwargs):
            try:
                record = request.env['user.input'].create({
                    'name': kwargs.get('name'),
                    'email': kwargs.get('address')
                })
                return {'success': True, 'record_id': record.id}
            except Exception as e:
                return {'success': False, 'error': str(e)}
