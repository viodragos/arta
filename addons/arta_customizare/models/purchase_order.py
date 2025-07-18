from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_intercompany_so_id = fields.Many2one('sale.order', string="Comandă SO Intercompany", readonly=True)