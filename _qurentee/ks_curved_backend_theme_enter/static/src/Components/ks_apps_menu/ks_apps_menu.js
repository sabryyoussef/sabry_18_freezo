/** @odoo-module */

import { NavBar } from "@web/webclient/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { useService } from "@web/core/utils/hooks";
import { onWillStart, onMounted, useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

/**
 * Reduces menu data to a flat structure for easier searching
 * @param {Object} memo - Accumulator object
 * @param {Object} menu - Current menu item
 * @returns {Object} Reduced menu data
 */
const ksGetReducedMenuData = (memo, menu) => {
    if (menu.actionID) {
        const key = menu.ks_parent_name ? menu.ks_parent_name : "";
        menu.ks_title = (key + menu.name).toLowerCase();
        memo[key + menu.name] = menu;
    }
    if (menu.children?.length) {
        const childMenus = this.menuService.getMenuAsTree(menu.id).childrenTree;
        childMenus.forEach((childMenu) => {
            childMenu.ks_parent_id = menu.id;
            childMenu.ks_parent_name = menu.ks_parent_name 
                ? `${menu.ks_parent_name}/${menu.name}`
                : menu.name;
        });
        childMenus.reduce(ksGetReducedMenuData.bind(this), memo);
    }
    return memo;
};

patch(NavBar.prototype, {
    setup() {
        super.setup();

        this.menuService = useService("menu");
        this.rpc = useService("rpc");
        this.state = useState({
            searchQuery: "",
            searchResults: {
                apps: [],
                items: []
            }
        });

        const hour = new Date().getHours();
        const greeting = hour < 12 ? "Good Morning" 
            : hour < 18 ? "Good Afternoon" 
            : "Good Evening";

        this.ks_user_id = session.uid;
        this.ks_user_name = `${greeting}, ${session.name}`;
        this._ks_fuzzysearchableMenus = this.menuService
            .getApps()
            .reduce(ksGetReducedMenuData.bind(this), {});

        onWillStart(async () => {
            await this.willStart();
        });

        onMounted(() => {
            this._setupSearchElements();
        });
    },

    async willStart() {
        const apps = this.menuService.getApps();
        let ks_fav_apps = apps;
        let data = [];

        try {
            const [favData, appIcons] = await Promise.all([
                this.rpc("/ks_app_frequency/render", {}),
                this.rpc("/ks_curved_theme/get_fav_icons", {
                    ks_app_icons: apps
                })
            ]);
            data = favData;
            ks_fav_apps = appIcons;
        } catch (error) {
            console.error("Error loading app data:", error);
        }

        this.apps = ks_fav_apps;
        this.ks_fav_apps = ks_fav_apps;
        this._ks_frequent_apps = data
            .map(itemId => apps.find(app => app.id === itemId))
            .filter(Boolean);
    },

    _setupSearchElements() {
        this.searchContainer = this.el.querySelector(".ks_menu_search");
        this.searchInput = this.el.querySelector(".ks_menu_search_box input");
        this.searchResults = this.el.querySelector(".ks-search-values");
    },

    /**
     * Splits apps into chunks of 12 for pagination
     * @returns {Object[][]} Array of app chunks
     */
    _getSplittedApps() {
        const chunkSize = 12;
        return Array.from(
            { length: Math.ceil(this.ks_fav_apps.length / chunkSize) },
            (_, i) => this.ks_fav_apps.slice(i * chunkSize, (i + 1) * chunkSize)
        );
    },

    /**
     * Returns frequent apps for current user
     * @returns {Object[]} Array of frequent apps
     */
    _getFrequentApps() {
        return this._ks_frequent_apps;
    },

    _ksHideFavIcons(ev) {
        ev.preventDefault();
        document.body.classList.remove("ks_appsmenu_edit");

        const favIcons = document.querySelectorAll(
            "div.ks_appdrawer_inner_app_div span.ks_fav_icon"
        );
        favIcons.forEach(icon => icon.classList.add("d-none"));

        const closeButtons = document.querySelectorAll(
            "div.ks_appdrawer_div div.ks-app-drawer-close"
        );
        closeButtons.forEach(btn => btn.classList.add("d-none"));
    },

    _ksSearchFocus() {
        if (!this.env.device.isMobile && this.searchInput) {
            this.searchInput.focus();
        }
    },

    _ksSearchMenuListTime() {
        this._ks_search_def = new Promise(resolve => setTimeout(resolve, 50));
        this._ks_search_def.then(() => this._ksSearchMenusList());
    },

    _ksSearchResetvalues() {
        if (this.searchContainer) {
            this.searchContainer.classList.remove("ks-find-values");
        }
        if (this.searchResults) {
            this.searchResults.innerHTML = "";
        }
        if (this.searchInput) {
            this.searchInput.value = "";
            this.state.searchQuery = "";
        }
    },

    _ksSearchMenusList() {
        if (!this.searchInput) return;

        const query = this.searchInput.value.toLowerCase();
        if (!query) {
            this._ksSearchResetvalues();
            return;
        }

        const newDataApp = Object.values(this._ks_fuzzysearchableMenus)
            .filter(menu => menu.ks_title && !menu.ks_parent_id && menu.ks_title.includes(query));
        const newDataItems = Object.values(this._ks_fuzzysearchableMenus)
            .filter(menu => menu.ks_title && menu.ks_parent_id && menu.ks_title.includes(query));

        this.state.searchResults = {
            apps: newDataApp,
            items: newDataItems
        };

        if (this.searchContainer) {
            this.searchContainer.classList.toggle(
                "ks-find-values",
                Boolean(newDataApp.length + newDataItems.length)
            );
        }
    },

    async _ksManageFavApps(ev) {
        const isAdd = ev.currentTarget.classList.contains("ks_add_fav");
        await (isAdd ? this._ksAddFavApps(ev) : this._ksRemoveFavApps(ev));
    },

    async _ksAddFavApps(ev) {
        ev.preventDefault();
        const currentTarget = ev.currentTarget;
        const menuId = currentTarget.previousElementSibling.getAttribute("data-menu-id");

        try {
            const result = await this.rpc("/ks_curved_theme/set_fav_icons", {
                ks_app_id: menuId
            });

            if (result) {
                await this.ks_update_fav_icon();
                this._ksRemFromFav(ev, currentTarget);
            }
        } catch (error) {
            console.error("Error adding favorite app:", error);
        }
    },

    async _ksRemoveFavApps(ev) {
        ev.preventDefault();
        const currentTarget = ev.currentTarget;
        const menuId = currentTarget.previousElementSibling.getAttribute("data-menu-id");

        try {
            const result = await this.rpc("/ks_curved_theme/rmv_fav_icons", {
                ks_app_id: menuId
            });

            if (result) {
                await this.ks_update_fav_icon();
                this._ksAddToFav(ev, currentTarget);
            }
        } catch (error) {
            console.error("Error removing favorite app:", error);
        }
    },

    async ks_update_fav_icon() {
        try {
            const apps = this.menuService.getApps();
            const favIcons = await this.rpc("/ks_curved_theme/get_fav_icons", {
                ks_app_icons: apps
            });
            this.ks_fav_apps = favIcons;
        } catch (error) {
            console.error("Error updating favorite icons:", error);
        }
    },

    _ksAddToFav(ev, ks_current_target) {
        ks_current_target.classList.remove("ks_rmv_fav");
        ks_current_target.classList.add("ks_add_fav");

        const img = ks_current_target.querySelector("img");
        if (img) {
            img.src = "ks_curved_backend_theme_enter/static/src/images/star.svg";
        }
    },

    _ksRemFromFav(ev, ks_current_target) {
        ks_current_target.classList.remove("ks_add_fav");
        ks_current_target.classList.add("ks_rmv_fav");

        const img = ks_current_target.querySelector("img");
        if (img) {
            img.src = "ks_curved_backend_theme_enter/static/src/images/fav_ic.svg";
        }
    },

    _onKsAppsMenuItemClicked(ev) {
        document.body.classList.toggle("o_home_menu_background");
        if (document.body.classList.contains("o_home_menu_background")) {
            document.body.classList.remove("brightness");
            this._ksManagerDrawer("open");
        } else {
            document.body.classList.add("brightness");
            this._ksManagerDrawer("close");
        }
    },

    _ksManagerDrawer(action) {
        // Implementation for managing drawer state
        console.log(`Managing drawer: ${action}`);
    },
});
