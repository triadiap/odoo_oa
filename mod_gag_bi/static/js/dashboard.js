odoo.define('mod_gag_bi.dashboard',function(require){
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

    var EmployeeDashboardBase = AbstractAction.extend({
            template:'MyDashboard',
            events: {
                 'change .yearname_input' : '_onchangeYear'
            },
            init : function(parent, context){
                this._super(parent, context);
                this.RenderDataYear();

            },
            start: function () {
                this._super.apply(this, arguments);

            },
            _onchangeYear:function(){
                 var getYear = this.$('#year_name').val()
                 this.RenderPillarCards()
                 this.RenderPercentageOfBudgetChart(getYear)
                 this.RenderBudgetVsExpense(getYear)
                 this.RenderTotalBudgetAndExpense(getYear)
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
                    this._onchangeYear()
                }).catch((error) => {
                    console.error('Error fetching HTML:', error);
                });
            },
            RenderPillarCards:function(){
                var getYear = this.$('#year_name').val()
                rpc.query({
                    route:'/ppm_modules/get_pillar_cards',
                    params:{},
                }).then((response) => {
                   if(response.status = 'success'){
                        self.$('#pillarcards').html("");
                        self.$('#pillarcards').html(response.card_lists);
                        this.RenderBudgetInfoPerPillar(response.id, getYear)
                   }
               }).catch((error)=> {
                    console.error('Error fetching HTML:', error);
               })
            },
            RenderPercentageOfBudgetChart:function(yearnumber){
                    rpc.query({
                    route:'/ppm_modules/get_percentagebypillar_chart',
                    params:{
                        'year' : yearnumber,
                    },
                }).then((response) => {
                   if(response.status = 'success'){
                        var ctx = document.getElementById('budgetpercentage').getContext('2d');
                       // Destroy the previous chart instance if it exists
                        if (window.doughnutChart) {
                            window.doughnutChart.destroy();
                        }
                        window.doughnutChart = new Chart(ctx, {
                            type: 'doughnut',
                            data: {
                                labels: response.labels,  // Dynamic labels
                                datasets: [{
                                    label: 'Budget Allocation',
                                    data: response.data,  // Dynamic data
                                    backgroundColor: response.backgroundColors,  // Dynamic background colors
                                    borderColor: response.borderColors,  // Dynamic border colors
                                    borderWidth: response.borderWidths  // Dynamic border widths
                                }]
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                responsive: true,
                                plugins: {
                                    legend: {
                                        position: 'right',
                                    },

                                },
                                layout: {
                                        padding: {
                                            left: 0,
                                            right: 0,
                                            top: 20,
                                            bottom: 0
                                        }
                                    }

                            }
                        });
                   }
               }).catch((error)=> {
                    console.error('Error fetching HTML:', error);
               })
            },
            RenderBudgetVsExpense:function(yearnumber){
                rpc.query({
                    route:'/ppm_modules/getmonthlyvsbudgetchartdata',
                    params:{
                        'year' : yearnumber,
                    },
                }).then((response) => {
                   if(response.status = 'success'){
                      var ctx = document.getElementById('monthlybudgetexpensechart').getContext('2d');
                        if (window.lineChart) {
                            window.lineChart.destroy();
                        }
                      window.lineChart = new Chart(ctx, {
                            type: 'line',
                            data: response.dataset,
                            options: {
                                responsive: true,
                                maintainAspectRatio:false,
                                title: {
                                        display: true,
                                        text: `Budget vs Expenses vs Balance (${yearnumber})`
                                    }
                            }
                        });
                   }
               }).catch((error)=> {
                    console.error('Error fetching HTML:', error);
               })
            },
            RenderBudgetInfoPerPillar:function(id, yearnumber){
                rpc.query({
                    route:'/ppm_modules/getbudgetperpillardetailinfo',
                    params:{
                        'year' : yearnumber,
                        'idpillar' : id
                    },
                }).then((response) => {
                   if(response.status = 'success'){
                     $.each(response.data, function(key, val){
                        document.getElementById("delivered_"+val.idpillar).textContent = "";
                        document.getElementById("delivered_"+val.idpillar).textContent = val.percentage+"%";
                        document.getElementById("expense"+val.idpillar).textContent = "";
                        document.getElementById("expense"+val.idpillar).textContent = "Expense:"+val.total_expense+" IDR";
                        document.getElementById("budget"+val.idpillar).textContent = "";
                        document.getElementById("budget"+val.idpillar).textContent = "Budget:"+val.total_budget+" IDR";
                     })
                   }
               }).catch((error)=> {
                    console.error('Error fetching HTML:', error);
               })
            },
            RenderTotalBudgetAndExpense : function(yearnumber){
                 rpc.query({
                    route:'/ppm_modules/gettotalbudgetandexpense',
                    params:{
                        'year' : yearnumber
                    },
                }).then((response) => {
                   if(response.status = 'success'){
                        document.getElementById("totalbudget").textContent = "";
                        document.getElementById("totalbudget").textContent = response.total_budget[0].total_budget+" IDR";
                        document.getElementById("totalexpense").textContent = "";
                        document.getElementById("totalexpense").textContent = response.total_expense[0].total_expense+" IDR";
                   }
               }).catch((error)=> {
                    console.error('Error fetching HTML:', error);
               })
            }
    })

    core.action_registry.add('employee_dashboard_base', EmployeeDashboardBase);
    return EmployeeDashboardBase;


})