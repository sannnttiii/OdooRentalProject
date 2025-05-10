from odoo import models,fields, api
from babel.dates import format_date
from datetime import datetime, timedelta
import logging
from odoo.exceptions import ValidationError,UserError

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order Vendor',
        tracking=True,
    )
    customer_phone = fields.Char(
        string='Customer Phone', 
        related='partner_id.phone', 
        readonly=True
    )

    route = fields.Char(string='Route',tracking=True)
    travel_day_start = fields.Datetime(string='Travel Start',tracking=True)
    travel_day_end = fields.Datetime(string='Travel End',tracking=True)

    travel_day_start_display = fields.Char(
        string='Start Day', 
        compute='_compute_travel_day_start',
        store=False
    )
    travel_day_end_display = fields.Char(
        string='End Day', 
        compute='_compute_travel_day_end',
        store=False
    )

    travel_day_duration = fields.Integer(
        string='Travel Duration (days)',
        compute='_compute_travel_day_duration',
        store=True
    )
    @api.depends('order_line')
    def _compute_purchase_orders(self):
        for order in self:
            purchase_orders = self.env['purchase.order'].search([
                ('order_line.product_id', 'in', order.order_line.mapped('product_id').ids)
            ])
            order.purchase_order_ids = purchase_orders

    def action_view_purchase_orders(self):
        action = self.env.ref('purchase.action_purchase_order').read()[0]
        action['domain'] = [('id', 'in', self.purchase_order_ids.ids)]
        return action

    @api.depends('travel_day_start')
    def _compute_travel_day_start(self):
        for record in self:
            lang = self.env.context.get('lang') or 'en_US'
            if record.travel_day_start:
                record.travel_day_start_display = format_date(
                    record.travel_day_start, 
                    format='EEEE',  
                    locale=lang
                )
            else:
                record.travel_day_start_display = ''

    @api.depends('travel_day_end')
    def _compute_travel_day_end(self):
        for record in self:
            lang = self.env.context.get('lang') or 'en_US'
            if record.travel_day_end:
                record.travel_day_end_display = format_date(
                    record.travel_day_end, 
                    format='EEEE',  
                    locale=lang
                )
            else:
                record.travel_day_end_display = ''

    @api.depends('travel_day_start', 'travel_day_end')
    def _compute_travel_day_duration(self):
        for record in self:
            if record.travel_day_start and record.travel_day_end:
                duration = (record.travel_day_end.date() - record.travel_day_start.date()).days
                record.travel_day_duration = max(duration, 0)
            else:
                record.travel_day_duration = 0

    @api.constrains('travel_day_start', 'travel_day_end')
    def _check_travel_day_dates(self):
        for record in self:
            if record.travel_day_start and record.travel_day_end:
                if record.travel_day_end < record.travel_day_start:
                    raise ValidationError("Travel End must be after Travel Start.")