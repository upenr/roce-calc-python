# Author: Upendra Rajan
# This makes 6 API calls for each company listed in mySymbols

import json
import re
import logging
from urllib.request import urlopen
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
import time
import traceback
import sqlite3

dbase = sqlite3.connect('stock-dcf-terminal.db')  # Open a database File
cursor = dbase.cursor()
print('Database opened')
print('Cursor created')

dbase.execute(''' CREATE TABLE IF NOT EXISTS six_metrics_screener_data(
    DATE TIMESTAMP NOT NULL UNIQUE,
    TICKER TEXT NOT NULL,
    NAME TEXT NOT NULL,
    CURRENTPRICE INT NULL, 
    YEARLOW INT NULL,
    YEARHIGH INT NULL,
    STATEMENTDATE TEXT NOT NULL UNIQUE,    
    ROCE INT NULL,
    FCFROCE INT NULL,
    OPERATINGINCOMEGROWTH INT NULL,
    FCFGROWTH INT NULL,
    BOOKVALUEGROWTH INT NULL,
    DTOERATIO INT NULL,
    TANGIBLEBVPS INT NULL,
    SHARESOUTSTANDING INT NULL) ''')

dbase.execute(''' CREATE TABLE IF NOT EXISTS companies_meeting_metrics_final(
    DATE TIMESTAMP NOT NULL,
    TICKER TEXT NOT NULL UNIQUE,
    NUMBEROFMETRICSMET INT NULL) ''')

dbase.execute(''' CREATE TABLE IF NOT EXISTS data_unavailable_companies(
    DATE TIMESTAMP NOT NULL,
    TICKER TEXT NOT NULL UNIQUE) ''')

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Upen: Enter your list of symbols here OR uncomment the read_Data() function call, and use Sqlite DB as input.
mySymbols = ['MMM', 'AOS', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADM', 'ADBE', 'ADP', 'AAP', 'AES', 'AFL', 'A', 'AIG', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AMD', 'AEE', 'AAL', 'AEP', 'AXP', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ANET', 'AIZ', 'T', 'ATO', 'ADSK', 'AZO', 'AVB', 'AVY', 'BKR', 'BLL', 'BAC', 'BBWI', 'BAX', 'BDX', 'WRB', 'BRK.B', 'BBY', 'BIO', 'TECH', 'BIIB', 'BLK', 'BK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BF.B', 'CHRW', 'CDNS', 'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CTLT', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'CNC', 'CNP', 'CDAY', 'CERN', 'CF', 'CRL', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'COP', 'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CTVA', 'COST', 'CTRA', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'XRAY', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DISH', 'DIS', 'DG', 'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DTE', 'DUK', 'DRE', 'DD', 'DXC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ENPH', 'ETR', 'EOG', 'EPAM', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ETSY', 'RE', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS', 'FAST', 'FRT', 'FDX', 'FITB', 'FRC', 'FE', 'FIS', 'FISV', 'FLT', 'FMC', 'F', 'FTNT', 'FTV', 'FBHS', 'FOXA', 'FOX', 'BEN', 'FCX', 'AJG', 'GRMN', 'IT', 'GE', 'GNRC', 'GD', 'GIS', 'GPC', 'GILD', 'GL', 'GPN', 'GM', 'GS', 'GWW', 'HAL', 'HIG', 'HAS', 'HCA', 'PEAK', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUM', 'HII', 'HBAN', 'IEX', 'IDXX', 'ITW', 'ILMN', 'INCY', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IPGP', 'IQV', 'IRM', 'JBHT', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN', 'LLY', 'LNC', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LUMN', 'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'FB', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NDSN', 'NSC', 'NTRS', 'NOC', 'NLOK', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC', 'OKE', 'ORCL', 'OGN', 'OTIS', 'PCAR', 'PKG', 'PARA', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PENN', 'PNR', 'PEP', 'PKI', 'PFE', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PTC', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RHI', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SEE', 'SRE', 'NOW', 'SHW', 'SBNY', 'SPG', 'SWKS', 'SJM', 'SNA', 'SEDG', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STE', 'SYK', 'SIVB', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO', 'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TWTR', 'TYL', 'TSN', 'USB', 'UDR', 'ULTA', 'UAA', 'UA', 'UNP', 'UAL', 'UNH', 'UPS', 'URI', 'UHS', 'VLO', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VFC', 'VTRS', 'V', 'VNO', 'VMC', 'WAB', 'WMT', 'WBA', 'WBD', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WRK', 'WY', 'WHR', 'WMB', 'WTW', 'WYNN', 'XEL', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']

