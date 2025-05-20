from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    nik_cust = fields.Char(string="NIK",size=16)
    is_driver = fields.Boolean(string="Driver")
