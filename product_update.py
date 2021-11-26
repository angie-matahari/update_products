import requests
import json
import csv

import time

url = 'https://sairaj-dev2-3663518.dev.odoo.com/product_update/'
headers = {'Content-Type': 'application/json'}
file_path = '/home/kanini/update_products'

with open('product.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    start_for_loop = time.time()
    for i, row in enumerate(csv_reader):
        if not i:
            continue
        start_loop = time.time()
        data = {"params": {'product': row[1]}}
        data_json = json.dumps(data)
        print(f'call update url with data {data_json}')
        response = requests.post(url=url, data=data_json, headers=headers)
        print(response.text)
        end_loop = time.time()
        print(f'Single product update time {end_loop - start_loop} s')
    end_for_loop = time.time()
    print(f'Finished uploading data in {end_for_loop - start_for_loop} s')

# dic = '{"jsonrpc": "2.0", "id": null, "result": {"params": {"product": "Ironman Key Chain, Part # KEY001"}}}'