def read_Data():
    # from math import *
    data = cursor.execute(
        ''' SELECT TICKER FROM dcf_analysis_upen WHERE DISCOUNTINPERCENT BETWEEN 0.5 AND 1 ORDER BY DISCOUNTINPERCENT DESC''')
    for record in data:
        #print ("'"+str(record[0])+"'"+'\n')
        mySymbols.append(str(record[0]))
# cacSymbols = ['MC.PA', 'SAN.PA', 'FP.PA', 'OR.PA', 'AI.PA', 'SU.PA', 'KER.PA', 'AIR.PA', 'BN.PA', 'EL.PA', 'DG.PA', 'BNP.PA', 'CS.PA', 'RI.PA', 'RMS.PA', 'VIV.PA', 'DSY.PA', 'ENGI.PA', 'LR.PA',
#              'CAP.PA', 'SGO.PA', 'STM.PA', 'ORA.PA', 'ML.PA', 'TEP.PA', 'WLN.PA', 'VIE.PA', 'GLE.PA', 'ACA.PA', 'UG.PA', 'CA.PA', 'ALO.PA', 'MT.PA', 'HO.PA', 'ATO.PA', 'EN.PA', 'PUB.PA', 'RNO.PA', 'URW.PA']
#dowSymbols = ['MMM', 'AMGN', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PG', 'CRM', 'TRV', 'UNH', 'VZ', 'V', 'WBA', 'WMT', 'DIS']
roce_dict = {}
fcfroce_dict = {}
sort_dict = {}
avg_roce_dict = {}
avg_fcfroce_dict = {}
negative_roce_companies = []
data_unavailable_companies = []
positive_eps_companies = []
final_roce_companies = []
final_fcfroce_companies = []
final_oiGrowth_companies = []
final_fcfGrowth_companies = []
final_bvGrowth_companies = []
threshold_roce = 10  # Set your ROCE % threshold
threshold_fcfroce = 7  # Set your FCFROCE % threshold
inflation = 0.05  # Inflation set to 5%
threshold_dte = 2  # Set your Debt-to-Equity threshold
dte_dict = {}
tbvg_dict = {}
count_elem = {}


