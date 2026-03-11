from odoo import models, api, SUPERUSER_ID
from odoo import registry
from datetime import datetime

class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    def _button_immediate_function(self, function):
        db_name = self.env.cr.dbname
        user_id = self.env.user.id
        modules_data = [
            {
                'name': module.name,
                'old_version': module.installed_version or module.latest_version,
            }
            for module in self
        ]
        try:
            res = super(IrModuleModule, self)._button_immediate_function(function)
            # 🔥 Log SUCCESS
            with registry(db_name).cursor() as new_cr:
                new_env = api.Environment(new_cr, SUPERUSER_ID, {})
                new_cr.execute("SELECT to_regclass('public.module_upgrade_log')")
                if new_cr.fetchone()[0]:
                    for m in modules_data:
                        upgraded_module = new_env['ir.module.module'].search(
                            [('name', '=', m['name'])],
                            limit=1
                        )
                        new_env['module.upgrade.log'].create({
                            'module_name': m['name'],
                            'old_version': m['old_version'],
                            'new_version': upgraded_module.latest_version,
                            'module_summary': upgraded_module.summary,
                            'module_description': upgraded_module.description,
                            'upgraded_by': user_id,
                            'upgrade_datetime': datetime.now(),
                            'status': 'success'
                        })
                    new_cr.commit()
            return res
        except Exception as e:
            raise
