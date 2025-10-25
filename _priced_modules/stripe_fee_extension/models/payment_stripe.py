# -*- coding: utf-8 -*-

from odoo import models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    def _compute_feature_support_fields(self):
        """Override of `payment` to enable additional features."""
        super()._compute_feature_support_fields()
        # Note: support_fees field doesn't exist in Odoo 18
        # Fee support is handled through other mechanisms
        # You can add other Stripe-specific feature support here if needed
