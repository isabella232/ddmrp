# Copyright 2020 Camptocamp (https://www.camptocamp.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models

from odoo.addons.queue_job.job import identity_exact, job_auto_delay


class Buffer(models.Model):
    _inherit = "stock.buffer"

    def cron_actions_job_options(self, only_nfp=False):
        return {
            "identity_key": identity_exact,
            "priority": 15,
            "description": "DDMRP Buffer calculation ({})".format(self.display_name),
        }

    @job_auto_delay(default_channel="root.ddmrp")
    def cron_actions(self, only_nfp=False):
        return super().cron_actions(only_nfp=only_nfp)
