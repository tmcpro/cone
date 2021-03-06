import re
import sys
import requests

from config import *
import searcher
import utils

def hotel_price(city):
    default_price = 150.

    if city is None:
        return default_price

    query = 'hotel cost in {}'.format(city)

    ans = searcher.search(query)

    print('Expected hotel cost at {} for 1 night: '.format(city))
    match = re.findall('\$\d+(?:\.\d+)?', ans)
    prices = [float(''.join(list(filter(utils.isdigit_or_dot, m)))) for m in match]

    if not prices:
        avg_price = default_price
    else:
        avg_price = sum(prices) / len(prices)

    print('${:.2f}'.format(avg_price))
    return avg_price


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python3 hotel_price.py <city>')
        print('City names should be 1 word')
        exit()

    hotel_price(sys.argv[1])
