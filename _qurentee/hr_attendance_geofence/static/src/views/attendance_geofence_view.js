/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

/**
 * @extends Component
 */
class AttendanceGeofenceClientAction extends Component {
  static template = "hr_attendance_geofence.AttendanceGeofenceView";
  static props = ["*"];

  setup() {
    this.state = useState({
      isLoading: false,
      error: null,
      currentUser: null,
    });

    this.orm = useService("orm");
    this.action = useService("action");
    this.notification = useService("notification");

    // Get user info from environment
    this.getCurrentUser();
  }

  async getCurrentUser() {
    try {
      // Get current user info
      const userInfo = await this.orm.call("res.users", "read", [[]], {
        fields: ["id", "name"],
      });
      if (userInfo && userInfo.length > 0) {
        this.state.currentUser = userInfo[0];
      }
    } catch (error) {
      console.error("Failed to get current user:", error);
    }
  }

  async onGeofenceClick() {
    try {
      this.state.isLoading = true;
      this.state.error = null;

      if (!this.state.currentUser) {
        this.notification.add("User information not available!", {
          type: "danger",
        });
        return;
      }

      const employee = await this.orm.searchRead(
        "hr.employee",
        [["user_id", "=", this.state.currentUser.id]],
        ["attendance_state", "name"]
      );

      if (employee.length === 0) {
        this.notification.add("No employee found for your user!", {
          type: "danger",
        });
        return;
      }

      const currentEmployee = employee[0];

      // Show current status
      const statusMessage =
        currentEmployee.attendance_state === "checked_in"
          ? `${currentEmployee.name} is currently checked in. Click to check out.`
          : `${currentEmployee.name} is currently checked out. Click to check in.`;

      this.notification.add(statusMessage, {
        type: "info",
      });

      const action = await this.orm.call(
        "hr.employee",
        "attendance_manual",
        [[currentEmployee.id]],
        {
          context: { get_location: true },
        }
      );

      if (action) {
        await this.action.doAction(action);
      }
    } catch (error) {
      console.error("Geofence error:", error);
      this.state.error = error;
      this.notification.add(error.message || "An error occurred", {
        type: "danger",
      });
    } finally {
      this.state.isLoading = false;
    }
  }
}

// Register the client action
registry
  .category("actions")
  .add("attendance_geofence", AttendanceGeofenceClientAction);
