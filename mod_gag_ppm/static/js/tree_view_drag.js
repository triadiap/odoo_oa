odoo.define('mod_gag_ppm.DraggableTreeView', function (require) {
    "use strict";

    const ListController = require('web.ListController');
    const ListView = require('web.ListView');
    const viewRegistry = require('web.view_registry');

    const DraggableListController = ListController.extend({
        start: function () {
            this._super.apply(this, arguments);
            this._initSortable();
        },

        _initSortable: function () {
            const tbody = this.$el.find('.o_list_view tbody')[0];
            if (tbody) {
                new Sortable(tbody, {
                    animation: 150,
                    handle: '.o_data_row',
                    onEnd: (event) => this._updateSequence(event),
                });
            }
        },

        _updateSequence: function (event) {
            const ids = [];
            const rows = this.$el.find('.o_list_view tbody tr');
            rows.each(function () {
                ids.push($(this).data('id'));
            });

            this._rpc({
                model: this.modelName,
                method: 'update_sequence',
                args: [ids],
            }).then(() => {
                this.reload();
            });
        },
    });

    const DraggableListView = ListView.extend({
        config: Object.assign({}, ListView.prototype.config, {
            Controller: DraggableListController,
        }),
    });

    viewRegistry.add('draggable_tree', DraggableListView);
});
