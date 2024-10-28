import json
import calendar
import random
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
import requests
from datetime import datetime

class BargingReporting(http.Controller):
    @http.route('/barging_module/get_data_month', type='json', auth='user', methods=['POST'])
    def get_data_month(self, **kwargs):
        months = [{"id": str(i), "name": month} for i, month in enumerate(calendar.month_name) if month]
        return months

    @http.route('/barging_module/get_data_year', type='json', auth='user', methods=['POST'])
    def get_data_year(self, **kwargs):
        current_year = datetime.now().year
        years = [{"id": str(year), "name": str(year)} for year in range(current_year - 5, current_year + 11)]
        # Move the current year to the top of the list
        years.sort(key=lambda x: (x['id'] != str(current_year), x['id']))
        return years

    @http.route('/barging_module/get_cards_data', type='json', auth='user', methods=['POST'], csrf=False)
    def get_cards_data(self):
        records = request.env['oa.master.vendor'].search([])
        output = ''
        for record in records:
            output += '<div class="col-md-6" style="margin-top:10px;";>'
            output += '<div class="card" style="width:100%;background-color:#fffff;padding-bottom:20px;padding-right:10px;">'
            output += '<label><h5 style="margin-left:10px; margin-top:10px;font-weight:normal;text-align:center;">'+str(record['name'])+'</h5></label>'
            output += '<canvas id="bichart_'+str(record['id'])+'"></canvas>'
            output += '</div>'
            output += '</div>'

        return {
            'id': [item['id'] for item in records],
            'status': 'success',
            'card_lists': output
        }
    @http.route('/barging_module/get_production_data', type='json', auth='user', methods=['POST'], csrf=False)
    def get_production_data(self, **kwargs):
        vendorid = kwargs.get('idvendor')
        tahun = int(kwargs.get('tahun'))
        bulan = int(kwargs.get('bulan'))
        query = """
                   SELECT
                       SUM(qty_plan) AS qty_plan_sum,
                       SUM(qty_actual) AS qty_actual_sum,
                       vendor_id,
                       TO_CHAR(production_date, 'DD/MM/YYYY') AS formatted_production_date
                   FROM bi_planactual_production
                   WHERE 1=1
               """
        params = []
        if vendorid:
            query += " AND vendor_id = %s"
            params.append(vendorid)

        if bulan and tahun:
            query += " AND EXTRACT(MONTH FROM production_date) = %s AND EXTRACT(YEAR FROM production_date) = %s"
            params.append(bulan)
            params.append(tahun)
        query += " GROUP BY vendor_id, production_date ORDER BY production_date ASC"

        request.env.cr.execute(query, tuple(params))

        results = request.env.cr.fetchall()
        plan_data = [plan[0] for plan in results]
        actual_data = [actual[1] for actual in results]
        tanggal_produksi = [tanggal[3] for tanggal in results]

        if results:
            dataset_plan = {
                    'label': 'Plan Quantity',
                    'data': plan_data,
                    'backgroundColor': 'rgba(242, 175, 17, 0.8)',
                    'borderColor': 'rgba(242, 175, 17, 1)',
                    'borderWidth': 1
            }
            dataset_actual = {
                    'label': 'Actual Quantity',
                    'data': actual_data,
                    'backgroundColor': 'rgba(8, 212, 29, 0.8)',
                    'borderColor': 'rgba(8, 212, 29, 1)',
                    'borderWidth': 1
                }
            return{
                'success' : True,
                'vendorid' : vendorid,
                'labels' : tanggal_produksi,
                'datasets' : [dataset_plan,dataset_actual]
            }
        else:
            return{
                'error' : True,
                'message' : 'Data Not Found'
            }

    @http.route('/barging_module/get_production_barging_cards', type='json', auth='user', methods=['POST'], csrf=False)
    def get_production_barging_cards(self, **kwargs):
         chartviews = ''
         chartviews += '<div class="col-md-12" style="margin-top:10px;";>'
         chartviews += '<div class="card" style="width:100%;background-color:#fffff;padding-bottom:20px;padding-right:10px;">'
         chartviews += '<label><h5 style="margin-left:10px; margin-top:10px;font-weight:normal;text-align:center;">Production & Barging (Tonnage)</h5></label>'
         chartviews += '<canvas id="prodbargingchart"></canvas>'
         chartviews += '</div>'
         chartviews += '</div>'

         return {
             'status' : True,
             'productionbargingchart' : chartviews
         }

    @http.route('/barging_module/get_total_production_barging', type='json', auth='user', methods=['POST'], csrf=False)
    def get_total_production_barging(self, **kwargs):
        tahun = int(kwargs.get('tahun'))
        bulan = int(kwargs.get('bulan'))
        getmastervendor = request.env['oa.master.vendor'].search([])
        vendorlist = []
        for vendors in getmastervendor:
            vendorlist.append({
                'idvendor' : vendors.id,
                'label' : f"Output {vendors.name}",
                'labels' : [actual[2] for actual in self.get_production_pervendor(tahun, bulan, vendors.id)],
                'data' : [actual[0] for actual in self.get_production_pervendor(tahun, bulan, vendors.id)],
                'backgroundColor': self.get_random_color(),
                'borderColor': self.get_random_color(),
                'borderWidth': 1
            })
        return{
            'status':'success',
            'datasets' : vendorlist
        }
    def get_production_pervendor(self, tahun, bulan, vendorid):
        query = """
                         SELECT
                             SUM(qty_actual) AS qty_actual_sum,
                             vendor_id,
                             TO_CHAR(production_date, 'DD/MM/YYYY') AS formatted_production_date
                         FROM bi_planactual_production
                         WHERE 1=1
                     """
        params = []
        if vendorid:
            query += " AND vendor_id = %s"
            params.append(vendorid)
        if bulan and tahun:
            query += " AND EXTRACT(MONTH FROM production_date) = %s AND EXTRACT(YEAR FROM production_date) = %s"
            params.append(bulan)
            params.append(tahun)
        query += " GROUP BY vendor_id, production_date ORDER BY production_date ASC"
        request.env.cr.execute(query, tuple(params))
        results = request.env.cr.fetchall()
        return results

    def getdates(self, tahun, bulan):
        query = """
                    SELECT  SUM(qty_actual) AS qty_actual_sum,
                    vendor_id, 
                    TO_CHAR(production_date, 'DD/MM/YYYY') AS formatted_production_date 
                    FROM bi_planactual_production
                    WHERE EXTRACT(MONTH FROM production_date) = %s
                    AND EXTRACT(YEAR FROM production_date) = %s
                    GROUP BY vendor_id, production_date
                    ORDER BY production_date ASC
                """
        # Execute the SQL query
        request.env.cr.execute(query, (bulan, tahun))
        # Fetch all the results
        results = request.env.cr.fetchall()
        # Format the results to be returned as JSON
        formatted_results = [result[2] for result in results]
        return formatted_results
    def get_random_color(self):
        """ Generate random RGBA color """
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'rgba({r}, {g}, {b}, 0.8)'

    @http.route('/barging_module/production_output_chart', type='json', auth="user")
    def get_production_output(self, month, year):
        query = """
                    SELECT p.production_date, v.name as vendor_name, SUM(p.qty_actual) as total_qty
                    FROM bi_planactual_production p
                    JOIN oa_master_vendor v ON p.vendor_id = v.id
                    WHERE EXTRACT(MONTH FROM p.production_date) = %s
                    AND EXTRACT(YEAR FROM p.production_date) = %s
                    GROUP BY p.production_date, v.name
                    ORDER BY p.production_date
                """
        request.env.cr.execute(query, (month, year))
        results = request.env.cr.fetchall()
        # Prepare the data for Chart.js
        output_by_vendor = {}
        for row in results:
            date_str = row[0].strftime('%d/%m/%Y')
            vendor_name = row[1]
            total_qty = row[2]

            if date_str not in output_by_vendor:
                output_by_vendor[date_str] = {}
            if vendor_name not in output_by_vendor[date_str]:
                output_by_vendor[date_str][vendor_name] = 0

            output_by_vendor[date_str][vendor_name] += total_qty

        tgl_produksi = list(output_by_vendor.keys())
        vendor_names = list({vendor for date in tgl_produksi for vendor in output_by_vendor[date].keys()})
        dataset = []
        for vendor in vendor_names:
            vendor_data = [output_by_vendor[date].get(vendor, 0) for date in tgl_produksi]
            dataset.append({
                'label': vendor,
                'data': vendor_data,
                'backgroundColor': 'rgba(75, 192, 192, 0.5)' if vendor == vendor_names[
                    0] else 'rgba(153, 102, 255, 0.5)'
            })

        return {
            'status' : 'success',
            'labels': tgl_produksi,
            'datasets': dataset
        }



