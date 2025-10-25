/** @odoo-module **/


// odoo.define('hr_attendance_geofence.GeofenceRenderer', function (require) {
//     'use strict';

//     var BasicRenderer = require('web.BasicRenderer');
//     var core = require('web.core');
//     var QWeb = require('web.QWeb');
//     var session = require('web.session');
//     var utils = require('web.utils');
//     var Widget = require('web.Widget');
//     var KanbanRecord = require('web.KanbanRecord');

//     var qweb = core.qweb;

//     var GeofenceRenderer = BasicRenderer.extend({        
//         template: 'GeofenceView',
//         className: 'o_geofence_view',
//         xmlDependencies: ['/hr_attendance_geofence/static/src/xml/geofence_template.xml'],
//         init: function (parent, state, params) {
//             this._super.apply(this, arguments);
//             this.olmap = null;
//             this.state = state;
//             this.drawingPath = params.drawingPath || 'overlay_paths';
//         },

//         start: function () {            
//             return this._super.apply(this, arguments);
//         },

//         on_attach_callback: function () {
//             var self = this;            
//             this._init_olmap();   
//             return this._super();
//         },

//         _init_olmap: function () {            
//             var olmap_div = this.$(".olmap_widget").get(0);
//             $(olmap_div).css({
//                 width: '100%',
//                 height: '100%'
//             });
//             var map = this._load_olmap();
//             if (this.olmap) {
//                 map.setTarget(olmap_div);
//                 this._ol_add_layer_vector();
//                 this.olmap.updateSize();
//             }
//         },
//         _load_olmap: function () {            
//             if (!this.olmap) {
//                 this.olmap = new ol.Map({
//                 layers: [
//                   new ol.layer.Tile({
//                     source: new ol.source.OSM(),
//                   }) ],
//                 view: new ol.View({
//                   center: ol.proj.fromLonLat([0,0]),
//                   zoom: 0,
//                 }),
//               });
//           }
//           return this.olmap;
//         },
//         _ol_add_layer_vector: function(){
//             var self = this;
//             if (self.olmap){
//                 console.log(this.state.data);
//                 _.each(this.state.data, function (record) {
//                     var value = record.data[self.drawingPath];
//                     if (Object.keys(value).length > 0) {  
//                         var value = JSON.parse(value);
//                         self.vectorSource = new ol.layer.Vector({
//                             source:new ol.source.Vector({
//                                 features:(new ol.format.GeoJSON()).readFeatures(value)
//                             }),
//                             style: new ol.style.Style({
//                                 fill: new ol.style.Fill({
//                                     color: 'rgb(255 235 59 / 62%)',
//                                 }),
//                                 stroke: new ol.style.Stroke({
//                                     color: '#ffc107',
//                                     width: 2,
//                                 }),
//                                 image: new ol.style.Circle({
//                                     radius: 7,
//                                     fill: new ol.style.Fill({
//                                         color: '#ffc107',
//                                     }),
//                                 }),
//                             }),
//                         });
//                         self.olmap.addLayer(self.vectorSource);
//                     };
//                 });
//                 self.olmap.updateSize();
//             }
            
//         },
//         _renderView: function () {
//             var self = this;
//             return this._super.apply(this, arguments);
//         },

//         updateState: function (state, params) {
//             this._super.apply(this, arguments);
//             if(this.olmap){
//                 this._ol_add_layer_vector();
//                 this.olmap.updateSize();
//             }
//             return $.when();
//         },
//     });

//     return GeofenceRenderer;
// });

import { BasicRenderer } from "@web/views/basic/basic_renderer";

export class GeofenceRenderer extends BasicRenderer {
    static template = "GeofenceView";
    static className = "o_geofence_view";
//    static xmlDependencies = ["/hr_attendance_geofence/static/src/xml/geofence_template.xml"];

    constructor(parent, state, params) {
        super(...arguments);
        this.olmap = null;
        this.state = state;
        this.drawingPath = params.drawingPath || "overlay_paths";
    }

    async start() {
        await super.start();
    }

    on_attach_callback() {
        super.on_attach_callback();
        this._init_olmap();
    }

    _init_olmap() {
        const olmapDiv = this.el.querySelector(".olmap_widget");
        if (olmapDiv) {
            olmapDiv.style.width = "100%";
            olmapDiv.style.height = "100%";
            const map = this._load_olmap();
            if (this.olmap) {
                map.setTarget(olmapDiv);
                this._ol_add_layer_vector();
                this.olmap.updateSize();
            }
        }
    }

    _load_olmap() {
        if (!this.olmap) {
            this.olmap = new ol.Map({
                layers: [
                    new ol.layer.Tile({
                        source: new ol.source.OSM(),
                    }),
                ],
                view: new ol.View({
                    center: ol.proj.fromLonLat([0, 0]),
                    zoom: 0,
                }),
            });
        }
        return this.olmap;
    }

    _ol_add_layer_vector() {
        if (this.olmap) {
            console.log(this.state.data);
            this.state.data.forEach((record) => {
                const value = record.data[this.drawingPath];
                if (value && Object.keys(value).length > 0) {
                    const parsedValue = JSON.parse(value);
                    const vectorSource = new ol.layer.Vector({
                        source: new ol.source.Vector({
                            features: new ol.format.GeoJSON().readFeatures(parsedValue),
                        }),
                        style: new ol.style.Style({
                            fill: new ol.style.Fill({
                                color: "rgb(255 235 59 / 62%)",
                            }),
                            stroke: new ol.style.Stroke({
                                color: "#ffc107",
                                width: 2,
                            }),
                            image: new ol.style.Circle({
                                radius: 7,
                                fill: new ol.style.Fill({
                                    color: "#ffc107",
                                }),
                            }),
                        }),
                    });
                    this.olmap.addLayer(vectorSource);
                }
            });
            this.olmap.updateSize();
        }
    }

    async updateState(state, params) {
        await super.updateState(state, params);
        if (this.olmap) {
            this._ol_add_layer_vector();
            this.olmap.updateSize();
        }
    }
}