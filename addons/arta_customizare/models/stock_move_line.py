# arta_customizare/models/stock_move_line.py
from odoo import models, fields, api
import datetime

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'lot_name' not in vals and vals.get('product_id'):
                product = self.env['product.product'].browse(vals['product_id'])
                if product.tracking == 'lot':
                    today = datetime.date.today().strftime('%Y%m%d')
                    company_code = self.env.company.code if hasattr(self.env.company, 'code') else f"C{self.env.company.id}"
                    lot_name = f"LOT-{today}-{company_code}-{product.id}"

                    existing = self.env['stock.lot'].search([
                        ('name', '=', lot_name),
                        ('product_id', '=', product.id),
                        ('company_id', '=', self.env.company.id)
                    ], limit=1)

                    if existing:
                        vals['lot_id'] = existing.id
                    else:
                        vals['lot_name'] = lot_name

        return super().create(vals_list)