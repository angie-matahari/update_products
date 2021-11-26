# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime

import json
import logging
_logger = logging.getLogger(__name__)

class SairajProductUpdate(http.Controller):
    @http.route('/product_update/', auth='none', type='json', method=['GET', 'POST'], cors='*', csrf=False)
    def update_product_valuation(self, **post):
        data = json.loads(request.httprequest.get_data())
        product_id = data['params']['product']
        if product_id:
            _logger.info(f'product_id {product_id}')
#             product = request.env['product.product'].sudo().search([('name', '=', data['params']['product'])])
            product = request.env['product.product'].sudo().browse(product_id)
            quants = request.env['stock.quant'].sudo().read_group(
                [('product_id', '=', int(product_id)), ('location_id.usage', '=', 'internal'), ('quantity', '>', 0)],
                ['location_id', 'quantity'],
                ['location_id']
            )
            _logger.info(quants)
            if quants:
                _logger.info(f'categ_id valuation {product.categ_id.property_valuation}')
                product.categ_id.write({'property_valuation': 'manual_periodic'})
                _logger.info(f'categ_id valuation {product.categ_id.property_valuation}')
                inventory = request.env['stock.inventory'].sudo().create({
                    'name': product.name + ' - ' + datetime.today().strftime('%m/%d/%y'),
                    'product_id': int(product_id),
                    'filter': 'product',
                    'location_id': 1
                })
                _logger.info(f'inventory {inventory}')
                inventory.action_start()
                _logger.info(f'inventory {inventory.state}')
                inventory.action_reset_product_qty()
                _logger.info(f'line_ids qty {inventory.line_ids.mapped("product_qty")}')
                inventory.action_validate()
                _logger.info(f'inventory {inventory.state}')
                product.categ_id.write({'property_valuation': 'real_time'})
                _logger.info(f'categ_id valuation {product.categ_id.property_valuation}')
                inventory_reset = request.env['stock.inventory'].sudo().create({
                    'name': product.name + ' - ' + datetime.today().strftime('%m/%d/%y'),
                    'product_id': int(product_id),
                    'filter': 'product',
                    'location_id': 1
                })
                _logger.info(f'inventory_reset {inventory_reset}')
                inventory_reset.action_start()
                _logger.info(f'inventory_reset {inventory_reset.state}')
                inventory_reset.line_ids.unlink()
                _logger.info(f'line_ids qty {inventory_reset.line_ids.mapped("product_qty")}')
                lines = []
                for quant in quants:
                    vals = {
                        'product_id': int(product_id),
                        'location_id': quant['location_id'][0],
                        'product_uom_id': product.uom_id,
                        'theoretical_qty': quant['quantity'],
                        'product_qty': quant['quantity']
                    }
                    lines.append((0, 0, vals))
                _logger.info(f'lines {lines}')
                inventory_reset.sudo().write({
                    'line_ids': lines
                })
                _logger.info(f'line_ids qty {inventory_reset.line_ids.mapped("product_qty")}')
                inventory_reset.action_validate()
                _logger.info(f'inventory_reset {inventory_reset.state}')

        return product