from collections import defaultdict
from utils import *
import argparse, sys

def mine(df, min_support, max_depth):
    # df with columns Id, Date, Products

    # key is tuple of elements
    # value is dict with sid and timestamp
    elements = defaultdict(list)

    for index, row in df.iterrows():
        for product in row.Products:
            # @todo change to something faster than list
            eid = time.mktime(time.strptime(row.Date, "%Y-%m-%d %H:%M:%S"))
            elements[((product,),)].append({'sid': row.Id, 'timestamp': row.Date, 'seq':((product,),), 'eid':eid})

    freq_single_elements = filter_to_frequent(elements,min_support)
    freq_double_elements = defaultdict(list)

    # get candidates len(c)==2
    doublets = candidate_sequences_size_2_but_faster(freq_single_elements, min_support)

    # get freq sets
    for two_seq in doublets:

        R = join(freq_single_elements[(two_seq[0],)],freq_single_elements[(two_seq[1],)])

        for seq,element in R.items():
            support = len(set([event["sid"] for event in element]))
            if support >= min_support:
                freq_double_elements[seq].extend(element)

    
    freq = generate_freq_recursive(freq_double_elements,min_support, max_depth)

    print("Frequent single sets:")
    for key in freq_single_elements.keys():
        print(key)
    print("Frequent pairs:")
    for key in freq_double_elements.keys():
        print(key)

    print("Frequent rest:")
    for key in freq.keys():
        print(key)
    return


def main(argv):
    parser = argparse.ArgumentParser(description=
            'Spade algorithm'
            )

    parser.add_argument('--dataset',dest='df_filename',help='Filename of Online Retail Dataset II',required=True)
    parser.add_argument('--support',dest='min_support',type=int,help='Minimum support',required=True)
    parser.add_argument('--max-depth',dest='max_depth',type=int,help='Maximum lenght',required=True)
    args = parser.parse_args(argv)
    
    # limit for testing
    df = parse_online_retail(args.df_filename).iloc[:20,:]

    mine(df, args.min_support, args.max_depth)


if __name__ == "__main__":

    main(sys.argv[1:])


