from odoo import models, fields, api

class ProductionReport(models.AbstractModel):
    _name = 'report.auto_lot_reception.production_report'
    _description = 'Raport de Productie Zilnic'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['mrp.production'].search([
            ('date_planned_start', '>=', fields.Date.today()),
            ('state', '=', 'done')
        ])

        return {
            'docs': docs,
            'date_today': fields.Date.today(),
        }