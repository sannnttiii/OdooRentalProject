from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    package_name = fields.Text(string="Package Name")

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