odoo.define('mod_gag_utm.custom_graph', function (require) {
    "use strict";

    console.log('Custom Graph JS Loaded');  // Add this line to check
    var GraphView = require('web.GraphView');
    GraphView.include({
        renderChart: function () {
            console.log('Rendering chart with forced type: bar'); // Debugging
            this.controllerParams.chartType = 'bar'; // Force chart type to bar
            this._super.apply(this, arguments);
        }
    });
});