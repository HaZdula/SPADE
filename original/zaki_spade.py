from pycspade.helpers import spade, print_result

# To get raw SPADE output
result = spade(filename='datasets/retail_zaki_formatted_extra.txt', support=0.3, parse=False)
print(result['mined'])