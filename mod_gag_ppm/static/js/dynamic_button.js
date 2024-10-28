odoo.define('mod_gag_ppm.dynamic_button', function (require) {
    'use strict';

    var FormView = require('web.FormView');
    var core = require('web.core');

    // Extend FormView to modify button text
    FormView.include({
        render_buttons: function ($node) {
            this._super($node);
            this._update_button_text();
        },

        _update_button_text: function () {
            var self = this;
            var $button = this.$el.find('.o_dynamic_button');
            if ($button.length) {
                var buttonText = self.model.get(this.handle).data.button_label;
                $button.find('.o_button_text').text(buttonText || 'Default Text');
            }
        },
    });
});
