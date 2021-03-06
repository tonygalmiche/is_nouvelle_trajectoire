# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'



    @api.model
    def _calculer_suivi_activite_ir_cron(self):
        self.env['res.partner'].search([('is_budget_previsionnel','>',0)])._compute_suivi_activite()
        return True


    def _calculer_suivi_activite_action(self):
        self.browse(self.env.context['active_ids'])._compute_suivi_activite()
 

    def _compute_sportif_count(self):
        for obj in self:
            nb = self.search_count([('is_club_id', '=', obj.id)])
            obj.is_sportif_count = nb


    def _compute_club_sportif_count(self):
        for obj in self:
            nb = self.search_count([('is_financeur_ids', '=', obj.id)])
            obj.is_club_sportif_count = nb


    @api.depends('is_type_contact','parent_id.is_type_contact')
    def _compute_group_id(self):
        for obj in self:
            name="sales_team.group_sale_manager"
            type_contact=False
            if obj.is_type_contact:
                type_contact = obj.is_type_contact
            else:
                if obj.parent_id.is_type_contact:
                    type_contact = obj.parent_id.is_type_contact
            if type_contact:
                name="is_nouvelle_trajectoire.is_group_"+type_contact
            grp = self.env.ref(name)
            if grp.id:
                obj.is_group_id=grp.id


    @api.depends('is_suivi_activite_ids')
    def _compute_suivi_activite_count(self):
        for obj in self:
            nb = len(obj.is_suivi_activite_ids)
            obj.is_suivi_activite_count=nb


    @api.depends('is_suivi_activite_ids','is_budget_previsionnel')
    def _compute_suivi_activite(self):
        for obj in self:
            nb=len(self.env['is.suivi.activite'].search([('partner_id','=',obj.id),('date_realisee','=',False)]))
            obj.is_nb_activite_en_cours=nb
            nb=len(self.env['is.suivi.activite'].search([('partner_id','=',obj.id),('date_realisee','!=',False)]))
            obj.is_nb_activite_terminee=nb
            ca = obj.get_total_facture()
            obj.is_total_facture = ca
            ecart = ca - obj.is_budget_previsionnel
            obj.is_ecart_budget = ecart
            d = obj.get_date_derniere_activite()
            obj.is_date_derniere_activite = d
            limite = date.today() + relativedelta(months=-6)
            alerte=False
            if obj.is_budget_previsionnel and d and d<limite:
                alerte = "Pas d'activité depuis 6 mois"
            if obj.is_budget_previsionnel and nb==0:
                alerte = "Pas d'activité"
            obj.is_alerte_activite=alerte


    def get_total_facture(self):
        for obj in self:
            ca=0
            if type(obj.id) == int:
                sql = """
                    SELECT sum(amount_untaxed_signed) 
                    FROM account_move 
                    WHERE move_type in ('out_invoice','out_refund') and state='posted' and partner_id=%s
                """
                self.env.cr.execute(sql,[obj.id])
                res = self._cr.fetchall()
                for line in res:
                    ca=line[0] or 0
            return ca


    def get_date_derniere_activite(self):
        for obj in self:
            d = False
            for line in obj.is_suivi_activite_ids:
                if line.date_realisee:
                    if not d or line.date_realisee>d:
                        d=line.date_realisee
            return d


    is_prenom = fields.Char("Prénom", size=255)
    is_createur_id = fields.Many2one('res.users', 'Créateur de la fiche', required=False, default=lambda self: self.env.user)
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
            ('entreprise'               , "Entreprise"),
        ],
        'Type de contact', required=False)

    is_group_id = fields.Many2one('res.groups', 'Groupe', compute='_compute_group_id', store=True)


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

    #Suivi activité / Budget
    is_suivi_activite_ids     = fields.One2many('is.suivi.activite', 'partner_id', "Suivi d'activité")
    is_budget_previsionnel    = fields.Integer("Budget prévisionnel")
    is_suivi_activite_count   = fields.Integer(compute=_compute_suivi_activite_count, string="# Suivi d'activité")
    is_nb_activite_en_cours   = fields.Integer(compute=_compute_suivi_activite      , string="Nb activités en cours", store=True, readonly=True)
    is_nb_activite_terminee   = fields.Integer(compute=_compute_suivi_activite      , string="Nb activités terminée", store=True, readonly=True)
    is_total_facture          = fields.Integer(compute=_compute_suivi_activite      , string="Total facturé"        , store=True, readonly=True)
    is_ecart_budget           = fields.Integer(compute=_compute_suivi_activite      , string="Ecart budget"         , store=True, readonly=True)
    is_alerte_activite        = fields.Text(   compute=_compute_suivi_activite      , string="Alerte"               , store=True, readonly=True)
    is_date_derniere_activite = fields.Date(   compute=_compute_suivi_activite      , string="Dernière activité"    , store=True, readonly=True)


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
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Base documentaire"
    name = fields.Char("Nom du document", required=True)
