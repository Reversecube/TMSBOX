# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TmsWaybill(models.Model):
    _name = 'tms.waybill'
    _description = 'TMS Waybill'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char('Waybill Number', required=True, default='New', tracking=True)
    date = fields.Date('Date', required=True, default=fields.Date.context_today, tracking=True)
    partner_id = fields.Many2one('res.partner', 'Customer', required=True, tracking=True)
    driver_id = fields.Many2one('res.partner', 'Driver', tracking=True)
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', tracking=True)
    route_id = fields.Many2one('tms.route', 'Route', tracking=True)
    travel_id = fields.Many2one('tms.travel', 'Travel', tracking=True)
    origin = fields.Char('Origin', required=True, tracking=True)
    destination = fields.Char('Destination', required=True, tracking=True)
    cargo_description = fields.Text('Cargo Description')
    cargo_weight = fields.Float('Weight (kg)', digits=(12, 2))
    cargo_volume = fields.Float('Volume (m³)', digits=(12, 2))
    amount_total = fields.Monetary('Total Amount', compute='_compute_amount_total', store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], default='draft', string='Status', tracking=True, required=True)
    line_ids = fields.One2many('tms.waybill.line', 'waybill_id', 'Waybill Lines')
    notes = fields.Text('Notes')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)

    @api.depends('line_ids.subtotal')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(record.line_ids.mapped('subtotal'))

    def action_confirm(self):
        self.state = 'confirmed'

    def action_in_transit(self):
        self.state = 'in_transit'

    def action_deliver(self):
        self.state = 'delivered'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_reset_to_draft(self):
        self.state = 'draft'


class TmsWaybillLine(models.Model):
    _name = 'tms.waybill.line'
    _description = 'TMS Waybill Line'

    sequence = fields.Integer('Sequence', default=10)
    waybill_id = fields.Many2one('tms.waybill', 'Waybill', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    description = fields.Text('Description')
    quantity = fields.Float('Quantity', default=1.0, required=True, digits=(12, 2))
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price')
    subtotal = fields.Float('Subtotal', compute='_compute_subtotal', store=True)

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

    name = fields.Char('Route Name', required=True)
    code = fields.Char('Code')
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)


class TmsTravel(models.Model):
    _name = 'tms.travel'
    _description = 'TMS Travel'

    name = fields.Char('Travel Number', required=True, default='New')
    state = fields.Selection([('draft', 'Draft'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='draft')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

# from odoo import models, fields, api, _
# from odoo.exceptions import ValidationError


# class TMSWaybill(models.Model):
#     _name = 'tms.waybill'
#     _description = 'TMS Waybill'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _order = 'date desc, id desc'

#     name = fields.Char(
#         string='Waybill Number',
#         required=True,
#         copy=False,
#         readonly=True,
#         default=lambda self: _('New'),
#         tracking=True
#     )
#     date = fields.Date(
#         string='Date',
#         required=True,
#         default=fields.Date.context_today,
#         tracking=True
#     )
#     partner_id = fields.Many2one(
#         'res.partner',
#         string='Customer',
#         required=True,
#         tracking=True
#     )
#     driver_id = fields.Many2one(
#         'res.partner',
#         string='Driver',
#         domain=[('is_driver', '=', True)],
#         tracking=True
#     )
#     vehicle_id = fields.Many2one(
#         'fleet.vehicle',
#         string='Vehicle',
#         tracking=True
#     )
#     route_id = fields.Many2one(
#         'tms.route',
#         string='Route',
#         tracking=True
#     )
#     origin = fields.Char(
#         string='Origin Location',
#         required=True,
#         tracking=True
#     )
#     destination = fields.Char(
#         string='Destination',
#         required=True,
#         tracking=True
#     )
#     cargo_description = fields.Text(
#         string='Cargo Description',
#         tracking=True
#     )
#     cargo_weight = fields.Float(
#         string='Weight (kg)',
#         tracking=True
#     )
#     cargo_volume = fields.Float(
#         string='Volume (m³)',
#         tracking=True
#     )
#     amount_total = fields.Monetary(
#         string='Total Amount',
#         currency_field='currency_id',
#         compute='_compute_amount_total',
#         store=True
#     )
#     currency_id = fields.Many2one(
#         'res.currency',
#         string='Currency',
#         default=lambda self: self.env.company.currency_id
#     )
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('confirmed', 'Confirmed'),
#         ('in_transit', 'In Transit'),
#         ('delivered', 'Delivered'),
#         ('cancelled', 'Cancelled')
#     ], string='Status', default='draft', tracking=True)
    
#     line_ids = fields.One2many(
#         'tms.waybill.line',
#         'waybill_id',
#         string='Waybill Lines'
#     )
#     expense_ids = fields.One2many(
#         'tms.expense',
#         'waybill_id',
#         string='Expenses'
#     )
#     travel_id = fields.Many2one(
#         'tms.travel',
#         string='Related Travel',
#         tracking=True
#     )
#     notes = fields.Text(string='Notes')
#     company_id = fields.Many2one(
#         'res.company',
#         string='Company',
#         default=lambda self: self.env.company
#     )

#     @api.model
#     def create(self, vals):
#         if vals.get('name', _('New')) == _('New'):
#             vals['name'] = self.env['ir.sequence'].next_by_code('tms.waybill') or _('New')
#         return super(TMSWaybill, self).create(vals)

#     @api.depends('line_ids.subtotal')
#     def _compute_amount_total(self):
#         for record in self:
#             record.amount_total = sum(record.line_ids.mapped('subtotal'))

#     def action_confirm(self):
#         self.write({'state': 'confirmed'})

#     def action_in_transit(self):
#         self.write({'state': 'in_transit'})

#     def action_deliver(self):
#         self.write({'state': 'delivered'})

#     def action_cancel(self):
#         self.write({'state': 'cancelled'})

#     def action_reset_to_draft(self):
#         self.write({'state': 'draft'})


# class TMSWaybillLine(models.Model):
#     _name = 'tms.waybill.line'
#     _description = 'TMS Waybill Line'

#     waybill_id = fields.Many2one(
#         'tms.waybill',
#         string='Waybill',
#         required=True,
#         ondelete='cascade'
#     )
#     product_id = fields.Many2one(
#         'product.product',
#         string='Product/Service',
#         required=True
#     )
#     description = fields.Text(string='Description')
#     quantity = fields.Float(
#         string='Quantity',
#         default=1.0,
#         required=True
#     )
#     uom_id = fields.Many2one(
#         'uom.uom',
#         string='Unit of Measure',
#         related='product_id.uom_id'
#     )
#     price_unit = fields.Float(
#         string='Unit Price',
#         required=True
#     )
#     subtotal = fields.Float(
#         string='Subtotal',
#         compute='_compute_subtotal',
#         store=True
#     )
#     currency_id = fields.Many2one(
#         related='waybill_id.currency_id',
#         string='Currency'
#     )

#     @api.depends('quantity', 'price_unit')
#     def _compute_subtotal(self):
#         for line in self:
#             line.subtotal = line.quantity * line.price_unit

#     @api.onchange('product_id')
#     def _onchange_product_id(self):
#         if self.product_id:
#             self.price_unit = self.product_id.list_price
#             self.description = self.product_id.name
