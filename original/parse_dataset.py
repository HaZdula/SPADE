import pandas as pd
from collections import defaultdict
import datetime
import time
import numpy as np
import json

def parse_products(list):
    new_list = ''
    for prod in list.Products:
        new_list += str(prod)+' '
    return new_list

df = pd.read_csv('datasets/dataset_online_retail_II.csv', sep = ";")
prod_list = []
for products in df.Products:
    products_without_brackets = products[1:-1]
    products_splitted = products_without_brackets.split(", ")
    products_parsed = [p[1:-1] for p in products_splitted]
    prod_list.append(products_parsed)
df.Products = prod_list

product_counter = 0
products_dict = {}

prod_list = []
for products in df.Products:
    product_as_numbers = []
    for p in products:
        if p in products_dict.keys():
            product_as_numbers.append(products_dict[p])
        else:
            products_dict[p] = product_counter
            product_as_numbers.append(product_counter)
            product_counter+=1 
    prod_list.append(product_as_numbers)
df.Products = prod_list

df = df.iloc[:,:3]
df['Count'] = df.apply(lambda row: len(row.Products), axis=1)
df['Products'] = df.apply(parse_products, axis=1)
df['Date'] = df.apply(lambda row: time.mktime(datetime.datetime.strptime(row.Date, "%Y-%m-%d %H:%M:%S").timetuple()), axis=1)
df = df[['Id', 'Date', 'Count', 'Products']]

last_sequence_id = 0
last_sequence_counter = 0
last_event_counter = 1
for i in range(0, len(df)):
    #print(df.iloc[i]['Id'])
    if df.iloc[i]['Id'] != last_sequence_id:
        last_sequence_id = df.iloc[i]['Id']
        last_sequence_counter+=1
        df.loc[[i],['Id']] = last_sequence_counter
        last_event_counter = 1
        df.loc[[i],['Date']] = last_event_counter
        last_event_counter += 1
    else:
        df.loc[[i],['Id']] = last_sequence_counter  
        df.loc[[i],['Date']] = last_event_counter
        last_event_counter += 1

df['Date'] = pd.to_numeric(df['Date'], downcast='integer')
file = open("datasets/products_map.json", "w")
json.dump(products_dict, file)
file.close()

exit (0)
df_small = df.iloc[:200,:]
df_xsmall = df.iloc[:50,:]
#np.savetxt('datasets/retail_zaki_extra.txt', df_xsmall, delimiter=' ')
df.to_csv('datasets/retail_zaki.txt', index=False, header=None)
df_small.to_csv('datasets/retail_zaki_small.txt', index=False, header=None)
df_xsmall.to_csv('datasets/retail_zaki_extra.txt', index=False, header=None)