import csv
from .foodly-backend.products.models import Product

bulk_list = []

with open('./realfinal.csv') as csv_file:
    data = csv.reader(csv_file)
    for row in data:
        bulk_list.append(Product(year = row[16]))

print(bulk_list)