import requests
import json
import csv

import time

url = 'https://sairaj-dev2-3681655.dev.odoo.com/product_update/'
headers = {'Content-Type': 'application/json'}

data = {"params" : { 'product': 25163} }
data_json = json.dumps(data)
print('call url')
r = requests.post(url=url, data=data_json, headers=headers)
print(r.text)