def upendra_metrics(comp1, url1, url2, url3, url4, url5, url6):
    try:
        dte = 0  # DebtToEquity TTM only
        n = 0
        m = 0
        urls = [url1, url2, url3, url4, url5, url6]
        allData = []
        for url in urls:
            request = urlopen(url)
            time.sleep(1)
            response = request.read()
            data = json.loads(response)
            allData.append(data)
        # print(allData)

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

        for data in allData[0]:
            #print ("Data: " + str(data))
            for key, value in data.items():
                if key == "date":
                    datesIncome.append(value)
                elif key == "operatingIncome":
                    if (float(value) == 0.0):
                        key = "incomeBeforeTax"
                    else:
                        ebit.append(value)
                elif key == "incomeBeforeTax":
                    #print ("Using Income Before Tax instead of Operating Income. Maybe, this is a bank?")
                    ebit.append(value)
                elif key == "eps":
                    eps.append(value)

        """         if allData[0]:
            datesIncome.append(allData[0][0]["date"])
            ebit.append(allData[0][0]["operatingIncome"] if allData[0][0]["operatingIncome"]
                        > 0 else allData[0][0]["incomeBeforeTax"])  # if = 0, make it earnings before tax
            eps.append(allData[0][0]["eps"]) """

        print(datesIncome)
        #print("EBIT: \n")
        # print(ebit)
        #print("EPS: \n")
        # print(eps)
        if int(float(eps[-1])) >= 0:
            positive_eps_companies.append(comp1)
        # Second Page
        # print (url2)

        for data in allData[1]:
            #print ("Data: " + str(data))
            for key, value in data.items():
                if key == "date":
                    datesBalance.append(value)
                elif key == "totalAssets":
                    ta.append(value)
                elif key == "totalCurrentLiabilities":
                    tcl.append(value)

        if allData[2]:
            #print (allData[2])
            for i in range(0, len(allData[2])):
                if i >= 10:
                    break
                fcf.append(allData[2][i]["freeCashFlow"])

        else:
            print("Balance Sheet Data not available")

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

        if areEqual(datesIncome, datesBalance, n):
            print("******************************************DATA AVAILABLE***************************************************")
            for i in range(0, (lambda: m, lambda: n)[m > n]()):
                if i >= 10:
                    break
                # print("Values")
                roce = (100 * float(re.sub("[^\\d\\.\\-]", "", str(ebit[i]))) / (float((re.sub(
                    "[^\\d\\.\\-]", "", str(ta[i])))) - float((re.sub("[^\\d\\.\\-]", "", str(tcl[i]))))))
                fcfroce = ((100 * fcf[i]) / (float((re.sub("[^\\d\\.\\-]", "", str(
                    ta[i])))) - float((re.sub("[^\\d\\.\\-]", "", str(tcl[i]))))))
                print(
                    f"Inc. Stmt Date: {datesIncome[i]}, Balance Sheet Date: {datesBalance[i]}, ROCE on that date was {roce:.2f}% and FCFROCE on that date was {fcfroce:.2f}%")
                #print("EBIT: " + str(ebit[i]))
                #print("TA: " + str(ta[i]))
                #print("TCL: " + str(tcl[i]) + "\n")
                roce_dict.setdefault(comp1, []).append(round(roce, 2))
                fcfroce_dict.setdefault(comp1, []).append(round(fcfroce, 2))
                #print (roce_dict)
                #print (fcfroce_dict)

        else:
            print(
                "The income statement and balance sheet data do not have the same dates."
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
        bank = 0
        if allData[3]:
            #print (allData[3])
            for i in range(0, len(allData[3])):
                if i >= 10:
                    break
                if (float(allData[3][0]["operatingIncomeGrowth"]) != 0.0 and float(allData[3][0]["bookValueperShareGrowth"]) != 0.0):
                    oiGrowth.append(allData[3][i]["operatingIncomeGrowth"])
                    fcfGrowth.append(allData[3][i]["freeCashFlowGrowth"])
                    bvGrowth.append(allData[3][i]["bookValueperShareGrowth"])
                else:
                    oiGrowth.append(allData[3][i]["netIncomeGrowth"])
                    fcfGrowth.append(allData[3][i]["freeCashFlowGrowth"])
                    bvGrowth.append(allData[3][i]["assetGrowth"])
                    if (bank != 1):
                        bank = 1

        else:
            print("Cash Flow Statement data not available")

        print("Operating Income, Free Cash Flow, Book Value growths for last 5 years shown in the 3 lines below.")
        print(" - ", oiGrowth[:5])
        print(" - ", fcfGrowth[:5])
        print(" - ", bvGrowth[:5])
        if (bank == 1):
            print("* Using EBT instead of OI, Net Income Growth instead of OI Growth and Total Asset Growth instead of Book Value Growth.")
        # inflation is the name of my threshold
        if all(x > inflation for x in oiGrowth[:5]):
            final_oiGrowth_companies.append(comp1)
        if all(x > inflation for x in fcfGrowth[:5]):
            final_fcfGrowth_companies.append(comp1)
        if all(x > inflation for x in bvGrowth[:5]):
            final_bvGrowth_companies.append(comp1)

        # 6. Growth in tangible book value per fully diluted share (ΔTBV/FDS) > Inflation% (say 3%)
        # 7. Liabilities-to-equity ratio < 2
        if allData[4]:
            sharesOut = allData[4][0]["sharesOutstanding"]
            share_price = allData[4][0]["price"]
            share_name = allData[4][0]["name"]
            year_high = allData[4][0]["yearHigh"]
            year_low = allData[4][0]["yearLow"]

        else:
            print("An error occurred under dte: %s") % (
                data["error"]["description"])

        if allData[5]:
            dte = allData[5][0]["debtToEquityTTM"]
            tbvps = allData[5][0]["tangibleBookValuePerShareTTM"]
            print(
                "The current debt-to-equity ratio is {0:.2f}.".format(
                    dte
                )
            )
            print(
                "The current tangible book value per share TTM is {0:.2f}. Manually determine the growth.".format(
                    tbvps)
            )
            if dte <= threshold_dte:
                dte_dict.setdefault(comp1, []).append(round(dte, 2))

        else:
            print("An error occurred under dte: %s") % (
                data["error"]["description"])

        print("***********************************************************************************************************")
        for x in range(0, len(datesIncome)):
            dbase.execute("INSERT OR REPLACE INTO six_metrics_screener_data (DATE, TICKER, NAME, CURRENTPRICE, YEARLOW, YEARHIGH, STATEMENTDATE, ROCE, FCFROCE, OPERATINGINCOMEGROWTH, FCFGROWTH, BOOKVALUEGROWTH, DTOERATIO, TANGIBLEBVPS, SHARESOUTSTANDING) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (datetime.today(), comp1, share_name, share_price, year_low, year_high, datesIncome[x], roce_dict[comp1][x], fcfroce_dict[comp1][x], oiGrowth[x], fcfGrowth[x], bvGrowth[x], dte if x == 0 else None, tbvps if x == 0 else None, sharesOut if x == 0 else None))
            dbase.commit()
            #print ("datesIncome[x]: " + str(datesIncome[x]))
        request.close()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        print(template.format(type(ex).__name__, ex.args))
        traceback.print_exc()
        data_unavailable_companies.append(comp1)
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


def areEqual(arr1, arr2, n):
    # Upen: There's some issue with the data provided. So, skipping comparison part.
    arr1.sort()
    arr2.sort()
    # Linearly compare elements
    for i in range(0, n - 1):
        if arr1[i] != arr2[i]:
            return False
    # If all elements were tthe same, return true
    return True

#read_Data()

def get_env_var(i):
    try:
        letter = ['I', 'K', 'J', 'F', 'G', 'C', 'D', 'E', 'N', 'L', 'A', 'B', 'H', 'M'][i // 40]
        return os.getenv("MY_VAR_" + letter)
    except IndexError:
        return "demo"


for i in range(0, len(mySymbols)):
    try:
        my_value_a = get_env_var(i)
        #my_value_a = "demo"
        #my_value_a =  os.getenv("MY_VAR_K")
        url_is_y = (
            "https://financialmodelingprep.com/api/v3/income-statement/"
            + mySymbols[i]
            + "?apikey="
            + my_value_a
        )
        url_bs_y = (
            "https://financialmodelingprep.com/api/v3/balance-sheet-statement/"
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

        upendra_metrics(mySymbols[i], url_is_y, url_bs_y,
                        url_cfs_y, url_fg, url_quote, url_metrics)

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        traceback.print_exc()
    continue
# print output here
print("\n*************************************************RESULTS***************************************************\n")
print("Data unavailable companies:")
print(data_unavailable_companies)
print("List of companies meeting the ROCE threshold (11%) every year for the last 5 years: ")
print(final_roce_companies)
print("List of companies meeting the ROCE threshold (11%), and its average ROCE for last 5 years: ")
print(sorted(avg_roce_dict.items(), key=lambda x: x[1], reverse=True))
print("List of companies meeting the FCFROCE threshold (8%) every year for the last 5 years: ")
print(final_fcfroce_companies)
print("List of companies meeting the FCFROCE threshold (8%), and its average FCFROCE for last 5 years: ")
print(sorted(avg_fcfroce_dict.items(), key=lambda x: x[1], reverse=True))
print("List of companies meeting the threshold (>inflation) each year for Operating Income growth for the last 5 years.")
print(final_oiGrowth_companies)
print("List of companies meeting the threshold (>inflation) each year for FCF growth for the last 5 years.")
print(final_fcfGrowth_companies)
print("List of companies meeting the threshold (>inflation) each year for Book Value growth for the last 5 years.")
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

metrics_matched = generate_elem_count()
#print (metrics_matched)

for key, value in metrics_matched.items():
    dbase.execute("INSERT OR REPLACE INTO companies_meeting_metrics_final (DATE, TICKER, NUMBEROFMETRICSMET) \
            VALUES (?,?,?)", (datetime.today(), str(key), value))
    dbase.commit()

for item in data_unavailable_companies:
    dbase.execute("INSERT OR REPLACE INTO data_unavailable_companies (DATE, TICKER) \
            VALUES (?,?)", (datetime.today(), item))
    dbase.commit()
