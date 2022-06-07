import pandas as pd
from collections import defaultdict

df = pd.read_csv('dataset_online_retail_II.csv', sep = ";")
prod_list = []
for products in df.Products:
    products_without_brackets = products[1:-1]
    products_splitted = products_without_brackets.split(", ")
    products_parsed = [p[1:-1] for p in products_splitted]
    prod_list.append(products_parsed)
df.Products = prod_list
df = df.iloc[:,:3]
df['Count'] = df.apply(lambda row: len(row.Products), axis=1)
df['Date'] = df.apply(lambda row: row.Date.replace(' ','T'), axis=1)
df = df[['Id', 'Date', 'Count', 'Products']]
#print(df.iloc[:20,:])
df.to_csv('test.csv', index=False)