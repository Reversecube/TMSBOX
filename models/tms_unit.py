from odoo import models, fields


class TMSUnit(models.Model):
    _name = 'tms.unit'
    _description = 'TMS Transport Unit'

    name = fields.Char('Unit Name', required=True)
    code = fields.Char('Code', required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle')
    unit_type = fields.Selection([
        ('truck', 'Truck'),
        ('trailer', 'Trailer'),
        ('container', 'Container'),
        ('van', 'Van'),
        ('other', 'Other')
    ], default='truck', required=True)
    capacity_weight = fields.Float('Weight Capacity (kg)')
    capacity_volume = fields.Float('Volume Capacity (m³)')
    license_plate = fields.Char('License Plate')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Maintenance'),
        ('out_of_service', 'Out of Service')
    ], default='available')
    notes = fields.Text('Notes')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
