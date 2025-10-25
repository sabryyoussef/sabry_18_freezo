/** @odoo-module **/

//odoo.define('hr_attendance_geofence.my_attendances', function (require) {
//    "use strict";
//
//    var MyAttendances = require('hr_attendance.my_attendances');
//    var GeofenceCommon = require('hr_attendance_geofence.GeofenceCommon');
//    var session = require("web.session");
//
//    var core = require('web.core');
//    var _t = core._t;
//
//    var MyAttendances= MyAttendances.include({
//        cssLibs: [
//            '/hr_attendance_geofence/static/src/js/lib/ol-6.12.0/ol.css',
//            '/hr_attendance_geofence/static/src/js/lib/ol-ext/ol-ext.css',
//        ],
//        jsLibs: [
//            '/hr_attendance_geofence/static/src/js/lib/ol-6.12.0/ol.js',
//            '/hr_attendance_geofence/static/src/js/lib/ol-ext/ol-ext.js',
//        ],
//        events: _.extend({}, MyAttendances.prototype.events, {
//            'click .gmap_kisok_toggle': '_toggle_gmap',
//        }),
//
//        start: function () {
//            var self = this;
//            this.olmap = null;
//            return this._super.apply(this, arguments).then(function () {
//                if (window.location.protocol == 'https:') {
//                    self.$('.o_hr_attendance_sign_in_out_icon').css('pointer-events','none');
//
//                    self.def_geolocation = $.Deferred();
//                    if(session.attendance_geolocation){
//                        self._initMap();
//                    }else{
//                        self.$('.gmap_kisok_container').addClass('d-none');
//                        self.def_geolocation.resolve();
//                    }
//
//                    $.when(self.def_geolocation).then(function(){
//                        self.$('.o_hr_attendance_sign_in_out_icon').css('pointer-events','');
//                    })
//                }
//            });
//        },
//        on_attach_callback: function () {
//            this._super.apply(this, arguments);
//            if (this.olmap) {
//                this.olmap.updateSize();
//            }
//        },
//        _toggle_gmap: function(){
//            var self = this;
//            if (self.$(".gmap_kisok_toggle").hasClass('fa-angle-double-down')) {
//                self.$('.gmap_kisok_view').toggle('show');
//                self.$("i.gmap_kisok_toggle", self).toggleClass("fa-angle-double-down fa-angle-double-up");
//                self.$(".o_hr_attendance_kiosk_backdrop")[0].setAttribute('style', 'height: calc(100vh + 197px);');
//                setTimeout(function () {
//                    self.olmap.updateSize()
//                }, 400);
//            } else {
//                self.$('.gmap_kisok_view').toggle('hide');
//                self.$("i.gmap_kisok_toggle", self).toggleClass("fa-angle-double-up fa-angle-double-down");
//                self.$(".o_hr_attendance_kiosk_backdrop")[0].setAttribute('style', 'height: calc(100vh);');
//                setTimeout(function () {
//                    self.olmap.updateSize()
//                }, 400);
//            }
//        },
//        _initMap: function(){
//            var self = this;
//            if (window.location.protocol == 'https:'){
//                var options = {
//                    enableHighAccuracy: true,
//                    maximumAge: 30000,
//                    timeout: 27000
//                };
//                if (navigator.geolocation) {
//                    navigator.geolocation.getCurrentPosition(successCallback, errorCallback, options);
//                }else {
//                    self.geolocation = false;
//                }
//
//                function successCallback(position) {
//                    self.latitude = position.coords.latitude;
//                    self.longitude = position.coords.longitude;
//                    if(!self.olmap){
//                        var olmap_div = self.$('.gmap_kisok_view').get(0);
//                        $(olmap_div).css({
//                            width: '425px !important',
//                            height: '200px !important'
//                        });
//                        var vectorSource = new ol.source.Vector({});
//                        self.olmap= new ol.Map({
//                            layers: [
//                                new ol.layer.Tile({
//                                    source: new ol.source.OSM(),
//                                }),
//                                new ol.layer.Vector({
//                                    source: vectorSource
//                                })
//                            ],
//                            loadTilesWhileInteracting: true,
//                            target: olmap_div,
//                            view: new ol.View({
//                                center: [self.latitude, self.longitude],
//                                zoom: 2,
//                            }),
//                        });
//                        const coords = [position.coords.longitude, position.coords.latitude];
//                        const accuracy = ol.geom.Polygon.circular(coords, position.coords.accuracy);
//                        vectorSource.clear(true);
//                        vectorSource.addFeatures([
//                            new ol.Feature(accuracy.transform('EPSG:4326', self.olmap.getView().getProjection())),
//                            new ol.Feature(new ol.geom.Point(ol.proj.fromLonLat(coords)))
//                        ]);
//                        self.olmap.getView().fit(vectorSource.getExtent(), {duration: 100, maxZoom:6});
//                        self.olmap.updateSize();
//                    }
//                    self.$('.gmap_kisok_container').css('display', '');
//                    self.def_geolocation.resolve();
//                }
//
//                function errorCallback(err) {
//                    switch(err.code) {
//                        case err.PERMISSION_DENIED:
//                        console.log("The request for geolocation was refused by the user.");
//                        break;
//                        case err.POSITION_UNAVAILABLE:
//                            console.log("There is no information about the location available.");
//                        break;
//                        case err.TIMEOUT:
//                            console.log("The request for the user's location was unsuccessful.");
//                        break;
//                        case err.UNKNOWN_ERROR:
//                            console.log("An unidentified error has occurred.");
//                        break;
//                    }
//                    self.def_geolocation.resolve();
//                }
//            }
//            else{
//                self.$('.gmap_kisok_container').addClass('d-none');
//                self.displayNotification({ message: _t("GEOLOCATION API MAY ONLY WORKS WITH HTTPS CONNECTIONS."), type: 'danger' });
//            }
//        },
//
//        update_attendance: function () {
//            var self = this;
//            if(session.attendance_geolocation){
//                if (window.location.protocol == 'https:'){
//                    self._getGeofenceData();
//                }else{
//                    self._super();
//                }
//            }else{
//                self._super();
//            }
//        },
//
//        _getGeofenceData: function(){
//            var self = this;
//            console.log(this.getSession());
//
//            var def = this._rpc({
//                model: 'hr.attendance.geofence',
//                method: 'search_read',
//                args: [[['company_id', '=', self.getSession().company_id],['employee_ids', 'in', self.employee.id]], ['id','name','overlay_paths']],
//            }).then(function (result) {
//                self.geofence = result;
//            });
//            return Promise.resolve(def).then(function(){
//                if(self.geofence.length > 0){
//                    self.checkIsInside();
//                }else{
//                    self.displayNotification({ message: _t("The location or employee are not included in the Geofence List."), type: 'danger' });
//                }
//            });
//        },
//
//        checkIsInside: function(){
//            var self = this;
//            var insidePolygon = false;
//            var insideGeofences = []
//            if(self.olmap){
//                for (let i = 0; i < self.geofence.length; i++) {
//                    var path = self.geofence[i].overlay_paths;
//                    var value = JSON.parse(path);
//                    if (Object.keys(value).length > 0) {
//                        let coords = ol.proj.fromLonLat([self.longitude,self.latitude]);
//                        var features = new ol.format.GeoJSON().readFeatures(value);
//                        var geometry = features[0].getGeometry();
//                        var insidePolygon = geometry.intersectsCoordinate(coords);
//                        if (insidePolygon === true) {
//                            insideGeofences.push(self.geofence[i].id);
//                        }
//                    }
//                }
//                if (insideGeofences.length > 0){
//                    var position = {
//                        latitude: self.longitude,
//                        longitude: self.latitude,
//                    }
//                    self._manual_attendance(position, insideGeofences);
//                }else{
//                    self.displayNotification({ message: _t("You haven't entered any of the geofence zones."), type: 'danger' });
//                }
//            }
//        },
//
//        _manual_attendance: function (position,insideGeofences) {
//            var self = this;
//            console.log(position,insideGeofences)
//            this._rpc({
//                model: 'hr.employee',
//                method: 'attendance_manual',
//                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances', null, [position.latitude, position.longitude], insideGeofences],
//            })
//            .then(function(result) {
//                if (result.action) {
//                    self.do_action(result.action);
//                } else if (result.warning) {
//                    self.do_warn(result.warning);
//                }
//            });
//        },
//
//    });
//});




