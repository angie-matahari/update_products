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
            product = request.env['product.product'].sudo().browse(
                int(product_id))
            quants = request.env['stock.quant'].sudo().read_group(
                [
                    ('product_id', '=', product.id),
                    ('location_id.usage', '=', 'internal'),
                    ('quantity', '>', 0)
                ],
                ['location_id', 'quantity'],
                ['location_id']
            )

            if quants:
                initial_category_state = product.categ_id.property_valuation
                res = product.categ_id.write(
                    {'property_valuation': 'manual_periodic'})
                if res:  # we need this operation to happen if above write returns True
                    for quant in quants:
                        location_id = quant.get('location_id')[0]
                        initial_quantity = quant.get('quantity')

                        inventory = request.env['stock.inventory'].sudo().create({
                            'name': product.name + ' -WRONG COST- ' + str(datetime.now()),
                            'product_id': product.id,
                            'filter': 'product',
                            'location_id': location_id
                        })
                        inventory.action_start()
                        inventory.action_reset_product_qty()
                        inventory.action_validate()

                        # starting the reset
                        new_res = product.categ_id.write(
                            {'property_valuation': initial_category_state})

                        if new_res:
                            inventory_reset = request.env['stock.inventory'].sudo().create({
                                'name': product.name + ' -WRONG COST- ' + datetime.today().strftime('%m/%d/%y'),
                                'product_id': product.id,
                                'filter': 'product',
                                'location_id': location_id
                            })
                            inventory_reset.action_start()

                            line = inventory_reset.line_ids.filtered(
                                lambda x: x.product_id.id == product.id)
                            line_res = line.write(
                                {'product_qty': initial_quantity})

                            if line_res:
                                result = inventory_reset.action_validate()
                                return {'result': result, 'message': 'Product updated successfully'}

        return {'result': 'Error', 'message': 'Product update failed!'}
