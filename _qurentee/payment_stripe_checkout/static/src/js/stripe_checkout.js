/** @odoo-module **/

import { loadJS } from "@web/core/assets";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.StripeCheckoutWidget = publicWidget.Widget.extend({
  selector: 'form[provider="stripe_checkout"]',
  events: {
    submit: "_onFormSubmit",
    "click #close-modal": "_onCloseModal",
    "click .stripe_same_page": "_onSamePagePayment",
  },

  /**
   * @override
   */
  init() {
    this._super(...arguments);
    this.stripe = null;
    this.elements = null;
    this.stripe_checkout = undefined;
    this.isProcessing = false;
  },

  /**
   * @override
   */
  async start() {
    await this._super(...arguments);
    this._showLoadingMessage(_t("Loading Stripe JS..."));
    await this._initializeStripe();
  },

  // #=== INITIALIZATION ===#

  /**
   * Initialize Stripe and setup payment elements.
   *
   * @private
   * @return {Promise}
   */
  async _initializeStripe() {
    try {
      this._showLoadingMessage(_t("Initializing Payment..."));

      // Load Stripe.js
      await loadJS("https://js.stripe.com/v3/");

      if (!window.Stripe) {
        throw new Error("Stripe.js failed to load");
      }

      // Get form data
      const formData = this._getFormData();
      const publishableKey = this.el.querySelector(
        'input[name="stripe_checkout_pub_key"]'
      )?.value;

      if (!publishableKey) {
        throw new Error("Stripe publishable key not found");
      }

      // Initialize Stripe
      this.stripe = Stripe(publishableKey);

      // Create payment intent
      const response = await rpc("/create-payment-intent", formData);
      const data = JSON.parse(response);
      const clientSecret = data.clientSecret;

      // Setup Stripe Elements
      const appearance = { theme: "stripe" };
      this.elements = this.stripe.elements({ appearance, clientSecret });

      // Render UI and mount payment element
      await this._renderPaymentUI();
      const paymentElement = this.elements.create("payment");
      paymentElement.mount("#payment-element");

      this._hideLoadingMessage();
    } catch (error) {
      this._hideLoadingMessage();
      this._showErrorDialog(_t("Initialization Error"), error.message);
    }
  },

  /**
   * Render the payment UI modal.
   *
   * @private
   * @return {Promise}
   */
  async _renderPaymentUI() {
    this._showLoadingMessage(_t("Processing..."));

    const modalElement = document.querySelector(".stripe_dropin_modal");
    if (modalElement) {
      // Initialize Bootstrap modal if available
      if (window.bootstrap && window.bootstrap.Modal) {
        const modal = new window.bootstrap.Modal(modalElement, {
          keyboard: false,
          backdrop: "static",
        });
        modal.show();
      } else if (window.$ && window.$.fn.modal) {
        // Fallback to jQuery modal
        window
          .$(modalElement)
          .modal({
            keyboard: false,
            backdrop: "static",
          })
          .modal("show");
      }
    }
  },

  // #=== EVENT HANDLERS ===#

  /**
   * Handle form submission.
   *
   * @private
   * @param {Event} ev
   */
  async _onFormSubmit(ev) {
    ev.preventDefault();
    if (this.isProcessing) return;

    await this._handlePaymentSubmission();
  },

  /**
   * Handle same page payment click.
   *
   * @private
   * @param {Event} ev
   */
  async _onSamePagePayment(ev) {
    ev.preventDefault();
    if (this.isProcessing) return;

    await this._handlePaymentSubmission();
  },

  /**
   * Handle modal close.
   *
   * @private
   * @param {Event} ev
   */
  _onCloseModal(ev) {
    ev.preventDefault();
    console.log("-----Close Stripe Modal---------");
    window.location.reload();
  },

  // #=== PAYMENT PROCESSING ===#

  /**
   * Handle payment submission.
   *
   * @private
   * @return {Promise}
   */
  async _handlePaymentSubmission() {
    if (!this.stripe || !this.elements) {
      this._showErrorDialog(
        _t("Payment Error"),
        _t("Payment system not initialized")
      );
      return;
    }

    try {
      this.isProcessing = true;
      this._setLoadingState(true);

      const { error } = await this.stripe.confirmPayment({
        elements: this.elements,
        confirmParams: {
          return_url: `${window.location.origin}/stripe/payment/status`,
        },
      });

      if (error) {
        if (error.type === "card_error" || error.type === "validation_error") {
          this._showPaymentMessage(error.message);
        } else {
          this._showPaymentMessage(_t("An unexpected error occurred."));
        }
      }
    } catch (error) {
      this._showErrorDialog(_t("Payment Error"), error.message);
    } finally {
      this.isProcessing = false;
      this._setLoadingState(false);
    }
  },

  /**
   * Check payment status from URL parameters.
   *
   * @private
   * @return {Promise}
   */
  async _checkPaymentStatus() {
    if (!this.stripe) return;

    const clientSecret = new URLSearchParams(window.location.search).get(
      "payment_intent_client_secret"
    );

    if (!clientSecret) return;

    try {
      const { paymentIntent } = await this.stripe.retrievePaymentIntent(
        clientSecret
      );

      switch (paymentIntent.status) {
        case "succeeded":
          this._showPaymentMessage(_t("Payment succeeded!"));
          break;
        case "processing":
          this._showPaymentMessage(_t("Your payment is processing."));
          break;
        case "requires_payment_method":
          this._showPaymentMessage(
            _t("Your payment was not successful, please try again.")
          );
          break;
        default:
          this._showPaymentMessage(_t("Something went wrong."));
          break;
      }
    } catch (error) {
      this._showErrorDialog(_t("Status Check Error"), error.message);
    }
  },

  // #=== UI HELPERS ===#

  /**
   * Set loading state for payment button.
   *
   * @private
   * @param {boolean} isLoading
   */
  _setLoadingState(isLoading) {
    const submitButton = document.querySelector("#submit");
    const spinner = document.querySelector("#spinner");
    const buttonText = document.querySelector("#button-text");

    if (submitButton) {
      submitButton.disabled = isLoading;
    }

    if (spinner) {
      spinner.classList.toggle("hidden", !isLoading);
    }

    if (buttonText) {
      buttonText.classList.toggle("hidden", isLoading);
    }

    // Also handle the main payment button
    const paymentButton = document.querySelector("#o_payment_form_pay");
    if (paymentButton) {
      paymentButton.disabled = isLoading;
    }
  },

  /**
   * Show payment message to user.
   *
   * @private
   * @param {string} messageText
   */
  _showPaymentMessage(messageText) {
    const messageContainer = document.querySelector("#payment-message");

    if (messageContainer) {
      messageContainer.classList.remove("hidden");
      messageContainer.textContent = messageText;

      setTimeout(() => {
        messageContainer.classList.add("hidden");
        messageContainer.textContent = "";
      }, 4000);
    }
  },

  /**
   * Show loading message with block UI.
   *
   * @private
   * @param {string} message
   */
  _showLoadingMessage(message) {
    // Use modern approach or fallback to blockUI if available
    if (this.call && this.call("ui", "block")) {
      this.call("ui", "block");
    } else if (window.$ && window.$.blockUI) {
      window.$.blockUI({
        message: `<h2 class="text-white">
                    <img src="/payment_stripe_checkout/static/src/img/spinner.gif" 
                         class="fa-pulse" style="height:100px;"/>
                    <br />${message}
                </h2>`,
        css: { border: "0", backgroundColor: "" },
        overlayCSS: { opacity: "0.9" },
      });
    }
  },

  /**
   * Hide loading message.
   *
   * @private
   */
  _hideLoadingMessage() {
    if (this.call && this.call("ui", "unblock")) {
      this.call("ui", "unblock");
    } else if (window.$ && window.$.unblockUI) {
      window.$.unblockUI();
    }
  },

  /**
   * Show error dialog to user.
   *
   * @private
   * @param {string} title
   * @param {string} message
   */
  _showErrorDialog(title, message) {
    this._hideLoadingMessage();

    if (this.call && this.call("dialog", "add")) {
      this.call("dialog", "add", ConfirmationDialog, {
        title: _t("Error: ") + title,
        body: message || "",
        confirmLabel: _t("Ok"),
        confirm: () => {},
        cancel: () => {},
      });
    } else {
      // Fallback to alert
      alert(`${title}: ${message}`);
    }
  },

  /**
   * Get form data as object.
   *
   * @private
   * @return {Object}
   */
  _getFormData() {
    const data = {};
    const inputs = this.el.querySelectorAll('input[type="hidden"]');

    inputs.forEach((input) => {
      if (input.name && input.value) {
        data[input.name] = input.value;
      }
    });

    return data;
  },
});
