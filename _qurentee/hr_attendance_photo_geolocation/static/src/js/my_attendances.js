/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { CheckInOut } from "@hr_attendance/components/check_in_out/check_in_out";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";

patch(CheckInOut.prototype, {
  setup() {
    super.setup();
    this.user = useService("user");
    this.notification = useService("notification");
    this.dialogService = useService("dialog");

    this.state = useState({
      latitude: null,
      longitude: null,
      isLocationEnabled: false,
      isPhotoEnabled: false,
      isLocationDisplayed: false,
    });

    // Initialize geolocation and photo settings
    this.initializeSettings();
  },

  async initializeSettings() {
    try {
      // Get company settings for photo and geolocation
      const companySettings = await rpc("/web/dataset/call_kw", {
        model: "res.company",
        method: "read",
        args: [
          [this.user.context.allowed_company_ids[0]],
          ["hr_attendance_geolocation", "hr_attendance_photo"],
        ],
        kwargs: {},
      });

      if (companySettings.length > 0) {
        const settings = companySettings[0];
        this.state.isLocationEnabled = settings.hr_attendance_geolocation;
        this.state.isPhotoEnabled = settings.hr_attendance_photo;
      }

      // Initialize geolocation if enabled and HTTPS
      if (
        this.state.isLocationEnabled &&
        window.location.protocol === "https:"
      ) {
        await this.getGeolocation();
      }
    } catch (error) {
      console.error("Failed to load settings:", error);
    }
  },

  async getGeolocation() {
    const options = {
      enableHighAccuracy: true,
      maximumAge: 30000,
      timeout: 27000,
    };

    if (!navigator.geolocation) {
      console.log("Geolocation is not supported by this browser.");
      return;
    }

    try {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, options);
      });

      this.state.latitude = position.coords.latitude;
      this.state.longitude = position.coords.longitude;
      this.state.isLocationDisplayed = true;
    } catch (error) {
      this.handleGeolocationError(error);
    }
  },

  handleGeolocationError(error) {
    switch (error.code) {
      case error.PERMISSION_DENIED:
        console.log("The request for geolocation was refused by the user.");
        break;
      case error.POSITION_UNAVAILABLE:
        console.log("There is no information about the location available.");
        break;
      case error.TIMEOUT:
        console.log("The request for the user's location was unsuccessful.");
        break;
      default:
        console.log("An unidentified error has occurred.");
        break;
    }
  },

  toggleLocationDisplay() {
    this.state.isLocationDisplayed = !this.state.isLocationDisplayed;
  },

  async signInOut() {
    if (window.location.protocol !== "https:") {
      return super.signInOut();
    }

    try {
      await this.validateAttendance();
    } catch (error) {
      console.error("Attendance validation failed:", error);
      this.notification.add(_t("Failed to process attendance"), {
        type: "danger",
      });
    }
  },

  async validateAttendance() {
    const attendanceData = {
      latitude: null,
      longitude: null,
      photo: null,
    };

    // Get geolocation data if enabled
    if (this.state.isLocationEnabled) {
      if (this.state.latitude && this.state.longitude) {
        attendanceData.latitude = this.state.latitude;
        attendanceData.longitude = this.state.longitude;
      } else {
        throw new Error("Geolocation data not available");
      }
    }

    // Get photo data if enabled
    if (this.state.isPhotoEnabled) {
      try {
        attendanceData.photo = await this.capturePhoto();
      } catch (error) {
        throw new Error("Photo capture failed");
      }
    }

    // Process attendance with collected data
    await this.processAttendance(attendanceData);
  },

  async capturePhoto() {
    return new Promise((resolve, reject) => {
      const dialogProps = {
        title: _t("Capture Snapshot"),
        body: this.renderPhotoDialog(),
        size: "md",
        confirm: () => {
          const photoData = this.getPhotoFromCanvas();
          if (photoData) {
            resolve(photoData);
          } else {
            reject(new Error("No photo captured"));
          }
        },
        cancel: () => reject(new Error("Photo capture cancelled")),
      };

      this.dialogService.add(Dialog, dialogProps);
    });
  },

  renderPhotoDialog() {
    return `
            <div class="container-fluid">
                <div class="col-12 controls">
                    <fieldset class="reader-config-group">
                        <div class="row">
                            <div class="col-3">
                                <label>
                                    <span>${_t("Select Camera")}</span>
                                </label>
                            </div>
                            <div class="col-6">
                                <select name="video_source" class="videoSource" id="videoSource">                                       
                                </select>
                            </div>
                            <div class="col-3">
                            </div>
                        </div>
                    </fieldset>
                </div>
                <div class="row">                                
                    <div class="col-12" id="videoContainer">
                        <video autoplay muted playsinline id="video" style="width: 100%; max-height: 100%; box-sizing: border-box;" autoplay="1"/>
                        <canvas id="image" style="display: none;"/>
                    </div>
                </div>
            </div>
        `;
  },

  async initializeCamera() {
    const videoElement = document.getElementById("video");
    const videoSelect = document.getElementById("videoSource");

    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const videoDevices = devices.filter(
        (device) => device.kind === "videoinput"
      );

      videoDevices.forEach((device, index) => {
        const option = document.createElement("option");
        option.value = device.deviceId;
        option.text = device.label || `Camera ${index + 1}`;
        videoSelect.appendChild(option);
      });

      await this.startVideoStream(videoSelect.value);

      videoSelect.onchange = async () => {
        await this.startVideoStream(videoSelect.value);
      };
    } catch (error) {
      console.error("Error accessing camera:", error);
      throw error;
    }
  },

  async startVideoStream(deviceId) {
    if (window.stream) {
      window.stream.getTracks().forEach((track) => track.stop());
    }

    const constraints = {
      video: { deviceId: deviceId ? { exact: deviceId } : undefined },
    };

    try {
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      window.stream = stream;
      document.getElementById("video").srcObject = stream;
    } catch (error) {
      console.error("Error starting video stream:", error);
      throw error;
    }
  },

  getPhotoFromCanvas() {
    const video = document.getElementById("video");
    const canvas = document.getElementById("image");

    if (!video || !canvas) return null;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL("image/jpeg");
    return imageData.replace(/^data:image\/(png|jpg|jpeg|webp);base64,/, "");
  },

  async processAttendance(attendanceData) {
    try {
      const result = await this.orm.call("hr.employee", "attendance_manual", [
        [this.props.employeeId],
        this.props.nextAction,
        null,
        attendanceData.latitude
          ? [attendanceData.latitude, attendanceData.longitude]
          : null,
        attendanceData.photo ? [attendanceData.photo] : null,
      ]);

      if (result.action) {
        this.actionService.doAction(result.action);
        // Clean up video streams
        if (window.stream) {
          window.stream.getTracks().forEach((track) => track.stop());
        }
      } else if (result.warning) {
        this.notification.add(result.warning, { type: "danger" });
      }
    } catch (error) {
      console.error("Error processing attendance:", error);
      this.notification.add(_t("Failed to process attendance"), {
        type: "danger",
      });
    }
  },
});
