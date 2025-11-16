# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TmsWaybill(models.Model):
    _name = 'tms.waybill'
    _description = 'TMS Waybill'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Waybill Number', required=True, default='New')
    date = fields.Date('Date', required=True, default=fields.Date.context_today)
    partner_id = fields.Many2one('res.partner', 'Customer', required=True)
    driver_id = fields.Many2one('res.partner', 'Driver')
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle')
    route_id = fields.Many2one('tms.route', 'Route')
    travel_id = fields.Many2one('tms.travel', 'Travel')
    origin = fields.Char('Origin', required=True)
    destination = fields.Char('Destination', required=True)
    cargo_description = fields.Text('Cargo Description')
    cargo_weight = fields.Float('Weight (kg)')
    cargo_volume = fields.Float('Volume (m³)')
    amount_total = fields.Monetary('Total Amount', compute='_compute_amount_total', store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
    ], default='draft', string='Status')
    line_ids = fields.One2many('tms.waybill.line', 'waybill_id', 'Waybill Lines')
    notes = fields.Text('Notes')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.depends('line_ids.subtotal')
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(record.line_ids.mapped('subtotal'))


class TmsWaybillLine(models.Model):
    _name = 'tms.waybill.line'
    _description = 'TMS Waybill Line'

    waybill_id = fields.Many2one('tms.waybill', 'Waybill', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    description = fields.Text('Description')
    quantity = fields.Float('Quantity', default=1.0, required=True)
    price_unit = fields.Float('Unit Price', required=True)
    subtotal = fields.Float('Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit


class TmsRoute(models.Model):
    _name = 'tms.route'
    _description = 'TMS Route'

    name = fields.Char('Route Name', required=True)


class TmsTravel(models.Model):
    _name = 'tms.travel'
    _description = 'TMS Travel'

    name = fields.Char('Travel Number', required=True)
