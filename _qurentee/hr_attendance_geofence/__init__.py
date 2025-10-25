# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from . import models
from odoo.exceptions import UserError


# def pre_init_check(env):
#     server_serie = env['ir.config_parameter'].sudo().get_param('server_serie')
#     if not server_serie:
#         raise UserError(
#             "The 'server_serie' parameter is not set in the system. Please configure it to '18.0'."
#         )
#     if server_serie != '18.0':
#         raise UserError(
#             'Module supports Odoo series 18.0. Found {}.'.format(server_serie)
#         )
#     return True


def uninstall_hook(env):
    # Add logic for uninstall hook if needed
    pass