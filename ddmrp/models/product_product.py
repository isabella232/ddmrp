# Copyright 2020 ForgeFlow S.L. (http://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class Product(models.Model):
    _inherit = "product.product"

    buffer_ids = fields.One2many(
        comodel_name="stock.buffer", string="Stock Buffers", inverse_name="product_id",
    )

    archived_buffer_warning_qty = fields.Integer(
        compute="_compute_archived_buffer_warning_qty", compute_sudo=True
    )

    @api.depends("buffer_ids", "buffer_ids.active")
    def _compute_archived_buffer_warning_qty(self):
        for product in self:
            product.archived_buffer_warning_qty = self.env["stock.buffer"].search_count(
                [
                    ("product_id", "=", product.id),
                    ("item_type", "=", "purchased"),
                    ("active", "=", False),
                ]
            )

    def write(self, values):
        res = super().write(values)
        if values.get("active") is False:
            buffers = self.env["stock.buffer"].search([("product_id", "in", self.ids)])
            buffers.write({"active": False})
        return res
