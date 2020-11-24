# Copyright 2020 Camptocamp (https://www.camptocamp.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models

from odoo.addons.queue_job.job import identity_exact


class Buffer(models.Model):
    _inherit = "stock.buffer"

    def cron_actions_job_options(self, only_nfp=False):
        return {
            "identity_key": identity_exact,
            "priority": 15,
            "description": "DDMRP Buffer calculation ({})".format(self.display_name),
        }

    def _register_hook(self):
        self._patch_method(
            "cron_actions",
            self._patch_job_auto_delay(
                "cron_actions", context_key="auto_delay_ddmrp_cron_actions"
            ),
        )
        return super()._register_hook()

    def cron_ddmrp(self, automatic=False):
        return super(
            Buffer, self.with_context(auto_delay_ddmrp_cron_actions=True)
        ).cron_ddmrp(automatic=automatic)
