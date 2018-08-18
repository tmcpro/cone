import re
import sys
import requests

from config import *

def flight_price(from_city, to_city):
    search_term = 'price from {} to {}'.format(from_city, to_city)

    headers = { "Ocp-Apim-Subscription-Key" : BING_SEARCH_AZURE_KEY }
    params  = { "q": search_term, "textDecorations":True, "textFormat": "HTML" }
    response = requests.get(BING_SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()

    search_results = response.json()

    rows = "\n".join(["""<tr>
                           <td><a href=\"{0}\">{1}</a></td>
                           <td>{2}</td>
                         </tr>""".format(v["url"],v["name"],v["snippet"]) \
                      for v in search_results["webPages"]["value"]])

    # print(rows)
    print('Price: ')
    match = re.search('\$[0-9,]+', rows)
    print(match.group(0))




if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage: python3 flight_price.py <fromCity> <toCity>')
        print('City names should be 1 word')
        exit()

    flight_price(sys.argv[1], sys.argv[2])
