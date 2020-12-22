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
    ], 
    "init_xml" : [],
    "demo_xml" : [],
    "data" : [
        "security/partner_access_data.xml",
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
    ],
    "installable": True,
    "active": False,
    "application": True,
}
