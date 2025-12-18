from odoo import http
from odoo.http import request

class PrintController(http.Controller):

    @http.route('/print/model_x/<int:doc_id>', type='http', auth='user')
    def print_model_x(self, doc_id, **kwargs):
        pdf = request.env.ref('odm_report_scheduler.report_ticket_action')._render_qweb_pdf([doc_id])[0]
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', 'inline; filename="receipt_note.pdf"')
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)

    @http.route('/report/completion/filters', type='json', auth='user')
    def get_completion_report_filters(self, doc_type_id=None, **kwargs):
        # Initial load: return all document types
        doc_types = request.env['oa.reporting.type'].search_read([], ['id', 'name'])
        
        # If a doc_type_id is provided, return a filtered list of reports
        report_domain = []
        if doc_type_id:
            report_domain.append(('document_type', '=', int(doc_type_id)))
        report_names = request.env['odm.document.configuration'].search_read(report_domain, ['id', 'name'])
        departments = request.env['hr.department'].search_read([], ['id', 'name'])
        return {
            'doc_types': doc_types,
            'report_names': report_names,
            'departments': departments,
        }

    @http.route('/report/completion/get_departments', type='json', auth='user')
    def get_departments_for_report(self, conf_id=None, **kwargs):
        department_obj = request.env['hr.department']
        if conf_id:
            report_config = request.env['odm.document.configuration'].browse(int(conf_id))
            if report_config.department_ids:
                return report_config.department_ids.read(['id', 'name'])
        # If no conf_id or no departments on the config, return all
        return department_obj.search_read([], ['id', 'name'])


    @http.route('/report/completion/data', type='json', auth='user')
    def completion_report_data(self, doc_type_id=None, conf_id=None, department_id=None, **kwargs):
        env = request.env
        submission_obj = env['odm.report.submission']
        
        domain = [('state', 'in', ['pending', 'completed'])]
        if doc_type_id:
            domain.append(('doc_type', '=', int(doc_type_id)))
        if conf_id:
            domain.append(('conf_id', '=', int(conf_id)))
            
        valid_submissions = submission_obj.with_context(skip_custom_search=True).search(domain)

        on_time_count = 0
        late_count = 0

        for submission in valid_submissions:
            if submission.realization_date and submission.deadline_time:
                realization_date_as_date = submission.realization_date
                deadline_time_as_date = submission.deadline_time.date()
                if realization_date_as_date <= deadline_time_as_date:
                    on_time_count += 1
                else:
                    late_count += 1

        return {
            'on_time_reports': on_time_count,
            'late_reports': late_count,
            'total_processed_reports': len(valid_submissions),
        }

    @http.route('/print/external_receipt/<int:doc_id>', type='http', auth='user')
    def print_external_receipt(self, doc_id, **kwargs):
        pdf = request.env.ref('odm_report_scheduler.report_external_receipt')._render_qweb_pdf([doc_id])[0]
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', 'inline; filename="receipt_note.pdf"')
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)