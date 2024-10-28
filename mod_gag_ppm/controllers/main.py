import json

from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
import requests

class FormControlls(http.Controller):
    @http.route('/my_form_module/submit', type='json', auth='user', methods=['POST'])
    def submit_form(self, **kwargs):
        name = kwargs.get('name')
        address = kwargs.get('address')
            # Here you can handle the form data, e.g., save it to the database
            # For demonstration, we'll just return a message
        # users = request.env['res.users'].search([], limit=10)
        data = []
        # for sistemuser in users:
        data.append({
                'nama' : name,
                'alamat': address
            })

        return{
            'status' : 'success',
            'message' : data,
        }

    @http.route('/my_module/get_html_content', type='json', auth='public')
    def get_html_content(self):
        return{
            'message': 'Notification from server',
        }

    @http.route('/my_module/restapicall', type='json', auth='public',  methods=['POST'])
    def restapicall(self, **kwargs):
        api_url = 'https://dummyjson.com/products'
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()  # Return the API response to the client-side
        else:
            return {'error': 'Failed to fetch data'}

    @http.route('/user_input/get_html', type='json', auth='public', methods=['POST'], csrf=False)
    def get_html(self):
        some_parameter = 'Parsed Value Test'
        # Generate or fetch the HTML content you want to return
        html_content = f"""
                            <div class="card row">
                                <div class = "col-12" style="width:100%;margin-top:5px;">
                                        <h1 class="label">Form Input Data</h1>
                                        <form id="FrmUserInputData" name="FrmUserInputData">
                                        <div style="padding-top:20px;">
                                              <label for="exampleFormControlInput1" class="form-label">Email address</label>
                                              <input type="email" class="form-control" id="name" name="name" placeholder="name@example.com"/>
                                        </div>
                                        <div style="padding-top:20px;">
                                              <label for="exampleFormControlTextarea1" class="form-label">Example textarea</label>
                                              <textarea class="form-control" id="address" name="address" rows="3">{some_parameter}</textarea>
                                              <span id="pesan_error" class="error field-validation-valid" style="color:red;"></span>
                                        </div>
                                        <div style="padding-top:20px;padding-bottom:10px;" class="text-right">
                                                <button type="submit" id="my_button" class="btn btn-primary submit_button">Submit</button>
                                        </div>
                                        <notebook>
                                            <page string="Budget Lines">
                                            </page>
                                        </notebook>
                                    </form>
                                    <div id="prnfeedback"></div>
                                </div>
                                
                            </div>
            """
        return {
            'status':'success',
            'message' : html_content
        }
    @http.route('/my_module/listofmenucall', auth='user', type='json')
    def listofmenucall(self,**kwargs):
        cr = request.env.cr
        sql_query = """
            SELECT * FROM tb_menu 
        """
        cr.execute(sql_query)
        results = cr.fetchall()

        output = ''
        for listofmenu in results:

            output += '<li class="o_search_panel_category_value list-group-item border-0 item" data-id='+str(listofmenu[2])+'>'
            output += '<header class="list-group-item-action">'
            output += '<label class="o_search_panel_label mb0 o_with_counters">'
            output += '<div class="o_toggle_fold"></div>'
            output += '<span class="o_search_panel_label_title">'+listofmenu[1]+'</span>'
            output += '</label>'
            output += '</header>'
            output += '</li>'

        return output
    @http.route('/my_module/contentrender', type='json', auth='user',methods=['POST'])
    def contentrender(self, **kwargs):
        nomormenu = kwargs.get('value')
        cr = request.env.cr
        sql_query = """
            SELECT route_address
            FROM tb_menu 
            WHERE idmenu = %s
         """
        cr.execute(sql_query,(nomormenu,))
        results = cr.fetchall()
        return redirect(results[0][0])

    @http.route('/my_module/get_data_pillar', type='json', auth='user', methods=['POST'])
    def get_data_pillar(self,**kwargs ):
        records = request.env['pillar.group'].search([])
        # Prepare the data to be returned as JSON
        data = []
        for record in records:
            data.append({
                'id': record.id,
                'nama_pillar': record.nama_pillar,
                # Add other fields as needed
            })
        # Return the data as JSON
        return data


