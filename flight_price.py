import re
import sys
import requests

from config import *
import searcher
import utils

def flight_price(from_city, to_city):
    query = 'price from {} to {}'.format(from_city, to_city)
    ans = searcher.search(query)

    match = re.search('\$\d+(?:\.\d+)?', ans)

    if not match:
        print('City pairs not supported yet, try another pair')
        return -1
    else:
        print('Price from {} to {}: '.format(from_city, to_city))
        price = float(''.join(list(filter(utils.isdigit_or_dot, match.group(0)))))
        print('${}'.format(price))
        return price

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage: python3 flight_price.py <fromCity> <toCity>')
        print('City names should be 1 word')
        exit()

    flight_price(sys.argv[1], sys.argv[2])
