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

    createur_id           = fields.Many2one('res.users'  , 'Créateur', readonly=True,default=lambda self: self.env.user, index=True)
    type_activite_id      = fields.Many2one('is.suivi.activite.type', "Libellé", required=True, index=True)
    partner_id            = fields.Many2one('res.partner', 'Client'  , required=True, index=True)
    date_prevue           = fields.Date('Date prévue'                , required=True, index=True)
    date_prochaine_action = fields.Date('Date prochaine action'      , required=True, index=True)
    date_realisee         = fields.Date('Date réalisée'                             , index=True)
    scoring               = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),], 'Scoring')
    commentaire           = fields.Text('Commentaire')
