odoo.define('mod_gag_utm.partbyequipment', function(require){
     'use strict';

    var FormController = require('web.FormController');
    var rpc = require('web.rpc');

    $(document).ready(function(){
      FormController.include({
            _onDropdownChange: function (event){
                 var self = this;
                var dropdown_value = this.renderer.state.data.equipment_id;
                if (dropdown_value) {
                    rpc.query({
                        model: 'maintenance.equipment',
                        method: 'search_read',
                        args: [[['id', '=', dropdown_value]], ['name', 'serial_no', 'model']],
                    }).then(function (result) {
                        if (result.length > 0) {
                            console.log('Fetched Data:', result);
                        } else {
                            console.log('No Data Found for the selected value.');
                        }
                    }).catch(function (error) {
                        console.error('Error fetching data:', error);
                    });
                } else {
                    console.log('Dropdown value is empty.');
                }
            },
            _render: function () {
                this._super.apply(this, arguments);
                var $dropdown = this.$el.find('select[name="equipment_id"]');
                $dropdown.change(this._onDropdownChange.bind(this));
        }
     })
    });


});