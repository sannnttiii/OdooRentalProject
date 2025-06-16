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
        domain="[('state','=','purchase')]",
    )
    customer_phone = fields.Char(
        string='Customer Phone', 
        related='partner_id.phone', 
        readonly=True
    )

    route = fields.Char(string='Route',tracking=True)
    travel_day_start = fields.Datetime(string='Travel Start',tracking=True, required=True)
    travel_day_end = fields.Datetime(string='Travel End',tracking=True, required=True)

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
    
    driver_id = fields.Many2one(
        'res.partner', 
        string='Driver',
        domain="[('is_driver', '=', True)]"
    )
    driver_phone = fields.Char(
        string='Driver Phone',
        related='driver_id.phone',
        readonly=True
    )

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
    
    @api.constrains('order_line', 'driver_id')
    def _check_driver_info(self):
        for order in self:
            has_driver_product = False
            for line in order.order_line:
                product_name = line.product_id.name.lower()
                # _logger.info("Driver Product: %s", product_name)
                if product_name == 'driver':
                    has_driver_product = True
                    break

            # _logger.info("Driver Product: %s", has_driver_product)

            if order.driver_id and not has_driver_product:
                raise ValidationError("You have selected a driver, but haven't added the 'Driver' product to the order line.")

            if has_driver_product and not order.driver_id:
                raise ValidationError("You have added the 'Driver' product to the order line, but haven't selected a driver.")
    
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.purchase_order_id and order.purchase_order_id.state == 'purchase':
                order.purchase_order_id.button_done()  # Ini mengubah status menjadi 'done' (Locked)
            # Cek apakah PO terkait sudah `done`, lanjutkan proses konfirmasi SO jika PO belum `done`
            elif order.purchase_order_id and order.purchase_order_id.state == 'done':
                raise UserError(
                    f"Purchase Order {order.purchase_order_id.name} sudah selesai dan tidak bisa dikaitkan dengan Sales Order ini."
                )
        return res

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        for order in self:
            po = order.purchase_order_id
            if po:
                if po.state == 'done':
                    po.button_unlock() 
        return res

    @api.model
    def create(self, vals):
        order = super().create(vals)
        order._check_driver_info()
        return order

    def write(self, vals):
        res = super().write(vals)
        self._check_driver_info()
        return res
