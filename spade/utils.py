import pandas as pd
from collections import defaultdict

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

def filter_to_frequent(elements,min_support):
    # return only elements that have higher support than min_support

    subsetted = defaultdict(list)

    for name,element in elements.items():
        support = len(set([event["sid"] for event in element]))
        if support >= min_support:
            subsetted[name].append(element)
                    
    return subsetted