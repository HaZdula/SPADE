import pandas as pd
def parse_online_retail(filepath):
    #
    # Parse online retail dataset
    # Handle nasty double quotes in products list
    # 
    df = pd.read_csv(filepath, sep = ";")
    prod_list = []
    for products in df.Products:
        products_without_brackets = products[1:-1]
        products_splitted = products_without_brackets.split(", ")
        products_parsed = [p[1:-1] for p in products_splitted]
        prod_list.append(products_parsed)
    df.Products = prod_list
    return df.iloc[:,:3]