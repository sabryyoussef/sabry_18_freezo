/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ErrorReportSystray extends Component {
    static template = "automatic_error_reporter.ErrorReportSystray";

    setup() {
        this.action = useService("action");
    }

    async onClick() {
        this.action.doAction('automatic_error_reporter.action_qa_error_event');
    }
}

registry.category("systray").add("automatic_error_reporter.ErrorReportSystray", {
    Component: ErrorReportSystray,
    isDisplayed: () => true,
});