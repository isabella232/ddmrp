# Copyright 2019-20 ForgeFlow S.L. (http://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, SUPERUSER_ID


class StockMove(models.Model):
    _inherit = "stock.move"

    # TODO remove override, either use hooks, either fix job_auto_delay
    def _update_ddmrp_nfp(self):
        if self.env.context.get("no_ddmrp_auto_update_nfp"):
            return True
        # Find buffers that can be affected. `out_buffers` will see the move as
        # outgoing and `in_buffers` as incoming.
        out_buffers = in_buffers = self.env["stock.buffer"]
        for move in self:
            out_buffers |= move.mapped("product_id.buffer_ids").filtered(
                lambda buffer: (
                    move.location_id.is_sublocation_of(buffer.location_id)
                    and not move.location_dest_id.is_sublocation_of(buffer.location_id)
                )
            )
            in_buffers |= move.mapped("product_id.buffer_ids").filtered(
                lambda buffer: (
                    not move.location_id.is_sublocation_of(buffer.location_id)
                    and move.location_dest_id.is_sublocation_of(buffer.location_id)
                )
            )

        for buffer in out_buffers.with_context(no_ddmrp_history=True):
            # TODO implement 'su' in jobs
            buffer.with_user(SUPERUSER_ID).with_delay(
                **buffer.cron_actions_job_options(only_nfp="out")
            ).job_cron_actions(only_nfp="out")

        for buffer in in_buffers.with_context(no_ddmrp_history=True):
            buffer.with_user(SUPERUSER_ID).with_delay(
                **buffer.cron_actions_job_options(only_nfp="in")
            ).job_cron_actions(only_nfp="in")
