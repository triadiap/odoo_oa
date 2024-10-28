odoo.define('mod_gag_ppm.dashboard',function(require){
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
                'click .frmSubmission': '_frmSubmission',
                'click .submit_button': '_onSubmit',
                'click .btnAlert': 'shoNotification',
                'click .btnDialog': 'shoNotification2',
                'click .btnRestApi' : '_CallRestAPI',
//                'click .menuitem' : '_attachEventHandlers',
            },
            init : function(parent, context){
                this._super(parent, context);

            },
            start: function () {
                this._super.apply(this, arguments);
                this.CallMenus()
                this._attachEventHandlers()
            },
            _attachEventHandlers: function () {
                 $(document).ready(function(){
                    $().ready(function() {
                        $('body').on('click','.item',function(event){
                               event.preventDefault();
                               var value = $(this).closest('li').attr('data-id')
                               rpc.query({
                                    route:value,
                                    params:{
                                        'value' : parseInt(value)
                                    }
                               }).then(function(responses){
                                    this.$('#my_div').html("");
                                    console.log(responses)
                                    this.$('#my_div').html(responses.message);
                               }).catch(function(error){
                                    Swal.fire({
                                    title: "Error",
                                    text: error,
                                    icon: "error"
                                    });
                               })
                        })
                    })
                 })
            },
            CallMenus : function(){
                rpc.query({
                    route:'/my_module/listofmenucall',
                    params:{}
                 }).then(function(response){
                    this.$('#listofmenu').html(response)
                }).catch(function(error){
                     console.log(error)
                 })
            },
            _CallRestAPI : function(){
                rpc.query({
                    route: '/my_module/restapicall',
                    params: {}
                }).then(function (result) {
                    console.log('API Data:', result);
                    if (result.error) {
                        alert('Error: ' + result.error);
                    } else {
                        // Process the result from the external API
                        console.log(result);
                    }
                }).catch(function (error) {
                    console.error('Failed to fetch data:', error);
                });
            },
            _frmSubmission : function(){
                 this.$('#my_div').html("");
                rpc.query({
                route: '/user_input/get_html',
                params:{}
                }).then((response) => {
                    this.$('#my_div').html(response.message);
                }).catch((error) => {
                    console.error('Error fetching HTML:', error);
                })
            },
            _fetchDataAndCreateTable: function (event) {
                event.preventDefault();
                rpc.query({
                route: '/user_input/get_html',
                params: {}
                }).then((response) => {
                    this.$('#my_div').html(response.message);
                }).catch((error) => {
                    console.error('Error fetching HTML:', error);
                });
            },
            _onSubmit: function (ev) {
                ev.preventDefault();
                    var formData = {
                        'name': this.$('#name').val(),
                        'address': this.$('#address').val(),
                    };

                    this._rpc({
                        route: '/user_input/submit_user_input',
                        params: formData,
                    }).then(function (result) {
                        if (result.success) {
                            alert('Record created successfully!');
                        } else {
                            alert('Error: ' + result.error);
                        }
                    }).catch(function (error) {
                        console.error('Submission error:', error);
                    });
            },
            _onSubmit2:function(ev){
                 ev.preventDefault();
                var self = this;
                self.shoNotification2()
            },
            shoNotification:function(){
                    rpc.query({
                        route : '/my_module/get_html_content',
                        params : {}
                    })
                    .then(function (response) {
                            Swal.fire({
                            title: "Good job!",
                            text: response.message,
                              icon: "success"
                            });
                    })
             },
             shoNotification2:function(){
                    rpc.query({
                        route : '/my_module/get_html_content',
                        params : {}
                    })
                    .then(function (response) {
                            const swalWithBootstrapButtons = Swal.mixin({
                             customClass: {
                                confirmButton: "btn btn-success",
                                cancelButton: "btn btn-danger"
                              },
                              buttonsStyling: false
                            });
                            swalWithBootstrapButtons.fire({
                              title: "Are you sure to revert?",
                              text: "You won't be able to revert this!",
                              icon: "warning",
                              showCancelButton: true,
                              confirmButtonText: "Yes, delete it!",
                              cancelButtonText: "No, cancel!",
                              reverseButtons: true
                            }).then((result) => {
                              if (result.isConfirmed) {
                                swalWithBootstrapButtons.fire({
                                  title: "Deleted!",
                                  text: "Your file has been deleted.",
                                  icon: "success"
                                });
                              } else if (
                                /* Read more about handling dismissals below */
                                result.dismiss === Swal.DismissReason.cancel
                              ) {
                                swalWithBootstrapButtons.fire({
                                  title: "Cancelled",
                                  text: "Your imaginary file is safe :)",
                                  icon: "error"
                                });
                              }
                            });
                    })
             },

    })

    core.action_registry.add('employee_dashboard_base', EmployeeDashboardBase);
    return EmployeeDashboardBase;


})