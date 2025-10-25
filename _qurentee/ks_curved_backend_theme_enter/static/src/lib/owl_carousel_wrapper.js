/** @odoo-module */

import { loadJS } from "@web/core/assets";

/**
 * OWL Carousel wrapper for Odoo 18
 * This module ensures jQuery is available before loading OWL Carousel
 */

let owlCarouselLoaded = false;

export async function loadOwlCarousel() {
  if (owlCarouselLoaded) {
    return Promise.resolve();
  }

  // Ensure jQuery is available globally
  if (typeof window.$ === "undefined" && typeof window.jQuery === "undefined") {
    // Load jQuery if not available
    await loadJS("/web/static/lib/jquery/jquery.js");
  }

  // Make sure jQuery is available as $ and jQuery
  if (typeof window.$ === "undefined") {
    window.$ = window.jQuery;
  }
  if (typeof window.jQuery === "undefined") {
    window.jQuery = window.$;
  }

  // Now load OWL Carousel with jQuery available
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src =
      "/ks_curved_backend_theme_enter/static/src/lib/owl.carousel.min.js";
    script.onload = () => {
      owlCarouselLoaded = true;
      resolve();
    };
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

export function initializeOwlCarousel(selector, options = {}) {
  return loadOwlCarousel().then(() => {
    if (window.$ && window.$.fn.owlCarousel) {
      return window.$(selector).owlCarousel(options);
    } else {
      throw new Error("OWL Carousel failed to load");
    }
  });
}
