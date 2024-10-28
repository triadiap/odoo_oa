from odoo import http
from odoo.http import request
import json
from datetime import datetime,date

class OfficeConnectorController(http.Controller):
    @http.route('/api/connector/sync', type='http', auth='public', methods=['POST'], csrf=False)
    def sync_data(self, **kwargs):
        # Fetch the token from the request headers
        token = request.httprequest.headers.get('Authorization')

        if not token:
            request.env['oa.api.hit.logs'].sudo().create({
                'name': None,
                'status': 400,
                'message': 'Missing token in request',
                'token_number': token,
                'timestamp': datetime.now(),
                'api_id': None
            })
            return json.dumps({'status': 'error', 'message': 'Missing token in request'})

        # Remove 'Bearer ' prefix if present
        if token.startswith("Bearer "):
            token = token[7:]

        # Validate token
        trading_partner = request.env['oa.trading.partner'].sudo().search(
            [('trading_partner_token', '=', token)], limit=1
        )
        if not trading_partner:
            request.env['oa.api.hit.logs'].sudo().create({
                'name': None,
                'status': 401,
                'message': 'Invalid token',
                'token_number': token,
                'timestamp': datetime.now(),
                'api_id': None
            })
            return json.dumps({'status': 'error', 'message': 'Invalid token'})

        # Retrieve form data parameters
        link_id = request.params.get('link_id')
        filters = request.params.get('filters', '[]')
        limit = request.params.get('limit')
        offset = request.params.get('offset', '0')

        # Convert offset to integer
        try:
            limit = int(limit) if limit else None  # Convert limit to int if provided
            offset = int(offset)
        except ValueError:
            return json.dumps({'status': 'error', 'message': 'Invalid offset value'})

        # Parse filters (expecting it as a JSON string in form-data)
        try:
            filters = json.loads(filters)
        except json.JSONDecodeError:
            return json.dumps({'status': 'error', 'message': 'Invalid filters format'})

        # Retrieve the data model for the provided link_id
        data_retrieve = request.env['office.connector.config'].sudo().search(
            [('token', '=', link_id)], limit=1
        )
        if not data_retrieve:
            request.env['oa.api.hit.logs'].sudo().create({
                'name': trading_partner.id,
                'status': 402,
                'message': 'Invalid API Name',
                'token_number': token,
                'timestamp': datetime.now(),
                'api_id': None
            })
            return json.dumps({'status': 'error', 'message': 'Invalid API Name'})

        # Ensure authorization for this link_id
        authorization_check = request.env['office.connector.config'].sudo().search([
            ('token', '=', link_id),
            ('trading_partner_name', '=', trading_partner.id)
        ])
        if not authorization_check:
            return json.dumps({'status': 'error', 'message': 'Your token is not authorized for this link ID'})

        # Get model and sync fields
        rest_api_name = data_retrieve.sync_model.model
        sync_fields = data_retrieve.sync_fields.mapped('name')
        if not sync_fields:
            request.env['oa.api.hit.logs'].sudo().create({
                'name': trading_partner.id,
                'status': 403,
                'message': 'No fields configured for syncing',
                'token_number': token,
                'api_id': data_retrieve.id,
                'timestamp': datetime.now(),
                'filters_applied': json.dumps(filters),
                'record_limit': limit,
                'record_offset': offset
            })
            return json.dumps({'status': 'error', 'message': 'No fields configured for syncing'})

        # Parse filters based on expected types
        parsed_filters = []
        for filter_item in filters:
            field_name = filter_item.get('field')
            value = filter_item.get('value')
            operator = filter_item.get('operator', '=')

            # Example type conversion
            if field_name in ['age', 'price']:
                try:
                    value = int(value)
                except ValueError:
                    return json.dumps({'status': 'error', 'message': f'Invalid integer for field {field_name}'})
            parsed_filters.append((field_name, operator, value))

        try:
            # Search records based on parsed filters
            records = request.env[rest_api_name].sudo().search(parsed_filters, limit=limit, offset=offset)
            data = records.read(sync_fields)

            # Convert date and datetime fields to string format
            for record in data:
                for key, value in record.items():
                    if isinstance(value, datetime):
                        record[key] = value.isoformat()  # Convert datetime to ISO 8601 string
                    elif isinstance(value, date):  # For date objects
                        record[key] = value.isoformat()  # Convert date to ISO 8601 string

            # Log API hit success
            request.env['oa.api.hit.logs'].sudo().create({
                'name': trading_partner.id,
                'status': 200,
                'message': 'Success',
                'token_number': token,
                'api_id': data_retrieve.id,
                'timestamp': datetime.now(),
                'filters_applied': json.dumps(filters),
                'record_limit': limit,
                'record_offset': offset
            })

            return json.dumps({'status': 'success', 'data': data})

        except Exception as e:
            # Log error if data retrieval fails
            request.env['oa.api.hit.logs'].sudo().create({
                'name': trading_partner.id,
                'status': 500,
                'message': str(e),
                'token_number': token,
                'api_id': data_retrieve.id,
                'timestamp': datetime.now(),
                'filters_applied': json.dumps(filters),
                'record_limit': limit,
                'record_offset': offset
            })
            return json.dumps({'status': 'error', 'message': str(e)})