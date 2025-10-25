/** @odoo-module **/

import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class GeofenceMap extends Component {
  setup() {
    this.state = useState({
      showMap: false,
      latitude: null,
      longitude: null,
    });

    this.olmap = null;
    this.notification = useService("notification");
    this.orm = useService("orm");
    this.user = useService("user");

    onMounted(() => this.initMap());
    onWillUnmount(() => {
      if (this.olmap) {
        this.olmap.setTarget(null);
        this.olmap = null;
      }
    });
  }

  async initMap() {
    if (window.location.protocol !== "https:") {
      this.notification.add(
        this.env._t("GEOLOCATION API MAY ONLY WORKS WITH HTTPS CONNECTIONS."),
        { type: "danger" }
      );
      return;
    }

    const options = {
      enableHighAccuracy: true,
      maximumAge: 30000,
      timeout: 27000,
    };

    try {
      const position = await this._getCurrentPosition(options);
      this.state.latitude = position.coords.latitude;
      this.state.longitude = position.coords.longitude;
      this._initializeOLMap(position);
    } catch (error) {
      console.error("Geolocation error:", error);
      this.notification.add(
        this.env._t("Failed to get location: ") + error.message,
        { type: "danger" }
      );
    }
  }

  _getCurrentPosition(options) {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error("Geolocation is not supported"));
        return;
      }
      navigator.geolocation.getCurrentPosition(resolve, reject, options);
    });
  }

  _initializeOLMap(position) {
    const mapElement = this.el.querySelector(".gmap_kisok_view");
    if (!mapElement) return;

    const vectorSource = new ol.source.Vector({});
    this.olmap = new ol.Map({
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM(),
        }),
        new ol.layer.Vector({
          source: vectorSource,
        }),
      ],
      loadTilesWhileInteracting: true,
      target: mapElement,
      view: new ol.View({
        center: ol.proj.fromLonLat([
          position.coords.longitude,
          position.coords.latitude,
        ]),
        zoom: 15,
      }),
    });

    const coords = [position.coords.longitude, position.coords.latitude];
    const accuracy = ol.geom.Polygon.circular(coords, position.coords.accuracy);
    vectorSource.clear(true);
    vectorSource.addFeatures([
      new ol.Feature(
        accuracy.transform("EPSG:4326", this.olmap.getView().getProjection())
      ),
      new ol.Feature(new ol.geom.Point(ol.proj.fromLonLat(coords))),
    ]);

    this.olmap.getView().fit(vectorSource.getExtent(), {
      duration: 100,
      maxZoom: 18,
    });
    this.olmap.updateSize();
  }

  toggleMap() {
    this.state.showMap = !this.state.showMap;
    if (this.state.showMap && this.olmap) {
      // Use setTimeout to ensure the map container is visible before updating
      setTimeout(() => this.olmap.updateSize(), 100);
    }
  }

  async checkGeofence() {
    const geofences = await this.orm.searchRead(
      "hr.attendance.geofence",
      [
        ["company_id", "=", this.user.companyId],
        ["employee_ids", "in", this.props.employeeId],
      ],
      ["id", "name", "overlay_paths"]
    );

    if (!geofences.length) {
      this.notification.add(
        this.env._t(
          "The location or employee are not included in the Geofence List."
        ),
        { type: "danger" }
      );
      return false;
    }

    const currentCoords = ol.proj.fromLonLat([
      this.state.longitude,
      this.state.latitude,
    ]);
    for (const geofence of geofences) {
      const path = JSON.parse(geofence.overlay_paths);
      if (Object.keys(path).length > 0) {
        const features = new ol.format.GeoJSON().readFeatures(path);
        const geometry = features[0].getGeometry();
        if (geometry.intersectsCoordinate(currentCoords)) {
          return true;
        }
      }
    }

    this.notification.add(
      this.env._t("You are not within any allowed attendance areas."),
      { type: "danger" }
    );
    return false;
  }
}

GeofenceMap.template = "hr_attendance_geofence.MapToggleTemplate";
GeofenceMap.props = {
  employeeId: { type: Number, required: true },
};
