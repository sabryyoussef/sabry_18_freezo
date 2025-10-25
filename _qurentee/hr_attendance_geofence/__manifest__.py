# -*- coding: utf-8 -*-
#################################################################################
# Author      : CFIS (<https://www.cfis.store/>)
# Copyright(c): 2017-Present CFIS.
# All Rights Reserved.
#
# Migration to Odoo 18 by Sabry Youssef for Freezoner Company.
#################################################################################

{
    "name": "HR Attendance Geofence",
    "version": "18.0.1.0.0",
    "category": "Human Resources/Attendances",
    "summary": "Geofencing for HR Attendance",
    "description": """
        This module adds geofencing capabilities to HR Attendance.
        It allows you to define geofences and track employee attendance within those areas.
    """,
    "depends": ["hr_attendance"],
    "data": [
        "security/ir.model.access.csv",
        "data/geolocation_data.xml",
        "views/hr_attendance_geofence.xml",
        "views/hr_attendance_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "hr_attendance_geofence/static/src/views/attendance_geofence_view.js",
            "hr_attendance_geofence/static/src/views/attendance_geofence_view.xml",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
