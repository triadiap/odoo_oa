odoo.define('mod_gag_bi.ppmbudget',function(require){
    "use.strict";

    var AbstractAction = require('web.AbstractAction')
    var core = require('web.core')
    var ajax = require('web.ajax')
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var NotificationService = require('web.NotificationService');
    var Class = require('web.Class');
    var ServicesMixin = require('web.ServicesMixin');
    var _t = core._t;

    var PPMBudgetMonitoring = AbstractAction.extend({
            template:'Ppmbudgeting',
            events: {
                'change .monthname_input' :'_onchangeMonth',
                'change .yearname_input' : '_onchangeYear'
            },
            init : function(parent, context){
                this._super(parent, context);
                this.RenderMonthName();
                this.RenderDataYear();
            },

            start: function () {
                this._super.apply(this, arguments);
                this.load_cards_data();
                this.production_barging_cards();

            },
            production_barging_cards:function(){
                var self = this
                rpc.query({
                    route:'/barging_module/get_production_barging_cards',
                    params: {}
                }).then((response) => {
                    if(response.status = 'success'){
                         self.$('#productionbargingboard').html("");
                         self.$('#productionbargingboard').html(response.productionbargingchart);
                         self.gettotalproductionpermonth();
                    }
                }).catch((error) => {
                    console.error('Error fetching HTML:', error);
                });
            },
            gettotalproductionpermonth:function(){
                var self = this
                var year = this.$('#year_name').val()
                var month = this.$('#month_name').val()
                rpc.query({
                    route:'/barging_module/production_output_chart',
                    params: {
                        'year' : year,
                        'month' : month
                    }
                }).then((response) => {
                    if(response.status = 'success'){
                            var ctx = document.getElementById('prodbargingchart').getContext('2d');
                            if (window.ProdBargingChart) {
                                window.ProdBargingChart.destroy();
                            }
                            window.ProdBargingChart = new Chart(ctx,{
                                    type: 'bar',
                                    data: {
                                        labels: response.labels,
                                        datasets: response.datasets
                                    },
                                    options:{
                                        scales: {
                                            x: {
                                                beginAtZero: true,
                                                title: {
                                                    display: true,
                                                    text: 'Date'
                                                }
                                            },
                                            y: {
                                                beginAtZero: true,
                                                title: {
                                                    display: true,
                                                    text: 'Quantity'
                                                }
                                            }
                                        },
                                        plugins: {
                                            legend: {
                                                display: true,
                                                position: 'top'
                                            }
                                        }
                                    }
                                })
                    }
                }).catch((error) => {
                    console.error('Error fetching HTML:', error);
                });
            },
            _onchangeYear:function(){
                 var getYear = this.$('#year_name').val()
                 console.log(getYear)
            },
            _onchangeMonth:function(){
                 var getMonth = this.$('#month_name').val()
                 console.log(getMonth)
            },
            load_cards_data: function () {
                var self = this
                rpc.query({
                    route:'/barging_module/get_cards_data',
                    params: {}
                }).then((response) => {
                    if(response.status = 'success'){
                         self.$('#cardlist').html("");
                         self.$('#cardlist').html(response.card_lists);
                         kode = response.id
                         kode.forEach(function (idvendor){
                            self.getPlanActualProduction(idvendor)
                         });
                    }
                }).catch((error) => {
                    console.error('Error fetching HTML:', error);
                });
            },
            getPlanActualProduction: function(idvendor){
                 var tahun = this.$('#year_name').val()
                 var bulan = this.$('#month_name').val()
                 var ProductionData = {
                        'idvendor': idvendor,
                        'tahun' : tahun,
                        'bulan' : bulan
                    };
                    this._rpc({
                        route: '/barging_module/get_production_data',
                        params: ProductionData,
                    }).then(function (result) {
                        if (result.success) {
                            var ctx = document.getElementById('bichart_'+result.vendorid).getContext('2d');
                            var myBarChart = new Chart(ctx,{
                                    type: 'bar',
                                    data: {
                                        labels: result.labels, // X-axis labels
                                        datasets: result.datasets // Datasets array
                                    },
                                    options:{
                                        scales: {
                                            x: {
                                                beginAtZero: true,
                                                title: {
                                                    display: true,
                                                    text: 'Date'
                                                }
                                            },
                                            y: {
                                                beginAtZero: true,
                                                title: {
                                                    display: true,
                                                    text: 'Quantity'
                                                }
                                            }
                                        },
                                        plugins: {
                                            legend: {
                                                display: true,
                                                position: 'top'
                                            }
                                        }
                                    }
                                })
                        } else {
                            alert('Error: ' + result.message);
                        }
                    }).catch(function (error) {
                        console.error('Submission error:', error);
                    });
            },
            RenderMonthName:function(){
                 rpc.query({
                    route:'/barging_module/get_data_month',
                    params: {}
                }).then((response) => {
                    var monthname = $('#month_name')
                    monthname.empty()
                    $.each(response, function(index, item){
                        monthname.append($('<option></option>').attr('value', item.id).text(item.name))
                    })
                }).catch((error) => {
                    console.error('Error fetching HTML:', error);
                });
            },
            RenderDataYear:function(){
                rpc.query({
                    route:'/barging_module/get_data_year',
                    params: {}
                }).then((response) => {
                    var yearname = $('#year_name')
                    yearname.empty()
                    $.each(response, function(index, item){
                        yearname.append($('<option></option>').attr('value', item.id).text(item.name))
                    })
                }).catch((error) => {
                    console.error('Error fetching HTML:', error);
                });
            }
    })

    core.action_registry.add('ppm_budgeting_base', PPMBudgetMonitoring);
    return PPMBudgetMonitoring;


})