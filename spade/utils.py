import pandas as pd
from collections import defaultdict
import time

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
        if support > min_support:
            subsetted[name] += element
                    
    return subsetted

# returns:
# 1 if x after y
# -1 if before
# 0 if at the same time
def after(timestamp_x, timestamp_y):
    if timestamp_x == timestamp_y:
        return 0
    #2010-10-04 09:54:00
    timestamp_x = time.strptime(timestamp_x, "%Y-%m-%d %H:%M:%S")
    timestamp_y = time.strptime(timestamp_y, "%Y-%m-%d %H:%M:%S")

    if timestamp_x > timestamp_y:
        return 1
    else:
        return -1

# returns dictionary candidate -> tidlist
def candidate_sequences_size_2(frequent_elements, min_support):
    for i in range(0, len(frequent_elements.keys())):
        candidates = {}
        # elements x and y are the same but in separate transactions x b4 y
        x = list(frequent_elements.keys())[i]
        candidate = (x[0],x[0])
        tidlist = []
        for transaction_x_id in range(0, len(frequent_elements[x])):
            for transaction_y_id in range(transaction_x_id+1, len(frequent_elements[x])):
                if frequent_elements[x][transaction_x_id]['sid'] == \
                frequent_elements[x][transaction_y_id]['sid'] and \
                after(frequent_elements[x][transaction_y_id]['timestamp'], frequent_elements[x][transaction_x_id]['timestamp']):
                    tidlist.append(frequent_elements[x][transaction_y_id])
        if(len(tidlist) > min_support):
            candidates[candidate] = tidlist

        for j in range(i+1, len(frequent_elements.keys())):
            # elements x and y are not the same and in single transaction
            x = list(frequent_elements.keys())[i]
            y = list(frequent_elements.keys())[j]
            candidate = (x[0]+';'+y[0],) # TODO: make sure if that is a good idea
            tidlist = []
            for transaction_x in frequent_elements[x]:
                if transaction_x in frequent_elements[y]:
                    tidlist.append(transaction_x)
            if(len(tidlist) > min_support):
                candidates[candidate] = tidlist
            
            #  elements x and y are not the same and in separate transactins x b4 y
            candidate = (x[0],y[0])
            tidlist = []
            for transaction_x_id in range(0, len(frequent_elements[x])):
                for transaction_y_id in range(0, len(frequent_elements[y])):
                    if frequent_elements[x][transaction_x_id]['sid'] == \
                    frequent_elements[y][transaction_y_id]['sid'] and \
                    after(frequent_elements[y][transaction_y_id]['timestamp'], frequent_elements[x][transaction_x_id]['timestamp']):
                        tidlist.append(frequent_elements[y][transaction_y_id])
            if(len(tidlist) > min_support):
                candidates[candidate] = tidlist

            #  elements x and y are not the same and in separate transactins y b4 x
            candidate = (y[0],x[0])
            tidlist = []
            for transaction_x_id in range(0, len(frequent_elements[x])):
                for transaction_y_id in range(0, len(frequent_elements[y])):
                    if frequent_elements[x][transaction_x_id]['sid'] == \
                    frequent_elements[y][transaction_y_id]['sid'] and \
                    after(frequent_elements[x][transaction_x_id]['timestamp'], frequent_elements[y][transaction_y_id]['timestamp']):
                        tidlist.append(frequent_elements[x][transaction_x_id])
            if(len(tidlist) > min_support):
                candidates[candidate] = tidlist
        return candidates