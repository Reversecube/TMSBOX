from odoo import models, fields, api, _


class TMSUnit(models.Model):
    _name = 'tms.unit'
    _description = 'TMS Transport Unit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Unit Name',
        required=True,
        tracking=True
    )
    code = fields.Char(
        string='Code',
        required=True,
        tracking=True
    )
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Vehicle',
        tracking=True
    )
    unit_type = fields.Selection([
        ('truck', 'Truck'),
        ('trailer', 'Trailer'),
        ('container', 'Container'),
        ('van', 'Van'),
        ('other', 'Other')
    ], string='Unit Type', required=True, default='truck', tracking=True)
    
    capacity_weight = fields.Float(
        string='Weight Capacity (kg)',
        tracking=True
    )
    capacity_volume = fields.Float(
        string='Volume Capacity (m³)',
        tracking=True
    )
    license_plate = fields.Char(
        string='License Plate',
        tracking=True
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    state = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Maintenance'),
        ('out_of_service', 'Out of Service')
    ], string='Status', default='available', tracking=True)
    
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )
