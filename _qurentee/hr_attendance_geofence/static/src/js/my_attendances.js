/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { MyAttendances } from "@hr_attendance/js/my_attendances";
import { GeofenceMap } from "./components/geofence_map";
import { useService } from "@web/core/utils/hooks";

patch(MyAttendances.prototype, {
  setup() {
    super.setup();
    this.user = useService("user");
    this.geofenceMap = null;
  },

  async update_attendance() {
    if (this.user.attendance_geolocation) {
      if (window.location.protocol !== "https:") {
        this.notification.add(
          this.env._t("Geolocation requires HTTPS connection."),
          { type: "danger" }
        );
        return;
      }

      if (!this.geofenceMap) {
        this.geofenceMap = new GeofenceMap(this.env, {
          employeeId: this.employee.id,
        });
        await this.geofenceMap.mount(
          this.el.querySelector(".attendance_geofence_container")
        );
      }

      const isInGeofence = await this.geofenceMap.checkGeofence();
      if (!isInGeofence) {
        return;
      }
    }

    return super.update_attendance();
  },
});
