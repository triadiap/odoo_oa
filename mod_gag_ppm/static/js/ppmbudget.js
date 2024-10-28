odoo.define('mod_gag_ppm.ppmbudget',function(require){
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

            },
            init : function(parent, context){
                this._super(parent, context);
                this.RenderDataTable();
                this.RenderPillarName();
            },
            start: function () {
                this._super.apply(this, arguments);

            },

            RenderDataTable:function(){
                $('#my_table').DataTable({
                // DataTable options
                });
            },
            RenderPillarName:function(){
                rpc.query({
                    route:'/my_module/get_data_pillar',
                    params: {}
                }).then((response) => {
                    var pillarname = $('#pillar_name')
                    pillarname.empty()
                    $.each(response, function(index, item){
                        pillarname.append($('<option></option>').attr('value', item.id).text(item.nama_pillar))
//                           console.log(item.nama_pillar)
                    })
                }).catch((error) => {
                    console.error('Error fetching HTML:', error);
                });
            }
    })

    core.action_registry.add('ppm_budgeting_base', PPMBudgetMonitoring);
    return PPMBudgetMonitoring;


})