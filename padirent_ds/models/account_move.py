from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    package_name = fields.Text(string="Package Name")



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    merge_product = fields.Boolean(string="Merge Product", default=False)