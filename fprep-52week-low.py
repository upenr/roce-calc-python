#Author: Upendra Rajan
#This makes 1 API call per company listed in mySymbols

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
mySymbols = ['HD','FB','GOOG','REGN','FOX','RHI','CMI','AMAT','FFIV','LOW','MAS','PKG','JBHT','EA','NVR','TER','CBRE','TSN','GOOGL','FOXA','EXPD','FBHS','HCA','HPQ','TXN','ACN','CSCO','AZO','CERN','PH','DGX','ALGN','CRL','ORLY','GRMN','EMR','PHM','DOV','BRO','SWKS','LEN','SNA','PM','AOS','CTSH','ZBRA']
threshold = 30  # Enter percentage you want stock price to be above 52 week low
final_companies = []
discount_dict = {}

def get_env_var(i):
    try:
        letter = ['O', 'G', 'B', 'I', 'A', 'M', 'K', 'L',
                  'J', 'F', 'H', 'C', 'D', 'E'][i // 250]
        return os.getenv("MY_VAR_" + letter)
    except IndexError:
        return "demo"

for i in range(0, len(mySymbols)):  # len(mySymbols)
    try:
        my_value_c = get_env_var(i)
        url = (
            "https://financialmodelingprep.com/api/v3/quote/"
            + mySymbols[i]
            + "?apikey="
            + my_value_c
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        # print (url)
        request = urlopen(url)
        response = request.read()
        data = json.loads(response)
        # print (data)
        if data[0]:
            symbol = data[0]["symbol"]
            price = data[0]["price"]
            yearLow = data[0]["yearLow"]
            yearHigh = data[0]["yearHigh"]
            print("This is for stock " + symbol + " today.")
            print("The price is {0:.2f}".format(price))
            print("The 52 week low is {0:.2f}".format(float(yearLow)))
            discount1 = ((price - yearLow) / yearLow) * 100
            discount2 = ((yearHigh - price) / yearHigh) * 100
            print(
                "The current price is {0:.2f} percent higher compared to 52 week low.".format(
                    discount1
                )
            )
            print(
                "The current price is {0:.2f} percent lower compared to 52 week high.".format(
                    discount2
                )
            )
            if discount1 <= discount2:  # and discount1 < (threshold*100)
                discount_dict[mySymbols[i]] = []
                # final_companies.append(symbol)
                discount_dict.setdefault(symbol, []).append(round(discount1, 2))
            print("******************************")
        else:
            print("An error occurred: %s") % (data["error"]["description"])
        request.close()
    except NameError:
        print("Name Error" + "\n")
        print(
            "*****************************************************************************"
            + "\n"
        )
    except TypeError:
        print("Type Error" + "\n")
        print(
            "*****************************************************************************"
            + "\n"
        )
    except KeyError:
        print("API Key probably exceeded max requests" + "\n")
        print(
            "*****************************************************************************"
            + "\n"
        )
        continue
    except ValueError:
        print("More data not available (Value)" + "\n")
        print(
            "*****************************************************************************"
            + "\n"
        )
    except ZeroDivisionError:
        print("Some data not available (Zero division error)" + "\n")
        print(
            "*****************************************************************************"
            + "\n"
        )
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
    continue
print(
    "These are the companies that are closer to their 52 week low than high (Number is percentage from low. Blank means none.): "
)
# print(final_companies)
sorted_d = dict(sorted(discount_dict.items(), key=lambda x: x[1], reverse=False))
print(sorted_d)
print("\n")
