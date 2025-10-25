from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def create(self, vals):
        line = super().create(vals)
        line._auto_create_sov()
        return line

    def write(self, vals):
        res = super().write(vals)
        for line in self:
            line._auto_create_sov()
        return res

    def _auto_create_sov(self):
        for line in self:
            # Create or update sale.sov record (actual SOV data)
            sov_model = self.env["sale.sov"]
            sov_line = sov_model.search(
                [
                    ("sale_id", "=", line.order_id.id),
                    ("product_id", "=", line.product_id.id),
                ],
                limit=1,
            )
            sov_vals = {
                "name": line.product_id.display_name or "No Description",
                "sale_id": line.order_id.id,
                "product_id": line.product_id.id,
                "qty": line.product_uom_qty,
                "unit_price": line.price_unit,
                "unit_cost": line.product_id.standard_price or 0.0,
                "revenue": line.price_subtotal,
                "planned_expenses": 0.0,
            }
            if sov_line:
                sov_line.write(sov_vals)
            else:
                sov_line = sov_model.create(sov_vals)

            # Don't automatically create commission.sale.sov records
            # Those should be created manually in the commission process
