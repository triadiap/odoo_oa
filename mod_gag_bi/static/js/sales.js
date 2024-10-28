odoo.define('mod_gag_bi.sales',function(require){
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

    var SalesBase = AbstractAction.extend({
        template:'sales',
        events: {
                'change .yearname_input' : '_onchangeYear',
                'change .montname_input' : '_onchangeMonth'
        },
        init : function(parent, context){
            this._super(parent, context);
            this.RenderMonthName();
            this.RenderDataYear();

        },
        start: function () {
            this._super.apply(this, arguments);

        },
        _onchangeYear:function(){
                //var getYear = this.$('#RenderDefault').val()
                this.RenderDefault()
        },
        _onchangeMonth:function(){
                //var getMonth = this.$('#RenderDefault').val()
                this.RenderDefault()
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
        },
        RenderDefault:function(){
            this.$('#salestoday').html('1.500.000')
            this.$('#invoicingtoday').html('1.000.000')
            this.$('#incomemonthly').html('1.000.000')
            this.$('#incomeyearly').html('1.000.000')

            var ctxincomepiutang = document.getElementById('incomevspiutang').getContext('2d');
            if (window.incomepiutang) {
                window.incomepiutang.destroy();
            }
            window.incomepiutang = new Chart(ctxincomepiutang, {
                type: 'pie',
                data: {
                    labels: ['Income','Piutang'],  // Dynamic labels
                    datasets: [{
                        label: 'Income VS Piutang',
                        data: [1000000, 500000],  // Dynamic data
                        backgroundColor: [
                            'rgba(0, 255, 0,0.5)',
                            'rgba(200, 200, 200,0.5)',],
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },

                    },
                }
            });

            var ctxinvpo = document.getElementById('invvspo').getContext('2d');
            if (window.invpo) {
                window.invpo.destroy();
            }
            window.invpo = new Chart(ctxinvpo, {
                type: 'pie',
                data: {
                    labels: ['Invoice','PO'],  // Dynamic labels
                    datasets: [{
                        label: 'Invoice VS PO',
                        data: [1500000, 3000000],  // Dynamic data
                        backgroundColor: [
                            'rgba(0, 255, 0,0.5)',
                            'rgba(255, 255, 0,0.5)',],
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },
                    },
                }
            });

            var ctxbarging = document.getElementById('bargingproduction').getContext('2d');
            if (window.barging) {
                window.barging.destroy();
            }
            window.barging = new Chart(ctxbarging, {
                data: {
                    labels: ['LGO-sty','MGO','HGO'],  // Dynamic labels
                    datasets: [{
                        type:'bar',
                        label: 'SMA',
                        data: [0, 1178.28,5171.34],
                    },{
                        type:'bar',
                        label: 'MKA',
                        data: [0, 978.16,1643.31],
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                }
            });
            
            var ctxpayment = document.getElementById('customerpayment').getContext('2d');
            if (window.payment) {
                window.payment.destroy();
            }
            window.payment = new Chart(ctxpayment, {
                data: {
                    labels: ['PT. A','PT. B','PT. C'],  // Dynamic labels
                    datasets: [{
                        type:'bar',
                        label: 'PO',
                        data: [1000000, 1000000,1000000],
                    },{
                        type:'bar',
                        label: 'INVOICE',
                        data: [500000, 500000,0],
                    },{
                        type:'bar',
                        label: 'PIUTANG',
                        data: [500000, 0,0],
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                }
            });
        }            
    })

    core.action_registry.add('sales_base', SalesBase);
    return SalesBase;
})