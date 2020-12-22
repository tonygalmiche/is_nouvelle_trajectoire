# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'


    def _compute_sportif_count(self):
        for obj in self:
            nb = self.search_count([('is_club_id', '=', obj.id)])
            obj.is_sportif_count = nb


    def _compute_club_sportif_count(self):
        for obj in self:
            nb = self.search_count([('is_financeur_ids', '=', obj.id)])
            obj.is_club_sportif_count = nb


    is_prenom = fields.Char("Prénom", size=255)
    is_createur_id = fields.Many2one('res.users', 'Créateur de la fiche', required=False)
    is_club_id = fields.Many2one('res.partner', 'Club', required=False)
    is_federation_id = fields.Many2one('res.partner', 'Fédération', required=False)
    is_syndicat_id = fields.Many2one('res.partner', 'Syndicat', required=False)
    is_financeur_ids = fields.Many2many(
        'res.partner',
        'res_partner_financeur_rel',
        'partner_id',
        'financeur_id',
        'Financeurs')
    is_facebook =  fields.Char("Facebook", size=255)
    is_region_id = fields.Many2one('is.region', 'Région', required=False)
    is_type_contact = fields.Selection([
            ('club'                     , 'Club'),
            ('sportif'                  , 'Sportif'),
            ('financeur_institutionnel' , 'Financeur institutionnel'),
            ('financeur_prive'          , 'Financeur privé'),
            ('federation_ligue'         , 'Fédération - Ligue'),
            ('syndicat'                 , 'Syndicat'),
            ('ambassadeur'              , "Ambassadeur"),
            ('messager'                 , "Messager"),
        ],
        'Type de contact', required=False)
    is_referent_id = fields.Many2one('res.users', 'Référent', required=False)

    # Club
    is_sport_id = fields.Many2one('is.sport', 'Sport', required=False)
    is_niveau_id = fields.Many2one('is.niveau', 'Niveau', required=False)
    is_statut_id = fields.Many2one('is.statut', 'Statut contractuel', required=False)
    is_opca1 =  fields.Char("OPCA 1")
    is_opca2 =  fields.Char("OPCA 2")
    reseaux_sociaux = fields.Text('Réseaux sociaux', required=False)
    is_nb_salaries = fields.Selection([('10', '-10'), ('49', '10-49'), ('999', '49 et +')], 'Nombre de salariés')
    is_budget_annuel = fields.Integer("Budget annuel")
    is_budget_formation = fields.Integer("Budget formation")
    is_centre_formation = fields.Selection([('oui', 'Oui'), ('non', 'Non')], 'Centre de formation')
    is_cellule_reconversion = fields.Selection([('oui', 'Oui'), ('non', 'Non')], 'Cellule de reconversion')
    is_nature_besoins = fields.Text('Nature des besoins et attentes')
    is_informations_complementaires = fields.Text('Informations complémentaires')
    is_sportif_count = fields.Integer(compute=_compute_sportif_count                  , string='# Sportifs'    )
    is_club_sportif_count = fields.Integer(compute=_compute_club_sportif_count, string='# Club/Sportif')
    is_apporteur_affaire_id = fields.Many2one('res.partner', 'Apporteur affaire', required=False)
    is_date_qualification = fields.Date('Date de qualification du client')

    # Sportif
    is_dernieres_saisons = fields.Text('3 dernières saisons')
    is_date_naissance = fields.Date('Date de naissance')
    is_statut_sportif_id = fields.Many2one('is.statut.sportif', 'Statut du sportif')
    is_situation_familiale =  fields.Char("Situation familiale")
    is_niveau_etude =  fields.Char("Niveau d'études")
    is_situation_contractuelle =  fields.Char("Situation contractuelle")
    is_remuneration_annuelle = fields.Integer("Rémunération annuelle")
    is_raison_fin_carriere =  fields.Text("Raison fin de carrière")
    is_projet =  fields.Char("Projet")
    is_nationalite_id = fields.Many2one('res.country', 'Nationalité', ondelete='restrict')

    #Financeur Institution
    is_referencement = fields.Selection([('oui', 'Oui'), ('non', 'Non')], 'Référencement')
    is_agrement = fields.Selection([('oui', 'Oui'), ('non', 'Non')], 'Agrément')
    is_historique_financement =  fields.Text("Historique des financements")

    #Financeur Privé
    is_siret =  fields.Char("Siret")
    is_activite =  fields.Char("Activité")
    is_ca = fields.Integer("CA")

    is_taxe_apprentissage = fields.Selection([('oui', 'Oui'), ('non', 'Non')], "Taxe d'apprentissage versée au club")
    is_prise_en_charge_sportif = fields.Selection([('oui', 'Oui'), ('non', 'Non')], "Prise en charge sportif")

    #Fédérations / Ligues ou  Syndicats ou Apporteur d'affaires
    is_historique_nt = fields.Selection([('oui', 'Oui'), ('non', 'Non')], 'Historique NT')

    #Ambassadeur
    is_contrat_nt = fields.Selection([('oui', 'Oui'), ('non', 'Non')], 'Contrat NT')
    is_date_fin_contrat = fields.Date('Date de fin de contrat')
    is_couverture_geographique = fields.Selection([('national', 'National'), ('regional', 'Régional'), ('departemental', 'Départemental')], 'Couverture géographique')
    is_nb_contacts = fields.Integer("Nb Contacts")
    is_objectif_contact = fields.Integer("Objectif contact")
    is_objectif_contrat = fields.Integer("Contrat objectif affaire")

    #Messager
    is_rattachement_nt =  fields.Char("Rattachement NT")
    is_prochaine_action =  fields.Date("Prochaine action")
    is_type_action =  fields.Char("Type d'action")


    # _defaults = {
    #     'is_createur_id = lambda obj, cr, uid, ctx=None: uid,
    # }


class is_region(models.Model):
    _name = 'is.region'
    _description = u"Région"
    name = fields.Char("Région", required=True)


class is_sport(models.Model):
    _name = 'is.sport'
    _description = "Sport"
    name = fields.Char("Sport", required=True)


class is_niveau(models.Model):
    _name = 'is.niveau'
    _description = "Niveau"
    name = fields.Char("Niveau", required=True)


class is_statut(models.Model):
    _name = 'is.statut'
    _description = "Statut contractuel"
    name = fields.Char("Statut", required=True)


class is_statut_sportif(models.Model):
    _name = 'is.statut.sportif'
    _description = "Statut du sportif"
    name = fields.Char("Statut du sportif", required=True)


class is_base_documentaire(models.Model):
    _name = 'is.base.documentaire'
    _description = "Base documentaire"
    name = fields.Char("Nom du document", required=True)
