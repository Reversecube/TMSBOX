from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TMSTravel(models.Model):
    _name = 'tms.travel'
    _description = 'TMS Travel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, id desc'

    name = fields.Char(
        string='Travel Number',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )
    date_start = fields.Datetime(
        string='Start Date',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )
    date_end = fields.Datetime(
        string='End Date',
        tracking=True
    )
    driver_id = fields.Many2one(
        'res.partner',
        string='Driver',
        required=True,
        domain=[('is_driver', '=', True)],
        tracking=True
    )
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Vehicle',
        required=True,
        tracking=True
    )
    route_id = fields.Many2one(
        'tms.route',
        string='Route',
        tracking=True
    )
    waybill_ids = fields.One2many(
        'tms.waybill',
        'travel_id',
        string='Waybills'
    )
    expense_ids = fields.One2many(
        'tms.expense',
        'travel_id',
        string='Expenses'
    )
    advance_ids = fields.One2many(
        'tms.advance',
        'travel_id',
        string='Advances'
    )
    odometer_start = fields.Float(
        string='Starting Odometer (km)',
        tracking=True
    )
    odometer_end = fields.Float(
        string='Ending Odometer (km)',
        tracking=True
    )
    distance = fields.Float(
        string='Distance (km)',
        compute='_compute_distance',
        store=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    total_revenue = fields.Monetary(
        string='Total Revenue',
        compute='_compute_totals',
        store=True
    )
    total_expenses = fields.Monetary(
        string='Total Expenses',
        compute='_compute_totals',
        store=True
    )
    total_advances = fields.Monetary(
        string='Total Advances',
        compute='_compute_totals',
        store=True
    )
    profit = fields.Monetary(
        string='Profit',
        compute='_compute_totals',
        store=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('tms.travel') or _('New')
        return super(TMSTravel, self).create(vals)

    @api.depends('odometer_start', 'odometer_end')
    def _compute_distance(self):
        for record in self:
            if record.odometer_end and record.odometer_start:
                record.distance = record.odometer_end - record.odometer_start
            else:
                record.distance = 0.0

    @api.depends('waybill_ids.amount_total', 'expense_ids.amount', 'advance_ids.amount')
    def _compute_totals(self):
        for record in self:
            record.total_revenue = sum(record.waybill_ids.mapped('amount_total'))
            record.total_expenses = sum(record.expense_ids.mapped('amount'))
            record.total_advances = sum(record.advance_ids.mapped('amount'))
            record.profit = record.total_revenue - record.total_expenses

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_start(self):
        self.write({'state': 'in_progress', 'date_start': fields.Datetime.now()})

    def action_complete(self):
        self.write({'state': 'completed', 'date_end': fields.Datetime.now()})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
