/** @odoo-module **/

import { MyAttendances } from "@hr_attendance/components/my_attendances/my_attendances";
import { KioskConfirm } from "@hr_attendance/components/kiosk_confirm/kiosk_confirm";
import { session } from "@web/session";
import { useDialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { Component } from "@odoo/owl";

let latitude;
let longitude;

// Error Dialog Component
class ErrorDialog extends Component {
    static template = "odoo_attendance_user_location.ErrorDialog";
    static props = ["title", "body"];
}

patch(MyAttendances.prototype, "odoo_attendance_user_location.my_attendances", {
    setup() {
        super.setup();
        this.dialog = useDialog();
    },

    update_attendance() {
        const self = this;
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const ctx = Object.assign(session.user_context, {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                    });

                    latitude = position.coords.latitude;
                    longitude = position.coords.longitude;
                    self._rpc({
                        model: 'hr.employee',
                        method: 'attendance_manual',
                        args: [
                            [self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances'
                        ],
                        context: ctx,
                    })
                    .then(function(result) {
                        if (result.action) {
                            self.do_action(result.action);
                        } else if (result.warning) {
                            self.displayNotification({
                                title: result.warning,
                                type: 'danger'
                            });
                        }
                    });
                },
                function(error) {
                    // Handle any errors
                    if (error) {
                        self.dialog.add(ErrorDialog, {
                            title: error.__proto__.constructor.name,
                            body: error['message'] + ". Also check your site connection is secured!",
                        });
                    }
                }
            );
        } else {
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [
                    [self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances'
                ],
                context: session.user_context,
            })
            .then(function(result) {
                if (result.action) {
                    self.do_action(result.action);
                } else if (result.warning) {
                    self.displayNotification({
                        title: result.warning,
                        type: 'danger'
                    });
                }
            });
        }
    },
});

patch(KioskConfirm.prototype, "odoo_attendance_user_location.kiosk_confirm", {
    setup() {
        super.setup();
        this.dialog = useDialog();
    },

    events: {
        "click .o_hr_attendance_sign_in_out_icon": _.debounce(
            function() {
                const self = this;
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            const ctx = Object.assign(session.user_context, {
                                latitude: position.coords.latitude,
                                longitude: position.coords.longitude,
                            });
                            latitude = position.coords.latitude;
                            longitude = position.coords.longitude;
                            self._rpc({
                                model: 'hr.employee',
                                method: 'attendance_manual',
                                args: [
                                    [self.employee_id], self.next_action
                                ],
                                context: ctx,
                            })
                            .then(function(result) {
                                if (result.action) {
                                    self.do_action(result.action);
                                } else if (result.warning) {
                                    self.displayNotification({
                                        title: result.warning,
                                        type: 'danger'
                                    });
                                }
                            });
                        },
                        function(error) {
                            // Handle any errors
                            if (error) {
                                self.dialog.add(ErrorDialog, {
                                    title: error.__proto__.constructor.name,
                                    body: error['message'] + ". Also check your site connection is secured!",
                                });
                            }
                        }
                    );
                }
            },
            200,
            true
        ),
        "click .o_hr_attendance_pin_pad_button_ok": _.debounce(
            function() {
                const self = this;
                this.pin_pad = true;
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            const ctx = Object.assign(session.user_context, {
                                latitude: position.coords.latitude,
                                longitude: position.coords.longitude,
                            });
                            latitude = position.coords.latitude;
                            longitude = position.coords.longitude;
                            self._rpc({
                                model: 'hr.employee',
                                method: 'attendance_manual',
                                args: [
                                    [self.employee_id], self.next_action, self.$('.o_hr_attendance_PINbox').val()
                                ],
                                context: session.user_context,
                            })
                            .then(function(result) {
                                if (result.action) {
                                    self.do_action(result.action);
                                } else if (result.warning) {
                                    self.displayNotification({
                                        title: result.warning,
                                        type: 'danger'
                                    });
                                    self.$('.o_hr_attendance_PINbox').val('');
                                    setTimeout(function() {
                                        self.$('.o_hr_attendance_pin_pad_button_ok').removeAttr("disabled");
                                    }, 500);
                                }
                            });
                        },
                        function(error) {
                            // Handle any errors
                            if (error) {
                                self.dialog.add(ErrorDialog, {
                                    title: error.__proto__.constructor.name,
                                    body: error['message'] + ". Also check your site connection is secured!",
                                });
                            }
                        }
                    );
                }
            },
            200,
            true
        ),
    },
});