import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { _t } from "@web/core/l10n/translation";

import { MyAttendances } from "@hr_attendance/views/my_attendances/my_attendances";

// Patch the existing MyAttendances class
patch(MyAttendances.prototype, {
    // Include required external CSS and JS libraries
    cssLibs: [
        '/hr_attendance_geofence/static/src/js/lib/ol-6.12.0/ol.css',
        '/hr_attendance_geofence/static/src/js/lib/ol-ext/ol-ext.css',
    ],
    jsLibs: [
        '/hr_attendance_geofence/static/src/js/lib/ol-6.12.0/ol.js',
        '/hr_attendance_geofence/static/src/js/lib/ol-ext/ol-ext.js',
    ],

    // Add DOM event listener for toggling map display
    events: {
        ...MyAttendances.prototype.events,
        'click .gmap_kisok_toggle': '_toggleGmap',
    },

    /**
     * Widget startup logic
     * Disables pointer-events until geolocation is processed
     */
    async start() {
        await super.start();

        this.olmap = null;
        this.defGeolocation = Promise.resolve();

        if (window.location.protocol === 'https:') {
            this.el.querySelector('.o_hr_attendance_sign_in_out_icon').style.pointerEvents = 'none';

            if (session.attendance_geolocation) {
                this.defGeolocation = this._initMap();
            } else {
                this.el.querySelector('.gmap_kisok_container').classList.add('d-none');
            }

            await this.defGeolocation;
            this.el.querySelector('.o_hr_attendance_sign_in_out_icon').style.pointerEvents = '';
        }
    },

    /**
     * Adjusts map size on re-attachment
     */
    on_attach_callback() {
        super.on_attach_callback?.();
        if (this.olmap) {
            this.olmap.updateSize();
        }
    },

    /**
     * Toggle the visibility of the geofence map
     */
    _toggleGmap() {
        const icon = this.el.querySelector(".gmap_kisok_toggle");
        const mapView = this.el.querySelector(".gmap_kisok_view");
        const backdrop = this.el.querySelector(".o_hr_attendance_kiosk_backdrop");

        if (icon.classList.contains('fa-angle-double-down')) {
            mapView.style.display = 'block';
            icon.classList.replace('fa-angle-double-down', 'fa-angle-double-up');
            backdrop.style.height = 'calc(100vh + 197px)';
        } else {
            mapView.style.display = 'none';
            icon.classList.replace('fa-angle-double-up', 'fa-angle-double-down');
            backdrop.style.height = 'calc(100vh)';
        }

        setTimeout(() => {
            this.olmap?.updateSize();
        }, 400);
    },

    /**
     * Initializes OpenLayers map with user's geolocation
     */
    async _initMap() {
        if (!navigator.geolocation) {
            console.warn("Geolocation is not supported.");
            return;
        }

        return new Promise((resolve) => {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    this.latitude = position.coords.latitude;
                    this.longitude = position.coords.longitude;

                    const olmapDiv = this.el.querySelector('.gmap_kisok_view');
                    olmapDiv.style.width = '425px';
                    olmapDiv.style.height = '200px';

                    const vectorSource = new ol.source.Vector();
                    this.olmap = new ol.Map({
                        layers: [
                            new ol.layer.Tile({ source: new ol.source.OSM() }),
                            new ol.layer.Vector({ source: vectorSource }),
                        ],
                        target: olmapDiv,
                        view: new ol.View({
                            center: ol.proj.fromLonLat([this.longitude, this.latitude]),
                            zoom: 6,
                        }),
                    });

                    const coords = [this.longitude, this.latitude];
                    const accuracy = ol.geom.Polygon.circular(coords, position.coords.accuracy);
                    vectorSource.clear(true);
                    vectorSource.addFeatures([
                        new ol.Feature(accuracy.transform('EPSG:4326', this.olmap.getView().getProjection())),
                        new ol.Feature(new ol.geom.Point(ol.proj.fromLonLat(coords)))
                    ]);

                    this.olmap.getView().fit(vectorSource.getExtent(), { duration: 100, maxZoom: 6 });
                    this.olmap.updateSize();

                    this.el.querySelector('.gmap_kisok_container').style.display = '';
                    resolve();
                },
                (error) => {
                    console.warn("Geolocation error:", error.message);
                    resolve();
                },
                {
                    enableHighAccuracy: true,
                    maximumAge: 30000,
                    timeout: 27000,
                }
            );
        });
    },

    /**
     * Called when the attendance button is clicked
     */
    async update_attendance() {
        if (session.attendance_geolocation && window.location.protocol === 'https:') {
            await this._getGeofenceData();
            // NOTE: insert geofence-checking logic here if needed
            return super.update_attendance();
        }
        return super.update_attendance();
    },

    /**
     * Calls backend to fetch geofencing configuration
     */
    async _getGeofenceData() {
        const result = await this.rpc({
            model: 'hr.attendance.geofence',
            method: 'search_read',
            args: [
                [
                    ['company_id', '=', this.getSession().company_id],
                    ['employee_ids', 'in', this.employee.id]
                ],
                ['id', 'name', 'overlay_paths']
            ]
        });
        this.geofence = result;
    },
});
