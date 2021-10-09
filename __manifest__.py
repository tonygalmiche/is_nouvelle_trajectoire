# -*- coding: utf-8 -*-
{
    "name" : "InfoSaône - Module Odoo 14 pour Nouvelle Trajectoire",
    "version" : "0.1",
    "author" : "InfoSaône / Tony Galmiche",
    "category" : "InfoSaône",
    "description": """
    InfoSaône - Module Odoo 14 pour Nouvelle Trajectoire
    ===================================================
    InfoSaône - Module Odoo 14 pour Nouvelle Trajectoire
    """,
    "maintainer": "InfoSaône",
    "website": "https://infosaone.com",
    "depends" : [
        "base",
        "mail",
        "calendar",               # Agenda
        "crm",                    # CRM
        "sale",                   # Gestion des ventes
        "purchase",               # Gestion des achats
        "project",                # Gestin de projets
        "hr",                     # Répertoire des employés
        "board",
        "hr_attendance",
        "hr_timesheet",
        "sale_crm",
        "sale_stock",
        "stock",
        "stock_account",
        "crm_phonecall",
    ], 
    "init_xml" : [],
    "demo_xml" : [],
    "data" : [
        "security/res.groups.xml",
        "security/partner_access_data.xml",
        "security/ir.model.access.csv",
        "views/is_suivi_activite_view.xml",
        "views/res_users_views.xml",
        "views/res_partner_view.xml",
        "views/res_partner_data.xml",
        "views/menu.xml",
        "views/report_suivi_prestation.xml",
    ],
    "installable": True,
    "active": False,
    "application": True,
}
