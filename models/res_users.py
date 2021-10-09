# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_code_couleur = fields.Char("Code couleur", help="Champ utilisé dans le suivi des presations")
