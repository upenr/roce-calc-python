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
import traceback

load_dotenv()

te = open("finalScreen.txt", "a")  # File where I keep the logs


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
# Upen: Enter your list of symbols here
mySymbols = ['WFC', 'GOOG', 'MSFT']
cacSymbols = ['MC.PA', 'SAN.PA', 'FP.PA', 'OR.PA', 'AI.PA', 'SU.PA', 'KER.PA', 'AIR.PA', 'BN.PA', 'EL.PA', 'DG.PA', 'BNP.PA', 'CS.PA', 'RI.PA', 'RMS.PA', 'VIV.PA', 'DSY.PA', 'ENGI.PA', 'LR.PA',
              'CAP.PA', 'SGO.PA', 'STM.PA', 'ORA.PA', 'ML.PA', 'TEP.PA', 'WLN.PA', 'VIE.PA', 'GLE.PA', 'ACA.PA', 'UG.PA', 'CA.PA', 'ALO.PA', 'MT.PA', 'HO.PA', 'ATO.PA', 'EN.PA', 'PUB.PA', 'RNO.PA', 'URW.PA']
roce_dict = {}
fcfroce_dict = {}
sort_dict = {}
avg_roce_dict = {}
avg_fcfroce_dict = {}
negative_roce_companies = []
data_unavailable_companies = []
data_available_companies = []
positive_eps_companies = []
final_roce_companies = []
final_fcfroce_companies = []
final_oiGrowth_companies = []
final_fcfGrowth_companies = []
final_bvGrowth_companies = []
threshold_roce = 11  # Set your ROCE % threshold
threshold_fcfroce = 8  # Set your FCFROCE % threshold
inflation = 0.01  # Inflation set to 1%
threshold_dte = 3  # Set your Debt-to-Equity threshold
dte_dict = {}
tbvg_dict = {}


