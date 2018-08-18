import re
import sys
import requests

from config import *

def search(query):
    headers = { "Ocp-Apim-Subscription-Key" : BING_SEARCH_AZURE_KEY }
    params  = { "q": query, "textDecorations":True, "textFormat": "HTML" }
    response = requests.get(BING_SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()

    search_results = response.json()

    rows = "\n".join(["""<tr>
                           <td><a href=\"{0}\">{1}</a></td>
                           <td>{2}</td>
                         </tr>""".format(v["url"],v["name"],v["snippet"]) \
                      for v in search_results["webPages"]["value"]])

    return rows

if __name__ == '__main__':
    print('Dont run this file directly')
    exit()