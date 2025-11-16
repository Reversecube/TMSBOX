# -*- coding: utf-8 -*-
{
    'name': 'TMSBOX By Reversecube',
    'version': '18.0.1.0.0',
    'category': 'Transport/Logistics',
    'summary': 'Transportation Management System for Odoo 18',
    'description': """
        TMSBOX - Transportation Management System
        ==========================================
        Complete TMS solution for logistics and fleet management.
    """,
    'author': 'Reversecube',
    'website': 'https://www.reversecube.net',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'fleet',
        'product',
    ],
    'data': [
        'security/tms_security.xml',
        'security/ir.model.access.csv',
        'views/tms_waybill_views.xml',
        'views/tms_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
