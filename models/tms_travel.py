from odoo import models, fields, api


class TMSTravel(models.Model):
    _name = 'tms.travel'
    _description = 'TMS Travel'

    name = fields.Char('Travel Number', required=True, default='New')
    date_start = fields.Datetime('Start Date', required=True, default=fields.Datetime.now)
    date_end = fields.Datetime('End Date')
    driver_id = fields.Many2one('res.partner', 'Driver', required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', required=True)
    route_id = fields.Many2one('tms.route', 'Route')
    odometer_start = fields.Float('Starting Odometer')
    odometer_end = fields.Float('Ending Odometer')
    distance = fields.Float('Distance', compute='_compute_distance', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='draft')
    total_revenue = fields.Monetary('Total Revenue', compute='_compute_totals', store=True)
    total_expenses = fields.Monetary('Total Expenses', compute='_compute_totals', store=True)
    profit = fields.Monetary('Profit', compute='_compute_totals', store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    notes = fields.Text('Notes')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.depends('odometer_start', 'odometer_end')
    def _compute_distance(self):
        for record in self:
            if record.odometer_end and record.odometer_start:
                record.distance = record.odometer_end - record.odometer_start
            else:
                record.distance = 0.0

    @api.depends()
    def _compute_totals(self):
        for record in self:
            record.total_revenue = 0.0
            record.total_expenses = 0.0
            record.profit = 0.0
