/** @odoo-module **/


// odoo.define('hr_attendance_geofence.GeofenceView', function (require) {
//     'use strict';

//     var BasicView = require('web.BasicView');
//     var GeofenceCommon = require('hr_attendance_geofence.GeofenceCommon');
//     var core = require('web.core');

//     var GeofenceModel = require('hr_attendance_geofence.GeofenceModel');
//     var GeofenceRenderer = require('hr_attendance_geofence.GeofenceRenderer');
//     var GeofenceController = require('hr_attendance_geofence.GeofenceController');

//     var view_registry = require('web.view_registry');

//     var _lt = core._lt;

//     var GeofenceView = BasicView.extend(GeofenceCommon.GeofenceCommon,{
//         accesskey: 'm',
//         display_name: _lt('Attendance Geofence'),
//         icon: 'fa fa-map-o',
//         config: _.extend({}, BasicView.prototype.config, {
//             Model: GeofenceModel,
//             Renderer: GeofenceRenderer,
//             Controller: GeofenceController,
//         }),
//         viewType: 'geofence_view',
//         mobile_friendly: true,
//         searchMenuTypes: [],
//         withSearchBar: false,

//         init: function (viewInfo, params) {
//             this._super.apply(this, arguments);

//             var arch = this.arch;
//             var attrs = arch.attrs;

//             var activeActions = this.controllerParams.activeActions;
//             var mode = arch.attrs.editable && !params.readonly ? "edit" : "readonly";

//             this.loadParams.limit = this.loadParams.limit || 80;
//             this.loadParams.openGroupByDefault = true;
//             this.loadParams.type = 'list';

//             this.loadParams.groupBy = arch.attrs.default_group_by ? [arch.attrs.default_group_by] : (params.groupBy || []);

//             this.rendererParams.arch = arch;
//             this.rendererParams.drawingPath = attrs.drawing_path;

//             this.rendererParams.record_options = {
//                 editable: activeActions.edit,
//                 deletable: activeActions.delete,
//                 read_only_mode: params.readOnlyMode || true,
//             };

//             this.controllerParams.mode = mode;
//             this.controllerParams.hasButtons = true;
//         }
//     });
//     view_registry.add('geofence_view', GeofenceView);
//     return GeofenceView;
// });
//this is my first edit



import { BasicView } from "@web/views/basic/basic_view";
import { registry } from "@web/core/registry";
import { GeofenceModel } from "./geofence_model";
import { GeofenceRenderer } from "./geofence_renderer";
import { GeofenceController } from "./geofence_controller";

export class GeofenceView extends BasicView {
    static viewType = "geofence_view";
    static display_name = "Attendance Geofence";
    static icon = "fa fa-map-o";

    static components = {
        Model: GeofenceModel,
        Renderer: GeofenceRenderer,
        Controller: GeofenceController,
    };

    constructor(viewInfo, params) {
        super(viewInfo, params);

        const arch = this.arch;
        const attrs = arch.attrs;

        const activeActions = this.controllerParams.activeActions;
        const mode = arch.attrs.editable && !params.readonly ? "edit" : "readonly";

        this.loadParams.limit = this.loadParams.limit || 80;
        this.loadParams.openGroupByDefault = true;
        this.loadParams.type = "list";

        this.loadParams.groupBy = arch.attrs.default_group_by
            ? [arch.attrs.default_group_by]
            : params.groupBy || [];

        this.rendererParams.arch = arch;
        this.rendererParams.drawingPath = attrs.drawing_path;

        this.rendererParams.record_options = {
            editable: activeActions.edit,
            deletable: activeActions.delete,
            read_only_mode: params.readOnlyMode || true,
        };

        this.controllerParams.mode = mode;
        this.controllerParams.hasButtons = true;
    }
}

// Register the view in the registry
registry.category("views").add("geofence_view", GeofenceView);