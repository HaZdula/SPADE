from collections import defaultdict
from utils import *
import argparse, sys

def mine(df, min_support):
    # df with columns Id, Date, Products
    # @todo uogolnic zeby dzialalo moze na czyms innym niz ta konkretna csvka

    # key is tuple of elements
    # value is dict with sid and timestamp
    # @todo change timestamp to event id,

    elements = defaultdict(list)

    for index, row in df.iterrows():
        for product in row.Products:
            # @todo change to something faster than list
            elements[(product,)].append({'sid': row.Id, 'timestamp': row.Date})

    freq_single_elements = filter_to_frequent(elements,min_support)

    return


def main(argv):
    parser = argparse.ArgumentParser(description=
            'Spade algorithm'
            )

    parser.add_argument('--dataset',dest='df_filename',help='Filename of Online Retail Dataset II',required=True)
    parser.add_argument('--support',dest='min_support',type=int,help='Minimum support',required=True)
    args = parser.parse_args(argv)
    #MIN_SUPPORT = 2
    df = parse_online_retail(args.df_filename)

    mine(df, args.min_support)


if __name__ == "__main__":

    main(sys.argv[1:])


