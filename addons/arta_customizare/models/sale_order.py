from odoo import models, api, _
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()

        for order in self:
            origin_company = self.env.company  # compania care emite SO
            origin_partner = origin_company.partner_id  # partenerul companiei curente

            partner_vat = order.partner_id.vat
            if not partner_vat:
                _logger.warning("[INTERCOMPANY] Partenerul %s nu are cod TVA", order.partner_id.name)
                continue

            # 🔍 căutăm compania corespunzătoare (pe baza partenerului SO)
            partner_company = self.env['res.company'].search([
                ('partner_id.vat', '=', partner_vat)
            ], limit=1)

            if not partner_company or partner_company == origin_company:
                _logger.info("[INTERCOMPANY] Fie nu am găsit compania, fie este aceeași cu emitenta.")
                continue

            _logger.info("[INTERCOMPANY] Generăm PO în %s pentru SO %s", partner_company.name, order.name)

            try:
                with self.env.cr.savepoint():
                    env_in_target_company = self.env(context=dict(
                        self.env.context, company_id=partner_company.id
                    ))

                    po_vals = {
                        'partner_id': origin_partner.id,  # ✅ emitentul SO devine furnizor în PO
                        'company_id': partner_company.id,
                        'origin': f"Auto from SO {order.name}",
                        'order_line': [(0, 0, {
                            'product_id': l.product_id.id,
                            'product_qty': l.product_uom_qty,
                            'product_uom': l.product_uom.id,
                            'price_unit': l.price_unit,
                            'date_planned': order.date_order,
                            'name': l.name,
                        }) for l in order.order_line]
                    }

                    po = env_in_target_company['purchase.order'].create(po_vals)

                    order.message_post(
                        body=_(
                            "Comandă de achiziție <b>%s</b> a fost generată automat în compania <b>%s</b> "
                            "de utilizatorul <i>%s</i>."
                        ) % (po.name, partner_company.name, self.env.user.name),
                        message_type='notification',
                        subtype_xmlid='mail.mt_note'
                    )

                    _logger.info("[INTERCOMPANY] PO %s creat în compania %s", po.name, partner_company.name)

            except Exception as e:
                _logger.error("[INTERCOMPANY] Eroare la generarea PO pentru SO %s: %s", order.name, str(e))

        return res