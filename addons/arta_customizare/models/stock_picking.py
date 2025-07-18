from odoo import models, api

# ATENȚIE: logica de mai jos e păstrată doar ca model de lucru.
# Momentan fluxul standard Odoo este suficient și mai robust.

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        picking = super().create(vals)

        if picking.picking_type_id.code == 'incoming' and picking.origin:
            source_picking = self.env['stock.picking'].search([
                ('origin', '=', picking.origin.replace('Auto from SO ', ''))
            ], limit=1)

            if source_picking and source_picking.picking_type_id.code == 'outgoing':
                for dest_move in picking.move_ids_without_package:
                    src_move = source_picking.move_ids_without_package.filtered(
                        lambda m: m.product_id == dest_move.product_id and m.quantity_done == dest_move.product_uom_qty
                    )
                    if src_move:
                        src_lot_lines = src_move.move_line_ids.filtered(lambda l: l.lot_id)
                        for line in src_lot_lines:
                            self.env['stock.move.line'].create({
                                'picking_id': picking.id,
                                'move_id': dest_move.id,
                                'product_id': dest_move.product_id.id,
                                'product_uom_id': dest_move.product_uom.id,
                                'qty_done': line.qty_done,
                                'lot_id': line.lot_id.id,
                                'location_id': picking.location_id.id,
                                'location_dest_id': picking.location_dest_id.id,
                            })

        return picking