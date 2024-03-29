import requests
import json
import logging
from urllib.request import urlopen
import os
import sys
from dotenv import load_dotenv

load_dotenv()
from os import environ

te = open("newCompList.txt", "a")  # File where you need to keep the logs


class Unbuffered:
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
        te.write(data)  # Write the data of stdout here to a text file as well

    def flush(self):
        pass


sys.stdout = Unbuffered(sys.stdout)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
symbols = []

try:
    my_value_a = os.getenv("MY_VAR_A")
    url = "https://financialmodelingprep.com/api/v3/stock/list?apikey=" + my_value_a
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }  #
    print(url)
    request = urlopen(url)
    response = request.read()
    data = json.loads(response)  # print(data)
    # li = [item.get('symbol') for item in data]
    symbols.extend([item.get("symbol") for item in data])
    request.close()
except IndexError:
    print("Data not available (Index)" + "\n")
    print(
        "*****************************************************************************"
        + "\n"
    )
except AttributeError as err:
    print("Data not available (Attribute)" + "\n")
    print(
        "*****************************************************************************"
        + "\n"
    )
    logger.warning("The data was not available: {}".format(err) + "\n")
    pass

print("*****My Symbols array*********" + "\n")
print(symbols)
print(len(symbols))
