/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { loadJS } from "@web/core/assets";
import paymentForm from "@payment/js/payment_form";

paymentForm.include({
  // #=== PAYMENT FLOW ===#

  /**
   * Redirect the customer to Stripe Checkout for payment processing.
   *
   * @override method from @payment/js/payment_form
   * @private
   * @param {string} providerCode - The code of the selected payment option's provider.
   * @param {number} paymentOptionId - The id of the selected payment option.
   * @param {string} paymentMethodCode - The code of the selected payment method, if any.
   * @param {object} processingValues - The processing values of the transaction.
   * @return {void}
   */
  _processRedirectFlow(
    providerCode,
    paymentOptionId,
    paymentMethodCode,
    processingValues
  ) {
    if (providerCode !== "stripe_checkout") {
      return this._super(...arguments);
    }

    // Ensure Stripe.js is loaded before attempting to redirect
    this._loadStripeJS(processingValues.publishable_key)
      .then(() => {
        const stripe = Stripe(processingValues.publishable_key);

        // Redirect to Stripe Checkout
        stripe
          .redirectToCheckout({
            sessionId: processingValues.session_id,
          })
          .then((result) => {
            if (result.error) {
              // Handle any errors that occur during redirect
              this._displayErrorDialog(
                _t("Payment processing failed"),
                result.error.message
              );
              this._enableButton();
            }
          })
          .catch((error) => {
            // Handle unexpected errors
            this._displayErrorDialog(
              _t("Payment processing failed"),
              error.message || _t("An unexpected error occurred")
            );
            this._enableButton();
          });
      })
      .catch((error) => {
        // Handle Stripe.js loading errors
        this._displayErrorDialog(
          _t("Payment system unavailable"),
          _t("Unable to load Stripe payment system")
        );
        this._enableButton();
      });
  },

  // #=== UTILITY METHODS ===#

  /**
   * Load Stripe.js library if not already loaded.
   *
   * @private
   * @param {string} publishableKey - The Stripe publishable key to validate loading.
   * @return {Promise} Promise that resolves when Stripe.js is loaded.
   */
  async _loadStripeJS(publishableKey) {
    if (window.Stripe) {
      return Promise.resolve();
    }

    try {
      await loadJS("https://js.stripe.com/v3/");

      // Verify Stripe is properly loaded
      if (!window.Stripe) {
        throw new Error("Stripe.js failed to load properly");
      }

      return Promise.resolve();
    } catch (error) {
      return Promise.reject(error);
    }
  },
});
