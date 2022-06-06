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


class Sequence:
    def __init__(self, products, sid, timestamp):
        self.products = products
        self.sid = sid
        d = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        self.eid = time.mktime(d)

def candidate_sequences_size_2_but_faster(frequent_elements, min_support):
    '''Given an IdList of atoms, return a dictionary of two-sequences as keys with
    the frequency of each two-sequence as the value.
    '''

    # Given an dictionary of Elements, convert it to a horizontal ID list in order to
    # count the frequency of each two-sequence of atoms.
    timeline = {} 

    for name,seq_list in frequent_elements.items():
        for event in seq_list:

            if event["sid"] not in timeline:
                 timeline[event["sid"]] = []

            #horizontal_db[event["sid"]].append((name,event["timestamp"]))
            timeline[event["sid"]].append(Sequence(name, event["sid"], event["timestamp"]))

    # create counts using horizontal_db
    counts = defaultdict(int)
    
    for sid,seq in timeline.items():
        
        for event_index_i,event_i in enumerate(seq):
            for event_index_j,event_j in enumerate(seq[event_index_i+1:]):

                if event_i.eid <= event_j.eid:
                    two_seq = event_i.products + event_j.products
                else:
                    two_seq = event_j.products + event_i.products

                counts[two_seq] += 1

    # this is followed by temporal joins between atoms in pairs, so
    # include only unique combinations
    return {tuple(sorted(two_seq)) for two_seq,count in counts.items() if count >= min_support}

def flat_tumple(d):
    for i in d:
        yield from [i] if not isinstance(i, tuple) else flat_tumple(i)

def join(element_i ,element_j):
    
    join_results = defaultdict(list)
    
    for event_index_i,event_i in enumerate(element_i):
        for event_index_j,event_j in enumerate(element_j):

                sid = event_i["sid"]

                # (xy)
                if event_i["eid"] > event_j["eid"]:
                    merged_seq = event_j["seq"] + (event_i["seq"][-1],)
                    merger_dict = {"sid": sid,"eid": event_i["eid"], 'seq': (merged_seq,)}
                    join_results[merged_seq].append(merger_dict)

                # (yx)
                elif event_i["eid"] < event_j["eid"]:
                    merged_seq = event_i["seq"] + (event_j["seq"][-1],)
                    merger_dict = {"sid": sid,"eid": event_i["eid"], 'seq': (merged_seq,)}
                    join_results[merged_seq].append(merger_dict)

                elif event_i["seq"][-1] != event_j["seq"][-1]:

                    merger_dict = {"sid": sid,"eid": event_j["eid"]}
                    try:
                        # try sorting if all elements are strings
                        flatten = tuple(sorted((list(event_i["seq"][-1]) + list(event_j["seq"][-1]))))
                    except:
                        # fails means nested tuples
                        tmp = tuple(flat_tumple(tuple((list(event_i["seq"][-1]) + list(event_j["seq"][-1])))))
                        flatten = tuple(sorted(list(tmp)))
                    merged_i = event_i["seq"][:-1] + flatten

                    merger_dict["seq"] = (merged_i,)
                    join_results[(merged_i,)].append(merger_dict)


                    merged_j = event_j["seq"][:-1] + flatten

                    # if both resulting atoms are identical, only add it once
                    if merged_j != merged_i:
                        merger_dict["seq"] = (merged_j,)
                        join_results[(merged_j,)].append(merger_dict)
                
    return join_results


def generate_freq_recursive(elements,min_support, max_depth = 5):

    frequent_elements = defaultdict(list)

    for element_index_i,seq_i in enumerate(elements.keys()):

        frequent_elements_inner = defaultdict(list)
            
        for element_index_j,seq_j in enumerate(list(elements.keys())[element_index_i+1:]):
            if len(tuple(flat_tumple(seq_i + seq_j))) > max_depth +1:
                continue
            R = join(elements[seq_i],elements[seq_j])

            for seq,element in R.items():
                support = len(set([event["sid"] for event in element]))
                if support >= min_support:
                    frequent_elements_inner[seq].extend(element)


        for seq,element in frequent_elements_inner.items():
            frequent_elements[seq].extend(element)

        for seq,element in generate_freq_recursive(frequent_elements_inner,min_support, max_depth).items():
            frequent_elements[seq].extend(element)

    return frequent_elements