from os import environ
import requests
import json
import re
import logging
from urllib.request import urlopen
from collections import defaultdict
import numpy as np
from colorama import init, Fore, Back, Style
import sys
import os
from dotenv import load_dotenv

load_dotenv()

te = open("cac40.txt", "a")  # File where you need to keep the logs


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

init(convert=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
snpSymbols = ['DGX', 'GOOG']
cacSymbols = ['MC.PA', 'SAN.PA', 'FP.PA', 'OR.PA', 'AI.PA', 'SU.PA', 'KER.PA', 'AIR.PA', 'BN.PA', 'EL.PA', 'DG.PA', 'BNP.PA', 'CS.PA', 'RI.PA', 'RMS.PA', 'VIV.PA', 'DSY.PA', 'ENGI.PA', 'LR.PA',
              'CAP.PA', 'SGO.PA', 'STM.PA', 'ORA.PA', 'ML.PA', 'TEP.PA', 'WLN.PA', 'VIE.PA', 'GLE.PA', 'ACA.PA', 'UG.PA', 'CA.PA', 'ALO.PA', 'MT.PA', 'HO.PA', 'ATO.PA', 'EN.PA', 'PUB.PA', 'RNO.PA', 'URW.PA']
# dowSymbols = ['ALIM', 'AB', 'ATHM', 'BSVN', 'BSTC', 'CAMT', 'CHKP', 'CORT', 'ENTA', 'ENDP', 'EPM', 'FFIV', 'GRMN', 'GNTX', 'LANC', 'LOGI', 'MX', 'MPX', 'MGI', 'PETS', 'QNST', 'RMR', 'SWKS', 'SMMT', 'THC', 'TGI', 'YRCW', 'ZEAL']
# snpSymbols = ['BSBR', 'BMO', 'CM', 'CNQ', 'COP', 'DAL', 'DFS', 'EC', 'ET', 'EPD', 'FOX', 'FOXA', 'GM', 'MU', 'MPLX', 'NEM', 'NTRS', 'PSX', 'PPL', 'RY', 'RCL', 'SNE', 'SO', 'SOLN', 'SLF', 'SYF', 'TRP', 'BNS', 'TD', 'USB', 'UAL', 'WBA']
# snpSymbols = ['HDB','GOOG','MSFT']
roce_dict = {}
sort_dict = {}
avg_dict = {}
negative_roce_companies = []
data_unavailable_companies = []
positive_eps_companies = []
final_companies = []
threshold = 12  # ROCE % threshold


def calc_roce(comp1, url, url2):
    try:
        request = urlopen(url)
        response = request.read()
        data = json.loads(response)
        # print (data)
        datesIncome = []
        datesBalance = []
        ta = []
        tcl = []
        ebit = []
        eps = []
        n = 0
        m = 0

        # for i in data['financials']:
        #  print (i.date)
        for key, value in data.items():
            if key == "financials":
                tmp = value
                # print("tmp:")
                # print (tmp)
                for lst_item in tmp:
                    for key, value in lst_item.items():
                        # print('key: {} value: {}'.format(key, value))
                        if key == "date":
                            datesIncome.append(value)
                        elif key == "operatingIncome":
                            ebit.append(value)
                        elif key == "EPS":
                            eps.append(value)
        # print (datesIncome)
        # print ("EBIT: \n")
        # print (ebit)
        # print("Last year's EPS: \n")
        # print(eps[-1])
        if int(float(eps[-1])) >= 0:
            positive_eps_companies.append(comp1)
        request.close()
        # Second Page
        # print (url2)
        request = urlopen(url2)
        response = request.read()
        data = json.loads(response)
        if not data.get("financials"):
            print("Data not available. Manual check may be needed for this company.")
        for key, value in data.items():
            if key == "financials":
                tmp = value
                # print (tmp)
                for lst_item in tmp:
                    for key, value in lst_item.items():
                        # print('key: {} value: {}'.format(key, value))
                        if key == "date":
                            datesBalance.append(value)
                        elif key == "Total assets":
                            ta.append(value)
                        elif key == "Total current liabilities":
                            tcl.append(value)

        # print ("TA: \n")
        # print (ta)
        # print ("TCL: \n")
        # print (tcl)
        request.close()
        # print ("Done")
        n = len(datesIncome)
        m = len(datesBalance)

        if areEqual(datesIncome, datesBalance, n, m):
            print(
                "******************************Data available*******************************************"
                + "\n"
            )
            for i in range(0, len(ta)):
                # print (float(re.sub("[^\\d\\.\\-]", "", tcl[i])))
                roce = (
                    100
                    * float(re.sub("[^\d\.\-]", "", ebit[i]))
                    / (
                        float((re.sub("[^\d\.\-]", "", ta[i])))
                        - float((re.sub("[^\d\.\-]", "", tcl[i])))
                    )
                )
                if roce > 0:
                    print(
                        f"Inc. Stmt Date: {datesIncome[n-1-i]}, Balance Sheet Date: {datesBalance[n-1-i]} and ROCE on that date was {roce:.2f}%"
                    )
                    print("EBIT: " + ebit[i])
                    print("TA: " + ta[i])
                    print("TCL: " + tcl[i] + "\n")
                    if comp1 in roce_dict.keys():
                        roce_dict.setdefault(comp1, []).append(round(roce, 2))
                elif roce < 0:
                    if comp1 not in negative_roce_companies:
                        negative_roce_companies.append(comp1)
                    print("Negative ROCE" + "\n")
                    # print(Style.RESET_ALL)
                    # print (f'Date: {datesIncome[i]} and ROCE on that date was {roce:.2f}%'+"\n")
                    # if comp1 in roce_dict.keys():
                    # roce_dict.setdefault(comp1, []).append(round(roce, 2))
        else:
            print(
                "The income statement and balance sheet could not be found for the same dates."
            )
            data_unavailable_companies.append(comp1)

    except ZeroDivisionError:
        print("Some data not available (Zero division error)" + "\n")
        data_unavailable_companies.append(comp1)
        print(
            "*****************************************************************************"
            + "\n"
        )
    except ValueError:
        print("Some data not available (Value)" + "\n")
        data_unavailable_companies.append(comp1)
        print(
            "*****************************************************************************"
            + "\n"
        )
    except IndexError:
        print("Data not available (Index)" + "\n")
        data_unavailable_companies.append(comp1)
        print(
            "*****************************************************************************"
            + "\n"
        )
    except AttributeError as err:
        print("Data not available (Attribute)" + "\n")
        data_unavailable_companies.append(comp1)
        print(
            "*****************************************************************************"
            + "\n"
        )
        logger.warning("The data was not available: {}".format(err) + "\n")
    return


def get_positive(val1):
    try:
        val = int(val1)
        if val >= 0:
            return True
        else:
            return False
    except ValueError:
        return False


def areEqual(arr1, arr2, n, m):
    if n != m:
        return False
    # Sort both arrays
    arr1.sort()
    arr2.sort()
    # Linearly compare elements
    for i in range(0, n - 1):
        if arr1[i] != arr2[i]:
            return False
    # If all elements were same.
    return True


for i in range(0, len(snpSymbols)):  # len(dowSymbols)
    try:
        # Basic API URL
        my_value_a = os.getenv("MY_VAR_A")
        url_is_y = (
            "https://financialmodelingprep.com/api/v3/financials/income-statement/"
            + snpSymbols[i]
            + "?apikey="
            + my_value_a
        )
        url_bs_y = (
            "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/"
            + snpSymbols[i]
            + "?apikey="
            + my_value_a
        )
        # url_bs_y = 'https://finnhub.io/api/v1/stock/financials?symbol='+ snpSymbols[i] + '&statement=bs&freq=annual&token='
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        roce_dict[snpSymbols[i]] = []
        # print (dowSymbols[i] + " Quarterly:")
        # roce_q = calc_roce (dowSymbols[i], url_is_q,url_bs_q)
        print(snpSymbols[i] + " Yearly:")
        calc_roce(snpSymbols[i], url_is_y, url_bs_y)
        # print("ROCE Dict")
        # print(roce_dict)
        tmp = np.diff(roce_dict[snpSymbols[i]])
        # print ('The magic number is {}'.format(sum(tmp)*-1))
        sort_dict[snpSymbols[i]] = round(
            ((sum(tmp) * -1) / (len(tmp) + 1)), 2
        )  # This is the magic number: Upen
        # print ("Sorted Dict:")
        # print (sort_dict)
        avg_dict[snpSymbols[i]] = round(
            sum(roce_dict[snpSymbols[i]]) / len(roce_dict[snpSymbols[i]]), 2
        )
    # print("Avg. Dict")
    # print(avg_dict)
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
# print("The order of companies from best to worst (based on year-on-year growth of ROCE):")
# print(sorted(sort_dict.items(), key=lambda x: x[1], reverse=True))
# print("List of data available companies: ")
data_available_companies = set(snpSymbols) ^ set(data_unavailable_companies)
# print(data_available_companies)
print("List excluding negative ROCE companies: ")
print(set(snpSymbols) ^ set(negative_roce_companies))
final_companies = dict((k, v) for k, v in avg_dict.items() if v >= threshold)
# print("Final companies: ")
# print (final_companies)
print("List of companies meeting the threshold: ")
print(sorted(final_companies.items(), key=lambda x: x[1], reverse=True))
print("List of companies meeting the threshold and whose data is available: ")
kv = [(k, final_companies[k])
      for k in data_available_companies if k in final_companies]
lv = sorted(kv, key=lambda x: x[1], reverse=True)
print(lv)
print(
    "List of companies meeting the threshold, whose data is available and have positive EPS: "
)
kv = [(k, final_companies[k])
      for k in positive_eps_companies if k in final_companies]
lv = sorted(kv, key=lambda x: x[1], reverse=True)
print(lv)
print("Data unavailable companies: ")
print(data_unavailable_companies)
print("********************************************" + "\n")
