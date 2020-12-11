import requests
import json
import logging
from urllib.request import urlopen
import os
from dotenv import load_dotenv
load_dotenv()
from os import environ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
dowSymbols = ["AAL","GOOG"]

for i in range (0, len(dowSymbols)): #len(dowSymbols
  try:
    my_value_a = os.getenv('MY_VAR_A')
    url = 'https://financialmodelingprep.com/api/v3/company/profile/'+dowSymbols[i]+'?apikey='+my_value_a
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
    print (url)
    request = urlopen(url)
    response = request.read()
    data = json.loads(response)
    print (data)
    if data['symbol']:
     price = data['profile']['price']
     print ("The price is {}".format(price))
    else:
     print ("An error occurred: %s") % (data['error']['description'])
    request.close()
  except IndexError:
    print ("Data not available (Index)"+"\n")
    print ("*****************************************************************************"+"\n")
  except AttributeError as err:
    print ("Data not available (Attribute)"+"\n")
    print ("*****************************************************************************"+"\n")
    logger.warning("The data was not available: {}".format(err)+"\n")
    continue
print("**************"+"\n")
