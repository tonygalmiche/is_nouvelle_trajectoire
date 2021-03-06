# -*- coding: utf-8 -*-
from odoo import api, fields, models


class IsSuiviActiviteType(models.Model):
    _name = 'is.suivi.activite.type'
    _description = "Type d'activité"
    _order='name'

    name = fields.Char("Type d'activité", required=True)


class IsSuiviActivite(models.Model):
    _name = 'is.suivi.activite'
    _description = "Suivi activité"
    _order='date_prevue desc'

    createur_id      = fields.Many2one('res.users'  , 'Créateur', readonly=True,default=lambda self: self.env.user, index=True)
    type_activite_id = fields.Many2one('is.suivi.activite.type', "Type d'activité", required=True, index=True)
    partner_id       = fields.Many2one('res.partner', 'Client'  , required=True, index=True)
    date_prevue      = fields.Date('Date prévue', required=True, index=True)
    date_realisee    = fields.Date('Date réalisée', index=True)
    commentaire      = fields.Text('Commentaire')
