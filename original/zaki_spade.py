from pycspade.helpers import spade, print_result

# To get raw SPADE output
result = spade(filename='datasets/retail_zaki_small.txt', support=0.2, parse=True, maxlen=2)
print_result(result)