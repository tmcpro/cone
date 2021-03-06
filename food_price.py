import re
import sys
import requests

from config import *
import searcher
import utils

def food_price(city):
    default_price = 15.

    if city is None:
        return default_price

    query = 'average meal cost in {}'.format(city)

    ans = searcher.search(query)

    print('Expected food price at {}: '.format(city))
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
        print('Usage: python3 food_price.py <city>')
        print('City names should be 1 word')
        exit()

    food_price(sys.argv[1])
