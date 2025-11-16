# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TmsWaybill(models.Model):
    _name = 'tms.waybill'
    _description = 'TMS Waybill'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Waybill Number',
        required=True,
        default='New',
        tracking=True
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        tracking=True
    )
    driver_id = fields.Many2one(
        'res.partner',
        string='Driver',
        tracking=True
    )
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Vehicle',
        tracking=True
    )
    route_id = fields.Many2one(
        'tms.route',
        string='Route',
        tracking=True
    )
    travel_id = fields.Many2one(
        'tms.travel',
        string='Travel',
        tracking=True
    )
    origin = fields.Char(
        string='Origin',
        required=True,
        tracking=True
    )
    destination = fields.Char(
        string='Destination',
        required=True,
        tracking=True
    )
    cargo_description = fields.Text(
        string='Cargo Description'
    )
    cargo_weight = fields.Float(
        string='Weight (kg)',
        digits=(12, 2)
    )
    cargo_volume = fields.Float(
        string='Volume (m³)',
        digits=(12, 2)
    )
    amount_total = fields.Monetary(
        string='Total Amount',
        currency_field='currency_id',
        compute='_compute_amount_total',
        store=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        required=True
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('in_transit', 'In Transit'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        default='draft',
        tracking=True,
        required=True
    )
    line_ids = fields.One2many(
        'tms.waybill.line',
        'waybill_id',
        string='Waybill Lines'
    )
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    @api.depends('line_ids.subtotal')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(record.line_ids.mapped('subtotal'))

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_in_transit(self):
        for rec in self:
            rec.state = 'in_transit'

    def action_deliver(self):
        for rec in self:
            rec.state = 'delivered'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'


class TmsWaybillLine(models.Model):
    _name = 'tms.waybill.line'
    _description = 'TMS Waybill Line'
    _order = 'waybill_id, sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    waybill_id = fields.Many2one(
        'tms.waybill',
        string='Waybill',
        required=True,
        ondelete='cascade'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )
    description = fields.Text(string='Description')
    quantity = fields.Float(
        string='Quantity',
        default=1.0,
        required=True,
        digits=(12, 2)
    )
    price_unit = fields.Float(
        string='Unit Price',
        required=True,
        digits='Product Price'
    )
    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
        digits='Product Price'
    )

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.list_price
            self.description = self.product_id.name


class TmsRoute(models.Model):
    _name = 'tms.route'
    _description = 'TMS Route'
    _order = 'name'

    name = fields.Char(string='Route Name', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company
    )


class TmsTravel(models.Model):
    _name = 'tms.travel'
    _description = 'TMS Travel'
    _order = 'name desc'

    name = fields.Char(string='Travel Number', required=True, default='New')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='draft', string='Status')
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company
    )
