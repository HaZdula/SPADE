import pandas as pd
from collections import defaultdict
import datetime
import time
import numpy as np

def parse_products(list):
    new_list = ''
    for str in list.Products:
        new_list += str.replace(" ",'_')+' '
    return new_list

df = pd.read_csv('datasets/dataset_online_retail_II.csv', sep = ";")
prod_list = []
for products in df.Products:
    products_without_brackets = products[1:-1]
    products_splitted = products_without_brackets.split(", ")
    products_parsed = [p[1:-1] for p in products_splitted]
    prod_list.append(products_parsed)
df.Products = prod_list
df = df.iloc[:,:3]
df['Count'] = df.apply(lambda row: len(row.Products), axis=1)
df['Products'] = df.apply(parse_products, axis=1)
df['Date'] = df.apply(lambda row: time.mktime(datetime.datetime.strptime(row.Date, "%Y-%m-%d %H:%M:%S").timetuple()), axis=1)
df = df[['Id', 'Date', 'Count', 'Products']]
df_small = df.iloc[:3000,:]
df_xsmall = df.iloc[:50,:]
#np.savetxt('datasets/retail_zaki_extra.txt', df_xsmall, delimiter=' ')
df.to_csv('datasets/retail_zaki.txt', index=False, header=None)
df_small.to_csv('datasets/retail_zaki_small.txt', index=False, header=None)
df_xsmall.to_csv('datasets/retail_zaki_extra.txt', index=False, header=None)