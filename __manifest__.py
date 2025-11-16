{
    'name': 'TMSBOX By Reversecube',
    'version': '18.0.1.0.0',
    'category': 'Transport/Logistics',
    'summary': 'Complete Transportation Management System for Fleet, Waybills, Travel, Routes & Expenses',
    'description': """
        TMSBOX - Transportation Management System
        ==========================================
        
        Complete TMS solution featuring:
        * Waybill Management
        * Travel & Route Planning
        * Expense & Advance Tracking
        * Fleet & Unit Management
        * Driver Assignment
        * Customer & Supplier Integration
        * Multi-currency Support
        * Advanced Reporting
        
        Developed by Reversecube
    """,
    'author': 'Reversecube',
    'website': 'https://www.reversecube.net',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'fleet',
        'contacts',
        'account',
        'stock',
        'product',
        'hr_expense',
        'sale',
        'purchase',
    ],
    'data': [
        # 1. Security groups FIRST
        'security/tms_security.xml',
        
        # 2. Data/sequences BEFORE views (models created via Python, not XML)
        'data/tms_sequence.xml',
        
        # 3. Views - This creates the models in the database
        'views/tms_waybill_views.xml',
        'views/tms_travel_views.xml',
        'views/tms_route_views.xml',
        'views/tms_unit_views.xml',
        'views/tms_expense_views.xml',
        'views/tms_advance_views.xml',
        'views/tms_menus.xml',
        
        # 4. Access rights CSV - AFTER views (models must exist)
        'security/ir.model.access.csv',
    ],
    'demo': [],
    # Assets (if you have custom CSS/JS)
    'assets': {
        'web.assets_backend': [
            # 'tmsbox_reversecube/static/src/css/tmsbox.css',
            # 'tmsbox_reversecube/static/src/js/tmsbox.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/icon.png'],
}
