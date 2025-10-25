/** @odoo-module */

import { WebClient } from "@web/webclient/webclient";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { onMounted, onWillStart } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";

patch(WebClient.prototype, {
  setup() {
    super.setup();
    onWillStart(async () => {
      // Ensure proper initialization order
      try {
        await this.env.services.loaded;
      } catch (e) {
        // Services might not be fully loaded yet, continue anyway
      }
    });
    onMounted(() => {
      // Add a small delay to ensure all services are available
      setTimeout(() => {
        this._updateClassList(true);
      }, 100);
    });
  },

  _updateClassList(inHomeMenu) {
    try {
      if (this.hm && this.hm.hasHomeMenu) {
        document.body.classList.remove("ks_menubar_autohide");
        document.body.classList.remove("brightness");

        if (
          document.documentElement.getAttribute("data-drawer-font-style") ===
          "dark"
        ) {
          document.documentElement.setAttribute("data-color-mode", "ks-dark");
        } else if (
          document.documentElement.getAttribute("data-drawer-font-style") ===
          "light"
        ) {
          document.documentElement.setAttribute("data-color-mode", "ks-light");
        }

        // Manage App drawer theme color.
        document.body.style.removeProperty("--body-background");
        document.body.style.removeProperty("--nav-link-color");
        document.body.style.removeProperty("--ks-over-link");

        const menuSystray = document.querySelector(".o_menu_systray");
        if (menuSystray) {
          menuSystray.classList.remove("ks_color_theme_dark_header");
        }

        const ksMenuSystray = document.querySelector(".ks-menu-systray");
        if (ksMenuSystray) {
          ksMenuSystray.classList.remove("ks_color_theme_dark_header");
        }

        const phoneMenuBtns = document.querySelectorAll(
          ".o_main_navbar button.phone-menu-btn, .ks_left_sidebar_panel .ks_app_sidebar .inner-sidebar button.phone-menu-btn"
        );
        phoneMenuBtns.forEach((btn) =>
          btn.classList.remove("ks_color_theme_dark_header")
        );
      } else {
        // Check if device service is available and not mobile
        if (this.env && this.env.device && !this.env.device.isMobile) {
          const mobileToggle = document.querySelector(".o_mobile_menu_toggle");
          if (mobileToggle && mobileToggle.parentElement) {
            mobileToggle.parentElement.classList.add("d-none");
          }
        }

        document.documentElement.setAttribute(
          "data-color-mode",
          session.ks_current_color_mode || "ks-light"
        );
        document.body.classList.add("brightness");

        if (
          session.ks_curved_backend_theme_enter_data &&
          session.ks_curved_backend_theme_enter_data.ks_menubar_autohide
        ) {
          document.body.classList.add("ks_menubar_autohide");
        }

        if (
          session.ks_current_color_mode === "ks-light" &&
          session.ks_color_theme
        ) {
          // Apply Color theme back.
          document.body.style.setProperty(
            "--body-background",
            session.ks_color_theme["body-background"]
          );
          document.body.style.setProperty(
            "--nav-link-color",
            session.ks_color_theme["nav-link-color"]
          );
          document.body.style.setProperty(
            "--ks-over-link",
            session.ks_color_theme["ks-over-link"]
          );
        }

        if (
          session.ks_color_theme &&
          session.ks_color_theme.ks_header_icon_clr
        ) {
          const menuSystray = document.querySelector(".o_menu_systray");
          if (menuSystray) {
            menuSystray.classList.add("ks_color_theme_dark_header");
          }

          const phoneMenuBtns = document.querySelectorAll(
            ".o_main_navbar button.phone-menu-btn, .ks_left_sidebar_panel .ks_app_sidebar .inner-sidebar button.phone-menu-btn"
          );
          phoneMenuBtns.forEach((btn) =>
            btn.classList.add("ks_color_theme_dark_header")
          );
        }
      }
    } catch (error) {
      console.warn("Theme update error:", error);
      // Continue silently if there are any issues
    }
  },
});
