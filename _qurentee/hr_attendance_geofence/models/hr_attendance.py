from odoo import fields, models


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    check_in_latitude = fields.Float(
        "Check-in Latitude", digits=(16, 10), readonly=True
    )
    check_in_longitude = fields.Float(
        "Check-in Longitude", digits=(16, 10), readonly=True
    )
    check_in_geofence_ids = fields.Many2many(
        "hr.attendance.geofence",
        "check_in_geofence_attendance_rel",
        "attendance_id",
        "geofence_id",
        string="Check-in Geofences",
    )

    check_out_latitude = fields.Float(
        "Check-out Latitude", digits=(16, 10), readonly=True
    )
    check_out_longitude = fields.Float(
        "Check-out Longitude", digits=(16, 10), readonly=True
    )
    check_out_geofence_ids = fields.Many2many(
        "hr.attendance.geofence",
        "check_out_geofence_attendance_rel",
        "attendance_id",
        "geofence_id",
        string="Check-out Geofences",
    )
