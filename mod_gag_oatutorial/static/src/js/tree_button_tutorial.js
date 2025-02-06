odoo.define('mod_gag_oatutorial.tree_button_tutorial', function (require) {
    "use strict";
    var core = require('web.core');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var rpc = require('web.rpc');
    var session = require('web.session');  // Import session
    var ActionManager = require('web.ActionManager');  // Import ActionManager

    function getCurrentMenuId() {
        var match = window.location.href.match(/menu_id=(\d+)/);
        return match ? parseInt(match[1], 10) : null;
    }
    function getCurrentModelName() {
        var match = window.location.href.match(/model=([\w\.]+)/);
        return match ? match[1] : null;
    }
    ListController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            var self = this;
            if (this.$buttons && !this.$buttons.find('.o_list_global_button_tutorial').length) {
                var $button = $("<button>", {
                    class: "btn btn-primary o_list_global_button_tutorial",
                    html: '<i class="fa fa-book"></i> Office Automation Tutorial', // Add icon
                    click: function () {
                        var current_menu_id = getCurrentMenuId();
                        if (!current_menu_id) {
                            alert("Current menu ID not found in URL!");
                            return;
                        }
                        rpc.query({
                             model: 'ir.actions.act_window',
                             method: 'search_read',
                             args: [[['res_model', '=', 'oa.management.tutorial']], ['id']],
                             }).then(function (actions) {
                                        if (actions.length > 0) {
                                            var action_id = actions[0].id;
                                            // Open OA Tutorials with filtered menu_id
                                            window.location.href = `/web#action=${action_id}&view_type=list&menu_id=${current_menu_id}`;
                                        } else {
                                            alert("OA Tutorials action not found!");
                                        }
                              }).catch(function (error) {
                                        console.error("RPC Error Fetching Action:", error);
                             });
                    }
                });
                this.$buttons.append($button);
            }
        },
    });
});