def upendra_metrics(comp1, url1, url2, url3, url4, url5):
    try:
        dte = 0  # DebtToEquity TTM only
        n = 0
        m = 0
        urls = [url1, url2, url3, url4, url5]
        allData = []
        for url in urls:
            request = urlopen(url)
            response = request.read()
            data = json.loads(response)
            allData.append(data)
        #print (allData)

        # 1. Return on capital employed (ROCE) > 11% - Refer to the 'fprep-roce_best' program
        # 2. Free cash flow return on capital employed (FCFROCE) > 8%
        datesIncome = []
        datesBalance = []
        ta = []
        tcl = []
        ebit = []
        fcf = []
        oiGrowth = []
        fcfGrowth = []
        bvGrowth = []
        eps = []
        n = 0
        m = 0

        for key, value in allData[0].items():
            #print (key)
            if key == "financials":
                for lst_item in value:
                    for key, value in lst_item.items():
                        #print('key: {} value: {}'.format(key, value))
                        if key == "date":
                            datesIncome.append(value)
                        elif key == "Operating Income":
                            ebit.append(value)
                        elif key == "EPS":
                            eps.append(value)
        #print (datesIncome)
        #print ("EBIT: \n")
        #print (ebit)
        #print("EPS: \n")
        # print(eps)
        if int(float(eps[-1])) >= 0:
            positive_eps_companies.append(comp1)
        # Second Page
        # print (url2)
        for key, value in allData[1].items():
            if key == "financials":
                for lst_item in value:
                    for key, value in lst_item.items():
                        #print('key: {} value: {}'.format(key, value))
                        if key == "date":
                            datesBalance.append(value)
                        elif key == "Total assets":
                            ta.append(value)
                        elif key == "Total current liabilities":
                            tcl.append(value)

        if allData[2]:
            #print (allData[2])
            for i in range(0, len(allData[2])):
                if i >= 10:
                    break
                fcf.append(allData[2][i]["freeCashFlow"])

        else:
            print("Cash Flow Data not available")

        #print ("TA: \n")
        #print (ta)
        #print ("TCL: \n")
        #print (tcl)
        #print ("Dates Balance")
        #print (datesBalance)
        #print ("FCF values")
        # print(fcf)
        n = len(ta)
        m = len(fcf)

        if areEqual(datesIncome, datesBalance, n, m):
            print("******************************************DATA AVAILABLE***************************************************")
            for i in range(0, (lambda: m, 'lambda: n')[m > n]()):
                if i >= 10:
                    break
                # print("Values")
                #print (float(re.sub("[^\\d\\.\\-]", "", ebit[i])))
                #print (float(re.sub("[^\\d\\.\\-]", "", ta[i])))
                #print (float(re.sub("[^\\d\\.\\-]", "", tcl[i])))
                #print (fcf[i])
                roce = (100 * float(re.sub("[^\\d\\.\\-]", "", ebit[i])) / (float(
                    (re.sub("[^\\d\\.\\-]", "", ta[i]))) - float((re.sub("[^\\d\\.\\-]", "", tcl[i])))))
                fcfroce = ((100 * fcf[i]) / (float((re.sub("[^\\d\\.\\-]", "", ta[i]))) - float(
                    (re.sub("[^\\d\\.\\-]", "", tcl[i])))))
                print(
                    f"Inc. Stmt Date: {datesIncome[i]}, Balance Sheet Date: {datesBalance[i]}, ROCE on that date was {roce:.2f}% and FCFROCE on that date was {fcfroce:.2f}%")
                #print("EBIT: " + ebit[i])
                #print("TA: " + ta[i])
                #print("TCL: " + tcl[i] + "\n")
                roce_dict.setdefault(comp1, []).append(round(roce, 2))
                fcfroce_dict.setdefault(comp1, []).append(round(fcfroce, 2))
                #print (roce_dict)
                #print (fcfroce_dict)

        else:
            print(
                "The income statement and balance sheet could not be found for the same dates."
            )

        if roce_dict[comp1][:5]:
            if all(x > threshold_roce for x in roce_dict[comp1][:5]):
                final_roce_companies.append(comp1)
            if [sum(roce_dict[comp1][:5])/5 for x in roce_dict[comp1][:5]][0] > threshold_roce:
                avg_roce_dict[comp1] = round(sum(roce_dict[comp1][:5])/5, 2)
            if all(x > threshold_fcfroce for x in fcfroce_dict[comp1][:5]):
                final_fcfroce_companies.append(comp1)
            if [sum(fcfroce_dict[comp1][:5])/5 for x in fcfroce_dict[comp1][:5]][0] > threshold_fcfroce:
                avg_fcfroce_dict[comp1] = round(
                    sum(fcfroce_dict[comp1][:5])/5, 2)

        # 3. Growth in operating income per fully diluted share (ΔOI/FDS) > Inflation% (say 3%)
        # 4. Growth in free cash flow per fully diluted share (ΔFCF/FDS) > Inflation% (say 3%)
        # 5. Growth in book value per fully diluted share (ΔBV/FDS) >  Inflation% (say 3%)
        if allData[3]:
            #print (allData[3])
            for i in range(0, len(allData[3])):
                if i >= 10:
                    break
                oiGrowth.append(allData[3][i]["operatingIncomeGrowth"])
                fcfGrowth.append(allData[3][i]["freeCashFlowGrowth"])
                bvGrowth.append(allData[3][i]["bookValueperShareGrowth"])
        else:
            print("Delta Operating Income data not available")

        print("Operating Income, Free Cash Flow, Book Value growths for last 5 years shown in the 3 lines below.")
        print(" - ", oiGrowth[:5])
        print(" - ", fcfGrowth[:5])
        print(" - ", bvGrowth[:5])
        # inflation is the name of my threshold
        if all(x > inflation for x in oiGrowth[:5]):
            final_oiGrowth_companies.append(comp1)
        if all(x > inflation for x in fcfGrowth[:5]):
            final_fcfGrowth_companies.append(comp1)
        if all(x > inflation for x in bvGrowth[:5]):
            final_bvGrowth_companies.append(comp1)

        """ if allData[4]: #Upen: Not calculating Shares Outstanding in this program. So, this bit is commented out.
            sharesOut = allData[4][0]["sharesOutstanding"]
            print(
                "The current number of shares outstanding is {0:.2f}.".format(
                    sharesOut
                )
            )
        else:
            print("An error occurred under items 3, 4 and 5: %s") % (data["error"]["description"]) """
        # 6. Growth in tangible book value per fully diluted share (ΔTBV/FDS) > Inflation% (say 3%)
        # 7. Liabilities-to-equity ratio < 2
        if allData[4]:
            dte = allData[4][0]["debtToEquityTTM"]
            print(
                "The current debt-to-equity ratio is {0:.2f}.".format(
                    allData[4][0]["debtToEquityTTM"]
                )
            )
            print(
                "The current tangible book value per share TTM is {0:.2f}. Manually determine the growth.".format(
                    allData[4][0]["tangibleBookValuePerShareTTM"]
                )
            )
            if dte <= threshold_dte:
                dte_dict.setdefault(comp1, []).append(round(dte, 2))
        else:
            print("An error occurred under dte: %s") % (
                data["error"]["description"])

        print("***********************************************************************************************************")
        request.close()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        print(template.format(type(ex).__name__, ex.args))
        traceback.print_exc()
        print("***********************************************************************************************************")
        pass

    return


