import json
import calendar
import random
from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
import requests
import locale
from datetime import datetime

class PpmReporting(http.Controller):
    @http.route('/ppm_modules/get_pillar_cards', type='json', auth='user', methods=['POST'], csrf=False)
    def get_pillar_cards(self):
        records = request.env['pillar.group'].search([])
        card = ''
        for record in records:
            card += '<div class="col-md-6" style="margin-top:10px;";>'
            card += '<div class="card" style="width:100%;background-color:#fffff;padding-bottom:30px;padding-right:10px;height:100px;padding-left:10px;">'
            card += '<label><h6 style="margin-top:10px;font-weight:normal;text-align:left;">'+ str(
                        record['nama_pillar']) + ' : </h6></label>'
            card += ' <h1 id="delivered_'+str(record['id'])+'" style="text-align:center;font-weight:bold;font-family:arial;"></h1>'
            card += '<div style="display:flex;justify-content: space-between;align-items: center;margin-bottom:10px;">'
            card += '<h7 id="expense'+str(record['id'])+'" style="text-align:right;color:#808b96;font-weight:normal;">Expense</h7>'
            card += '<h7 id="budget'+str(record['id'])+'" style="text-align:left;color:#808b96;font-weight:normal;">Budget</h7>'
            card += '</div>'
            card += '</div>'
            card += '</div>'

        return {
            'id': [item['id'] for item in records],
            'status': 'success',
            'card_lists': card
        }
    @http.route('/ppm_modules/get_percentagebypillar_chart', type='json', auth='user', methods=['POST'], csrf=False)
    def get_percentagebypillar_chart(self,year):
        if not year:
            return json.dumps({'error': 'Year is required'})
        try:
            year = int(year)  # Ensure the year is an integer
        except ValueError:
            return json.dumps({'error': 'Invalid year format'})
        query = """
                SELECT
                        namapillar,
                        SUM(nilai_anggaran)
                FROM
                        detail_anggaran_perbulan
                WHERE
                        EXTRACT(YEAR FROM date_of_fiscal) =  %s
                GROUP BY
                        namapillar
        """
        query_params = [year]  # Filter by year only
        request.env.cr.execute(query, query_params)
        result = request.env.cr.fetchall()

        labels = [row[0] for row in result]
        data = [row[1] for row in result]

        # Dynamically create colors for each segment
        background_colors = [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ]
        border_colors = [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
        ]
        border_widths = [1 for _ in labels]  # Set dynamic border widths for each section

        # Truncate or repeat colors if necessary to match the number of segments
        while len(background_colors) < len(labels):
            background_colors.extend(background_colors)  # Extend the color list
        while len(border_colors) < len(labels):
            border_colors.extend(border_colors)  # Extend the color list

        return {
            'status': 'success',
            'data' : data,
            'labels' : labels,
            'backgroundColors': background_colors[:len(labels)],  # Ensure length matches labels
            'borderColors': border_colors[:len(labels)],
            'borderWidths': border_widths
        }

    @http.route('/ppm_modules/getmonthlyvsbudgetchartdata', type='json', auth='user', methods=['POST'], csrf=False)
    def getmonthlyvsbudgetchartdata(self,year):
        if not year:
            return json.dumps({'error': 'Year is required'})
        try:
            year = int(year)  # Ensure the year is an integer
        except ValueError:
            return json.dumps({'error': 'Invalid year format'})
        query = """
                SELECT
                    row_number() OVER () AS id,
                    m.month_number,
                    m.month_name,
                    COALESCE(b.total_budget, 0) AS total_budget,
                    COALESCE(t.total_expense, 0) AS total_expense,
                    CASE
                        WHEN COALESCE(b.total_budget, 0) = 0 THEN 0 -- If total_budget is 0, set total_balance to 0
                        WHEN COALESCE(b.total_budget, 0) - COALESCE(t.total_expense, 0) < 0 THEN 0 -- If balance is negative, set to 0
                        ELSE COALESCE(b.total_budget, 0) - COALESCE(t.total_expense, 0) -- Otherwise, calculate normally
                    END AS total_balance
                FROM
                   (SELECT
                       1 AS month_number, 'Jan' AS month_name
                       UNION ALL SELECT 2, 'Feb'
                       UNION ALL SELECT 3, 'Mar'
                       UNION ALL SELECT 4, 'Apr'
                       UNION ALL SELECT 5, 'May'
                       UNION ALL SELECT 6, 'Jun'
                       UNION ALL SELECT 7, 'Jul'
                       UNION ALL SELECT 8, 'Aug'
                       UNION ALL SELECT 9, 'Sep'
                       UNION ALL SELECT 10, 'Oct'
                       UNION ALL SELECT 11, 'Nov'
                       UNION ALL SELECT 12, 'Dec') AS m

                LEFT JOIN (
                        SELECT
                           EXTRACT(MONTH FROM b.date_of_fiscal) AS month_number,
                           EXTRACT(YEAR FROM b.date_of_fiscal) AS tahunanggaran,
                           SUM(b.nilai_anggaran) AS total_budget
                        FROM
                           detail_anggaran_perbulan b
                        WHERE EXTRACT(YEAR FROM b.date_of_fiscal) = %s
                        GROUP BY
                           EXTRACT(MONTH FROM b.date_of_fiscal), EXTRACT(YEAR FROM b.date_of_fiscal)
                             ) b ON m.month_number = b.month_number
                LEFT JOIN (
                      SELECT
                            EXTRACT(MONTH FROM t.transaction_date) AS month_number,
                            EXTRACT(YEAR FROM t.transaction_date) AS tahunanggaran,
                            SUM(t.transaction_subtotal) AS total_expense
                      FROM
                            detail_trans_perbudget t
                      WHERE EXTRACT(YEAR FROM t.transaction_date) = %s
                      GROUP BY
                               EXTRACT(MONTH FROM t.transaction_date), EXTRACT(YEAR FROM t.transaction_date)
                                )t ON m.month_number = t.month_number
                ORDER BY
                           m.month_number
        """
        query_params = [year,year]  # Filter by year only
        request.env.cr.execute(query, query_params)
        result = request.env.cr.fetchall()
        # Prepare data for the chart
        labels = []
        total_budget = []
        total_expense = []
        total_balance = []

        for row in result:
            labels.append(row[2])  # month_name
            total_budget.append(row[3])  # total_budget
            total_expense.append(row[4])  # total_expense
            total_balance.append(row[5])  # total_balance

            # Format data for Chart.js multiple line chart
            data = {
                'labels': labels,  # Month names (Jan, Feb, etc.)
                'datasets': [
                    {
                        'label': 'Total Budget',
                        'data': total_budget,
                        'borderColor': 'rgba(54, 162, 235, 1)',  # Line color for budget
                        'fill': True
                    },
                    {
                        'label': 'Total Expense',
                        'data': total_expense,
                        'borderColor': 'rgba(255, 99, 132, 1)',  # Line color for expenses
                        'fill': True
                    },
                    {
                        'label': 'Total Balance',
                        'data': total_balance,
                        'borderColor': 'rgba(75, 192, 192, 1)',  # Line color for balance
                        'fill': True
                    }
                ]
            }
        return {
            'status' : 'success',
            'dataset' : data
        }

    @http.route('/ppm_modules/getbudgetperpillardetailinfo', type='json', auth='user', methods=['POST'], csrf=False)
    def getbudgetperpillardetailinfo(self,idpillar,year):
        query = """
                SELECT row_number() OVER () AS id,
                m.idpillar,
                m.pillar_nama,
                COALESCE(b.total_budget, 0) AS total_budget,
                COALESCE(t.total_expense, 0) AS total_expense,
                CASE
                    WHEN COALESCE(b.total_budget, 0) = 0 THEN 0 -- If total_budget is 0, set total_balance to 0
                    WHEN COALESCE(t.total_expense, 0) = 0 THEN 0 -- If total_budget is 0, set total_balance to 0
                    ELSE ((COALESCE(b.total_budget, 0) - COALESCE(t.total_expense, 0))/COALESCE(b.total_budget, 0))*100 -- Otherwise, calculate normally
                END AS percentage_deliverable
                FROM (
                    SELECT id as idpillar, 
                    nama_pillar as pillar_nama FROM pillar_group
                )as m
                LEFT JOIN(
                    SELECT
                     b.namapillar as pillar_nama,
                     EXTRACT(YEAR FROM b.date_of_fiscal) AS tahunanggaran,
                     SUM(b.nilai_anggaran) AS total_budget
                    FROM
                         detail_anggaran_perbulan b
                    WHERE 
                        EXTRACT(YEAR FROM b.date_of_fiscal) = %s
                    GROUP BY 
                        EXTRACT(YEAR FROM b.date_of_fiscal), b.namapillar
                ) b ON m.pillar_nama = b.pillar_nama
                LEFT JOIN(
                    SELECT
                     t.namapillar as pillar_nama,
                     EXTRACT(YEAR FROM t.transaction_date) AS tahunanggaran,
                     SUM(t.transaction_subtotal) AS total_expense
                    FROM
                         detail_trans_perbudget t
                    WHERE 
                        EXTRACT(YEAR FROM t.transaction_date) = %s
                    GROUP BY 
                        EXTRACT(YEAR FROM t.transaction_date), t.namapillar
                ) t ON m.pillar_nama = t.pillar_nama
        """
        labels = []
        data = []
        query_params = [year, year]  # Filter by year only
        request.env.cr.execute(query, query_params)
        result = request.env.cr.fetchall()
        # Set the locale to Indonesia for proper formatting
        locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
        for records in result:
            data.append({
                'idpillar': records[1],
                'year' : year,
                'total_budget':locale.format_string('%.2f', records[3], grouping=True),
                'total_expense' : locale.format_string('%.2f', records[4], grouping=True),
                'percentage': locale.format_string('%.2f', records[5], grouping=True)
            })

        return{
            'status' : 'success',
            'data' : data
        }

    @http.route('/ppm_modules/gettotalbudgetandexpense', type='json', auth='user', methods=['POST'], csrf=False)
    def gettotalbudgetandexpense(self, year):
        querytotalbudget = """
                            SELECT COALESCE(SUM(nilai_anggaran),0) FROM detail_anggaran_perbulan  
                            WHERE EXTRACT(YEAR FROM date_of_fiscal) = %s
                    """
        querytotalexpense = """
                    SELECT COALESCE(SUM(transaction_subtotal),0) FROM 
                    detail_trans_perbudget 
                    WHERE EXTRACT(YEAR FROM transaction_date) = %s
            """
        datatotalexpense = []
        datatotalbudget = []

        query_params = [year]  # Filter by year only
        request.env.cr.execute(querytotalexpense, query_params)
        result_totalexpense = request.env.cr.fetchall()

        request.env.cr.execute(querytotalbudget, query_params)
        result_totalbudget = request.env.cr.fetchall()

        for recordtotalexpense in result_totalexpense:
            datatotalexpense.append({
                'total_expense' : locale.format_string('%.2f', recordtotalexpense[0], grouping=True)
            })
        for recordtotalbudget in result_totalbudget:
            datatotalbudget.append({
                'total_budget': locale.format_string('%.2f', recordtotalbudget[0], grouping=True)
            })

        return{
            'status' : 'success',
            'total_expense' : datatotalexpense,
            'total_budget' : datatotalbudget
        }



