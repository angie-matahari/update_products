# 'https://sairaj-dev2-3663518.dev.odoo.com/product_update/'

import requests
import json
import csv

import time

url = 'https://sairaj-dev2-3663518.dev.odoo.com/product_update/'
headers = {'Content-Type': 'application/json'}
file_path = '/home/kanini/update_products'

with open('product.product (3).csv', encoding='utf-8') as csv_file:
    print(csv_file)
    csv_reader = csv.reader(csv_file, delimiter=',')
    print(csv_reader)
    start_for_loop = time.time()
    for i, row in enumerate(csv_reader):
        start_loop = time.time()
        if i == 158:
            print(row[1])
            data = {"params" : { 'product': row[1]} }
            data_json = json.dumps(data)
            print('call url')
            r = requests.post(url=url, data=data_json, headers=headers)
            print(r.text)
            print(type(r.text))
            end_loop = time.time()
            print(f'loop time {end_loop - start_loop}')
            if i > 0:
                break
    end_for_loop = time.time()
    print(f'End loop {end_for_loop - start_for_loop}') 

# dic = '{"jsonrpc": "2.0", "id": null, "result": {"params": {"product": "Ironman Key Chain, Part # KEY001"}}}'
