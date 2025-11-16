from odoo import models, fields, api, _


class TMSAdvance(models.Model):
    _name = 'tms.advance'
    _description = 'TMS Advance Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )
    driver_id = fields.Many2one(
        'res.partner',
        string='Driver',
        required=True,
        domain=[('is_driver', '=', True)],
        tracking=True
    )
    travel_id = fields.Many2one(
        'tms.travel',
        string='Travel',
        tracking=True
    )
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
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('card', 'Card')
    ], string='Payment Method', required=True, default='cash', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('reconciled', 'Reconciled'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('tms.advance') or _('New')
        return super(TMSAdvance, self).create(vals)

    def action_pay(self):
        self.write({'state': 'paid'})

    def action_reconcile(self):
        self.write({'state': 'reconciled'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})
