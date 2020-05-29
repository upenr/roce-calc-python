import requests
import json
import logging
from urllib.request import urlopen
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)
symbols = []

try: #Basic API URL
  url = 'https://financialmodelingprep.com/api/v3/stock/list?apikey=YOUR_API_KEY'
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
  }#
  print(url)
  request = urlopen(url)
  response = request.read()
  data = json.loads(response)# print(data)
  # li = [item.get('symbol') for item in data]
  symbols.extend([item.get('symbol') for item in data])
  request.close()
except IndexError:
  print ("Data not available (Index)"+"\n")
  print ("*****************************************************************************"+"\n")
except AttributeError as err:
  print ("Data not available (Attribute)"+"\n")
  print ("*****************************************************************************"+"\n")
  logger.warning("The data was not available: {}".format(err)+"\n")
  pass

print("*****My Symbols array*********" + "\n")
print(symbols)
print (len(symbols))
