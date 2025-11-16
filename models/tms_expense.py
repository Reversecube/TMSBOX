from odoo import models, fields, api, _


class TMSExpense(models.Model):
    _name = 'tms.expense'
    _description = 'TMS Expense'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Description',
        required=True,
        tracking=True
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )
    expense_type = fields.Selection([
        ('fuel', 'Fuel'),
        ('toll', 'Toll'),
        ('maintenance', 'Maintenance'),
        ('parking', 'Parking'),
        ('meal', 'Meal'),
        ('accommodation', 'Accommodation'),
        ('other', 'Other')
    ], string='Expense Type', required=True, tracking=True)
    
    amount = fields.Monetary(
        string='Amount',
        required=True,
        currency_field='currency_id',
        tracking=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    travel_id = fields.Many2one(
        'tms.travel',
        string='Travel',
        tracking=True
    )
    waybill_id = fields.Many2one(
        'tms.waybill',
        string='Waybill',
        tracking=True
    )
    driver_id = fields.Many2one(
        'res.partner',
        string='Driver',
        domain=[('is_driver', '=', True)],
        tracking=True
    )
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Vehicle',
        tracking=True
    )
    invoice_id = fields.Many2one(
        'account.move',
        string='Vendor Bill',
        tracking=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)
    
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_pay(self):
        self.write({'state': 'paid'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
