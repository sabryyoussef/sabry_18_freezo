/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ErrorReportSystray extends Component {
    static template = "error_reporter_enterprise.ErrorReportSystray";
    static props = {};

    setup() {
        this.action = useService("action");
    }

    async onClick() {
        this.action.doAction('error_reporter_enterprise.action_qa_error_event');
    }
}

registry.category("systray").add("error_reporter_enterprise.ErrorReportSystray", {
    Component: ErrorReportSystray,
    isDisplayed: () => true,
});