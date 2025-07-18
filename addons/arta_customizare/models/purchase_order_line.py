from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    x_lot_id = fields.Many2one('stock.lot', string="Lot asociat", readonly=True)