from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    package_name = fields.Text(string="Package Name")

    travel_day_start = fields.Datetime(string='Travel Start', readonly=True)
    travel_day_end = fields.Datetime(string='Travel End', readonly=True)

    travel_day_start_display = fields.Char(readonly=True)
    travel_day_end_display = fields.Char(readonly=True)

    travel_day_duration = fields.Integer(readonly=True)

    route = fields.Char(string='Route', readonly=True)
    
    driver_id = fields.Many2one(
        'res.partner', 
        string='Driver',
        domain="[('is_driver', '=', True)]",
        readonly=True
    )
    driver_phone = fields.Char(
        string='Driver Phone',
        related='driver_id.phone',
        readonly=True
    )

    def get_custom_invoice_lines(self):
        for move in self:
            merged_lines = move.invoice_line_ids.filtered(lambda l: l.merge_product)
            normal_lines = move.invoice_line_ids.filtered(lambda l: not l.merge_product)

            result = []
            if merged_lines:
                merged_total = sum(merged_lines.mapped('price_subtotal'))
                result.append({
                    'name': move.package_name or 'Merged Product',
                    'quantity': 1,
                    'price_unit': merged_total,
                    'price_subtotal': merged_total,
                    'display_type': 'product',
                    'is_merged': True,
                })

            for line in normal_lines:
                result.append({
                    'name': line.name,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'display_type': line.display_type,
                    'discount': line.discount,
                    'taxes': ', '.join([(tax.invoice_label or tax.name) for tax in line.tax_ids]),
                    'product_uom_id': line.product_uom_id,
                    'merged': False
                })

            return result



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    merge_product = fields.Boolean(string="Merge Product", default=False)