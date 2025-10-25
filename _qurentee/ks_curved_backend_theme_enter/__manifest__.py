# -*- coding: utf-8 -*-
{
    "name": "Arc Backend Theme Enterprise",
    "summary": """
        Advanced Material Backend theme, Responsive Theme, fully functional
        theme, Flexible backend theme, lightweight backend theme, animated
        backend theme, Modern multipurpose theme, customizable backend theme,
        multi tab back theme, back end theme odoo.
    """,
    "description": """
odoo backend themes
        odoo responsive backend theme
        odoo themes
        odoo backend theme V18
        odoo 18 backend theme
        backend theme odoo
        odoo enterprise theme
        odoo custom themes
        odoo theme download
        change odoo backend theme
        odoo material backend theme
        odoo theme backend
        backend theme odoo apps
        odoo backend theme customize
        change backend theme odoo
        odoo backend layout theme
        customizable odoo Theme
        customize odoo backend
        change odoo backend color
        odoo app backend theme
        Arc Theme
        Arc Themes
        Backend Theme
        Backend Themes
        Curved Theme
        Boxed Theme
        Curved Backend Theme
        Odoo Arc Theme
        Odoo Arc Backend Theme
        Odoo Arc
        Odoo Backend Theme
        Ksolves Arc
        Ksolves Arc Theme
        Ksolves Arc Backend Theme
        Ksolves Odoo Theme
        Ksolves Odoo Backend Theme
        Ksolves Backend Theme
        Ksolves Themes
    """,
    "author": "Ksolves India Ltd.",
    "website": "https://www.ksolves.com",
    "license": "OPL-1",
    "currency": "EUR",
    "price": "98.25",
    "version": "18.0.1.0.0",
    "live_test_url": "https://arcbackendtheme18.kappso.com/web/demo_login",
    "category": "Themes/Backend",
    "support": "sales@ksolves.com",
    "depends": ["web", "base_setup", "mail", "auth_signup", "web_enterprise"],
    # always loaded
    "data": [
        "data/data.xml",
        "data/ks_drawer_colors.xml",
        "data/ks_color_theme.xml",
        "security/ir.model.access.csv",
        "security/curved_theme_security.xml",
        "views/views.xml",
        "views/ks_main_panel.xml",
        "views/templates.xml",
        "views/ks_assets_popup_animation.xml",
        "views/ks_login_page.xml",
        "views/ks_res_users_preferences.xml",
        "views/ks_res_config_settings_view.xml",
    ],
    "images": [
        "static/description/odoo arch theme.gif",
        "static/description/Odoo Apps GIF Dashboard Ninja with AI.gif",
    ],
    "assets": {
        "web._assets_primary_variables": [
            (
                "ks_curved_backend_theme_enter/static/src/scss/"
                "abstracts/odoo_primary_variables.scss"
            ),
        ],
        "web.assets_backend": [
            # SCSS Files
            "ks_curved_backend_theme_enter/static/src/scss/abstracts/variables.scss",
            "ks_curved_backend_theme_enter/static/src/scss/base/fonts.scss",
            "ks_curved_backend_theme_enter/static/src/scss/base/default.scss",
            "ks_curved_backend_theme_enter/static/src/scss/base/animation.scss",
            "ks_curved_backend_theme_enter/static/src/scss/base/forms.scss",
            "ks_curved_backend_theme_enter/static/src/scss/base/fields.scss",
            "ks_curved_backend_theme_enter/static/src/scss/abstracts/mixins.scss",
            "ks_curved_backend_theme_enter/static/src/scss/abstracts/placeholder.scss",
            "ks_curved_backend_theme_enter/static/src/scss/components/buttons.scss",
            "ks_curved_backend_theme_enter/static/src/scss/components/color_theme.scss",
            "ks_curved_backend_theme_enter/static/src/scss/components/tabs.scss",
            "ks_curved_backend_theme_enter/static/src/scss/components/table.scss",
            "ks_curved_backend_theme_enter/static/src/scss/components/form-control.scss",
            "ks_curved_backend_theme_enter/static/src/scss/components/checkbox.scss",
            "ks_curved_backend_theme_enter/static/src/scss/components/loaders.scss",
            "ks_curved_backend_theme_enter/static/src/scss/components/Breadcrumb.scss",
            "ks_curved_backend_theme_enter/static/src/scss/layout/header.scss",
            "ks_curved_backend_theme_enter/static/src/scss/layout/apps-drawer.scss",
            "ks_curved_backend_theme_enter/static/src/scss/layout/ks_quick_settings.scss",
            "ks_curved_backend_theme_enter/static/src/scss/layout/sidebar.scss",
            "ks_curved_backend_theme_enter/static/src/scss/layout/bookmark.scss",
            "ks_curved_backend_theme_enter/static/src/scss/layout/ks_control_panel.scss",
            "ks_curved_backend_theme_enter/static/src/scss/layout/ks_form_view.scss",
            "ks_curved_backend_theme_enter/static/src/scss/layout/ks_view.scss",
            "ks_curved_backend_theme_enter/static/src/scss/layout/ks_vertical_menus.scss",
            "ks_curved_backend_theme_enter/static/src/scss/responsive/ipad_responsive.scss",
            "ks_curved_backend_theme_enter/static/src/scss/responsive/phone_responsive.scss",
            "ks_curved_backend_theme_enter/static/src/scss/pages/discuss.scss",
            "ks_curved_backend_theme_enter/static/src/scss/pages/calendar.scss",
            "ks_curved_backend_theme_enter/static/src/scss/pages/all_apps.scss",
            "ks_curved_backend_theme_enter/static/src/lib/owl.carousel.min.css",
            "ks_curved_backend_theme_enter/static/src/scss/components/ks_custom_tooltip.css",
            # Modern JS Components (Odoo 18 compatible)
            "ks_curved_backend_theme_enter/static/src/components/ks_web_client/ks_web_client.js",
            # XML Templates are loaded from views directory instead
        ],
        "web.assets_frontend": [
            "ks_curved_backend_theme_enter/static/src/scss/pages/ks_login.scss",
        ],
    },
    "application": True,
    "installable": True,
}
