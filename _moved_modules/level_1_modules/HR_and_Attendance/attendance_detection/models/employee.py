# -*- coding: utf-8 -*-

from datetime import date, datetime

import pytz
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrEmployeeChecksDeduction(models.Model):
    _inherit = "hr.employee"

    regular_check_in = fields.Boolean(
        string="Doesn't Use Attendance Application",
        help="Check if this employee does not use odoo attendance application to "
        "determine his status in Attendance Report",
    )
