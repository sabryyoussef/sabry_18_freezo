from odoo import models

class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    def get_view_info(self):
        res = super().get_view_info()
        res['geofence_view'] = {
            'icon': 'fa fa-map-marker',
            'template': 'hr_attendance_geofence.GeofenceViewTemplate',
        }
        return res
