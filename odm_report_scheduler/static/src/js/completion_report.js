odoo.define('odm_report_scheduler.dashboard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var CompletionDashboard = AbstractAction.extend({
        template: 'CompletionReportDashboard',
        
        events: {
            'change #doc_type_filter': '_onDocTypeChange',
            'change #report_name_filter': '_onReportNameChange',
            'change #department_filter': '_onDepartmentChange',
        },

        init: function(parent, action) {
            this._super(parent, action);
            this.dashboard_data = {};
            this.myChart = null;
        },

        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                var def1 = self._fetchInitialFilters();
                var def2 = self._fetchDashboardData();
                return Promise.all([def1, def2]);
            });
        },

        start: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                setTimeout(function() {
                    self._renderDashboard();
                }, 0);
            });
        },
        
        _fetchInitialFilters: function() {
            var self = this;
            return rpc.query({
                route: '/report/completion/filters'
            }).then(function(data) {
                self.initial_filters = data;
            });
        },

        _fetchDashboardData: function (filters) {
            var self = this;
            return rpc.query({
                route: '/report/completion/data',
                params: filters || {}
            }).then(function (data) {
                self.dashboard_data = data;
            });
        },
        
        _renderDashboard: function() {
            if (!this.initial_filters_rendered) {
                this._populateSelect(this.$('#doc_type_filter'), this.initial_filters.doc_types, "All Document Types");
                this._populateSelect(this.$('#report_name_filter'), this.initial_filters.report_names, "All Report Names");
                this._populateSelect(this.$('#department_filter'), this.initial_filters.departments, "All Departments");
                this.initial_filters_rendered = true;
            }
            this.$('.display-4').eq(0).text(this.dashboard_data.total_processed_reports);
            this.$('.display-4').eq(1).text(this.dashboard_data.on_time_reports);
            this.$('.display-4').eq(2).text(this.dashboard_data.late_reports);
            this._renderChart();
        },
        
        _populateSelect: function($select, items, default_option_text, current_val) {
            $select.empty();
            $select.append($('<option>', { value: "", text: default_option_text }));
            items.forEach(function(item) {
                $select.append($('<option>', { value: item.id, text: item.name }));
            });
            if (current_val) {
                $select.val(current_val);
            }
        },
        
        _renderChart: function() {
            var chartDom = this.$('#completion_chart')[0];
            if (chartDom) {
                if (!this.myChart) { this.myChart = echarts.init(chartDom); }
                var option = {
                    tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
                     series: [{
                        name: 'Report Status', type: 'pie', radius: ['50%', '70%'],
                        data: [
                            {value: this.dashboard_data.on_time_reports, name: 'On-Time Reports', itemStyle: { color: '#5cb85c' }},
                            {value: this.dashboard_data.late_reports, name: 'Late Reports', itemStyle: { color: '#d9534f' }}
                        ]
                    }]
                };
                this.myChart.setOption(option, true);
            }
        },

        _updateDashboard: function() {
            var self = this;
            var filters = {
                doc_type_id: this.$('#doc_type_filter').val(),
                conf_id: this.$('#report_name_filter').val(),
                department_id: this.$('#department_filter').val(),
            };
            this._fetchDashboardData(filters).then(function() {
                self._renderDashboard();
            });
        },

        _onDocTypeChange: function(e) {
            var self = this;
            var doc_type_id = $(e.currentTarget).val();
            // Reset children
            this._populateSelect(this.$('#department_filter'), [], "All Departments");
            
            rpc.query({
                route: '/report/completion/filters',
                params: {doc_type_id: doc_type_id}
            }).then(function(data) {
                self._populateSelect(self.$('#report_name_filter'), data.report_names, "All Report Names");
                self._updateDashboard();
            });
        },

        _onReportNameChange: function(e) {
            var self = this;
            var conf_id = $(e.currentTarget).val();

            rpc.query({
                route: '/report/completion/get_departments',
                params: {conf_id: conf_id}
            }).then(function(data) {
                self._populateSelect(self.$('#department_filter'), data, "All Departments");
                self._updateDashboard();
            });
        },

        _onDepartmentChange: function() {
            this._updateDashboard();
        }
    });

    core.action_registry.add('completion_report_dashboard', CompletionDashboard);

    return CompletionDashboard;
});