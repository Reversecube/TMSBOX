from odoo import models, fields


class TMSRoute(models.Model):
    _name = 'tms.route'
    _description = 'TMS Route'

    name = fields.Char('Route Name', required=True)
    code = fields.Char('Code')
    origin = fields.Char('Origin', required=True)
    destination = fields.Char('Destination', required=True)
    distance = fields.Float('Distance (km)', required=True)
    estimated_duration = fields.Float('Estimated Duration (hours)')
    waypoint_ids = fields.One2many('tms.route.waypoint', 'route_id', 'Waypoints')
    active = fields.Boolean('Active', default=True)
    notes = fields.Text('Notes')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)


class TMSRouteWaypoint(models.Model):
    _name = 'tms.route.waypoint'
    _description = 'TMS Route Waypoint'

    route_id = fields.Many2one('tms.route', 'Route', required=True, ondelete='cascade')
    sequence = fields.Integer('Sequence', default=10)
    name = fields.Char('Waypoint Name', required=True)
    distance_from_origin = fields.Float('Distance from Origin (km)')
    notes = fields.Text('Notes')
