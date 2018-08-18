import re
import sys
import requests

from config import *
import searcher

def food_price(city):
    query = 'average meal cost in {}'.format(city)

    ans = searcher.search(query)

    print('Avg Food Price at {}: '.format(city))
    match = re.findall('\$[0-9,]+', ans)

    prices = [int(re.search('\d+', m).group(0)) for m in match]
    avg_price = sum(prices) / len(prices)

    print('${}'.format(avg_price))
    return avg_price

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python3 flight_price.py <city>')
        print('City names should be 1 word')
        exit()

    food_price(sys.argv[1])
