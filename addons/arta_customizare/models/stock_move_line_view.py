from odoo import models


class XStockMoveLineView(models.Model):
    _name = 'x.stock.move.line.view'
    _inherit = 'stock.move.line'
    _description = 'Linii de stoc standalone pentru vizualizare'

    consume_line_ids = None