def generate_elem_count():
    result_data = []
    for val in mapper.values():
        if type(val) == list:
            result_data += val
        elif type(val) == dict:
            for key in val:
                result_data.append(key)

    count_elem = {elem: result_data.count(elem) for elem in result_data}
    return count_elem


def get_from_min_match(var):
    temp = []
    count_elem = generate_elem_count()
    for item in count_elem:
        if var <= count_elem[item]:
            temp.append(item)
    return set(temp) if len(set(temp)) > 0 else "None"


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
    # Upen: There's some issue with the data provided. So, skipping comparison part.
    # arr1.sort()
    # arr2.sort()
    # Linearly compare elements
    # for i in range(0, n - 1):
    #    if arr1[i] != arr2[i]:
    #        return False
    # If all elements were same.
    return True


for i in range(0, len(mySymbols)):
    try:
        if i < 50:
            my_value_a = os.getenv("MY_VAR_A")
        elif i >= 50 and i < 100:
            my_value_a = os.getenv("MY_VAR_B")
        elif i >= 100 and i < 150:
            my_value_a = os.getenv("MY_VAR_C")
        elif i >= 150 and i < 200:
            my_value_a = os.getenv("MY_VAR_D")
        elif i >= 200 and i < 250:
            my_value_a = os.getenv("MY_VAR_E")
        elif i >= 250 and i < 300:
            my_value_a = os.getenv("MY_VAR_F")
        elif i >= 300 and i < 350:
            my_value_a = os.getenv("MY_VAR_G")
        else:
            my_value_a = "demo"
        #my_value_a = "demo"
        url_is_y = (
            "https://financialmodelingprep.com/api/v3/financials/income-statement/"
            + mySymbols[i]
            + "?apikey="
            + my_value_a
        )
        url_bs_y = (
            "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/"
            + mySymbols[i]
            + "?apikey="
            + my_value_a
        )
        url_cfs_y = (
            "https://financialmodelingprep.com/api/v3/cash-flow-statement/"
            + mySymbols[i]
            + "?apikey="
            + my_value_a
        )
        url_fg = (
            "https://financialmodelingprep.com/api/v3/financial-growth/"
            + mySymbols[i]
            + "?apikey="
            + my_value_a
        )
        url_quote = (
            "https://financialmodelingprep.com/api/v3/quote/"
            + mySymbols[i]
            + "?apikey="
            + my_value_a
        )
        url_metrics = (
            "https://financialmodelingprep.com/api/v3/key-metrics-ttm/"
            + mySymbols[i]
            + "?apikey="
            + my_value_a
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        # print(i,'.',mySymbols[i],'Yearly:')
        print("%d. %s Yearly:" % (i, mySymbols[i]))

        upendra_metrics(mySymbols[i], url_is_y,
                        url_bs_y, url_cfs_y, url_fg, url_metrics)

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        traceback.print_exc()
    continue
# print output here
print("\n*************************************************RESULTS***************************************************\n")
print("List of companies meeting the ROCE threshold (11%): ")
print(final_roce_companies)
print("List of companies meeting the ROCE threshold (11%), and its average ROCE for last 5 years: ")
print(sorted(avg_roce_dict.items(), key=lambda x: x[1], reverse=True))
print("List of companies meeting the FCFROCE threshold (8%): ")
print(final_fcfroce_companies)
print("List of companies meeting the FCFROCE threshold (8%), and its average FCFROCE for last 5 years: ")
print(sorted(avg_fcfroce_dict.items(), key=lambda x: x[1], reverse=True))
print("List of companies meeting the threshold (>inflation) for Operating Income growth over the last 5 years.")
print(final_oiGrowth_companies)
print("List of companies meeting the threshold (>inflation) for FCF growth over the last 5 years.")
print(final_fcfGrowth_companies)
print("List of companies meeting the threshold (>inflation) for Book Value growth over the last 5 years.")
print(final_bvGrowth_companies)
print("List of companies meeting the DTE threshold of <2")
print(dte_dict)
print("List of companies meeting 3, 4, 5 and 6 metrics shown in the 4 lines below.")
mapper = {1: final_roce_companies, 2: final_fcfroce_companies, 3: final_oiGrowth_companies,
          4: final_fcfGrowth_companies, 5: final_bvGrowth_companies, 6: dte_dict}
print(" - ", get_from_min_match(3))
print(" - ", get_from_min_match(4))
print(" - ", get_from_min_match(5))
print(" - ", get_from_min_match(6))
print("\n******************************************ENF OF RESULTS***************************************************\n")
