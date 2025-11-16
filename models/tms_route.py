from odoo import models, fields, api, _


class TMSRoute(models.Model):
    _name = 'tms.route'
    _description = 'TMS Route'
    _order = 'name'

    name = fields.Char(
        string='Route Name',
        required=True
    )
    code = fields.Char(string='Code')
    origin = fields.Char(
        string='Origin',
        required=True
    )
    destination = fields.Char(
        string='Destination',
        required=True
    )
    distance = fields.Float(
        string='Distance (km)',
        required=True
    )
    estimated_duration = fields.Float(
        string='Estimated Duration (hours)'
    )
    waypoint_ids = fields.One2many(
        'tms.route.waypoint',
        'route_id',
        string='Waypoints'
    )
    active = fields.Boolean(
        string='Active',
        default=True
    )
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )


class TMSRouteWaypoint(models.Model):
    _name = 'tms.route.waypoint'
    _description = 'TMS Route Waypoint'
    _order = 'sequence, id'

    route_id = fields.Many2one(
        'tms.route',
        string='Route',
        required=True,
        ondelete='cascade'
    )
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(
        string='Waypoint Name',
        required=True
    )
    distance_from_origin = fields.Float(
        string='Distance from Origin (km)'
    )
    notes = fields.Text(string='Notes')
