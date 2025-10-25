from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    company_latitude = fields.Float(
        string="Company Latitude",
        config_parameter="hr_attendance_location.company_latitude",
    )
    company_longitude = fields.Float(
        string="Company Longitude",
        config_parameter="hr_attendance_location.company_longitude",
    )
    allowed_distance = fields.Float(
        string="Allowed Distance",
        config_parameter="hr_attendance_location.allowed_distance",
    )
