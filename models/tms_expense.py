from odoo import models, fields


class TMSExpense(models.Model):
    _name = 'tms.expense'
    _description = 'TMS Expense'

    name = fields.Char('Description', required=True)
    date = fields.Date('Date', required=True, default=fields.Date.context_today)
    expense_type = fields.Selection([
        ('fuel', 'Fuel'),
        ('toll', 'Toll'),
        ('maintenance', 'Maintenance'),
        ('parking', 'Parking'),
        ('meal', 'Meal'),
        ('accommodation', 'Accommodation'),
        ('other', 'Other')
    ], required=True)
    amount = fields.Monetary('Amount', required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    travel_id = fields.Many2one('tms.travel', 'Travel')
    waybill_id = fields.Many2one('tms.waybill', 'Waybill')
    driver_id = fields.Many2one('res.partner', 'Driver')
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected')
    ], default='draft')
    notes = fields.Text('Notes')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
