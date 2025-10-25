/** @odoo-module */

import { Component, useRef, useState, useExternalListener } from "@odoo/owl";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

/**
 * Custom dropdown menu component for Odoo 18
 * @extends Component
 */
export class KsDropdownMenu extends Component {
  static template = "ks_curved_backend_theme_enter.KsGenericDropdownMenu";
  static components = { DropdownItem };
  static props = {
    icon: { type: String, optional: true },
    items: { type: Array, optional: true },
    title: { type: String, optional: true },
    closeOnSelected: { type: Boolean, optional: true },
    ks_all_data: { type: Object, optional: true },
    slots: { type: Object, optional: true },
  };
  static defaultProps = {
    items: [],
    closeOnSelected: true,
  };

  setup() {
    this.dropdownMenu = useRef("dropdown");
    this.state = useState({ open: false });

    useExternalListener(window, "click", this._onWindowClick, true);
    useExternalListener(window, "keydown", this._onWindowKeydown);
  }

  //---------------------------------------------------------------------
  // Getters
  //---------------------------------------------------------------------

  /**
   * In desktop, by default, we do not display a caret icon next to the
   * dropdown.
   * @returns {boolean}
   */
  get displayCaret() {
    return false;
  }

  /**
   * In mobile, by default, we display a chevron icon next to the dropdown
   * button. Note that when 'displayCaret' is true, we display a caret
   * instead of a chevron, no matter the value of 'displayChevron'.
   * @returns {boolean}
   */
  get displayChevron() {
    return this.env.device.isMobile;
  }

  /**
   * Can be overriden to force an icon on an inheriting class.
   * @returns {string} Font Awesome icon class
   */
  get icon() {
    return this.props.icon;
  }

  /**
   * Meant to be overriden to provide the list of items to display.
   * @returns {Object[]}
   */
  get items() {
    return this.props.items;
  }

  /**
   * @returns {string}
   */
  get title() {
    return this.props.title;
  }

  //---------------------------------------------------------------------
  // Handlers
  //---------------------------------------------------------------------

  /**
   * @private
   * @param {KeyboardEvent} ev
   */
  _onButtonKeydown(ev) {
    switch (ev.key) {
      case "ArrowLeft":
      case "ArrowRight":
      case "ArrowUp":
      case "ArrowDown":
        const firstItem = this.el.querySelector(".dropdown-item");
        if (firstItem) {
          ev.preventDefault();
          firstItem.focus();
        }
    }
  }

  /**
   * @private
   * @param {OwlEvent} ev
   */
  _onItemSelected(/* ev */) {
    if (this.props.closeOnSelected) {
      this.state.open = false;
    }
  }

  /**
   * @private
   * @param {MouseEvent} ev
   */
  _onWindowClick(ev) {
    if (
      this.state.open &&
      !this.el.contains(ev.target) &&
      !this.el.contains(document.activeElement)
    ) {
      if (document.body.classList.contains("modal-open")) {
        // retrieve the active modal and check if the dropdown is a child of this modal
        const modal = document.querySelector(
          "body > .modal:not(.o_inactive_modal)"
        );
        if (modal && !modal.contains(this.el)) {
          return;
        }
        const owlModal = document.querySelector(
          "body > .o_dialog > .modal:not(.o_inactive_modal)"
        );
        if (owlModal && !owlModal.contains(this.el)) {
          return;
        }
      }
      // check for an active open bootstrap calendar like the filter dropdown inside the search panel)
      if (document.querySelector("body > .bootstrap-datetimepicker-widget")) {
        return;
      }
      this.state.open = false;
    }
  }

  /**
   * @private
   * @param {KeyboardEvent} ev
   */
  _onWindowKeydown(ev) {
    if (this.state.open && ev.key === "Escape") {
      this.state.open = false;
    }
  }

  /**
   * Toggle dropdown state
   */
  toggle() {
    this.state.open = !this.state.open;
  }
}
