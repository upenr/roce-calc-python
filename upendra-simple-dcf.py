# Author: Upendra Rajan
# This makes 3 API calls per company listed in mySymbols

import json
import logging
import sqlite3
import sys
import os
import traceback
from datetime import datetime
from dotenv import load_dotenv
import time
from urllib.request import urlopen

dbase = sqlite3.connect('stock-dcf-data.db')  # Open a database File
cursor = dbase.cursor()
print('Database opened')
print('Cursor created')

dbase.execute(''' CREATE TABLE IF NOT EXISTS dcf_analysis_upen(
    DATE TIMESTAMP NOT NULL,
    TICKER TEXT NOT NULL UNIQUE,
    NAME TEXT NOT NULL,
    CURRENTPRICE INT NULL, 
    DCFPRICE INT NULL,    
    DISCOUNTINPERCENT INT NULL,
    YEARLOW INT NULL,
    YEARHIGH INT NULL) ''')

print('Table created')

load_dotenv()

te = open("dcfScreen.txt", "a")  # File where I keep the logs


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
# Upendra: Enter your list of symbols here
mySymbols = ['RICK', 'BFIN']
# cacSymbols = ['MC.PA', 'SAN.PA', 'FP.PA', 'OR.PA', 'AI.PA', 'SU.PA', 'KER.PA', 'AIR.PA', 'BN.PA', 'EL.PA', 'DG.PA', 'BNP.PA', 'CS.PA', 'RI.PA', 'RMS.PA', 'VIV.PA', 'DSY.PA', 'ENGI.PA', 'LR.PA',
#              'CAP.PA', 'SGO.PA', 'STM.PA', 'ORA.PA', 'ML.PA', 'TEP.PA', 'WLN.PA', 'VIE.PA', 'GLE.PA', 'ACA.PA', 'UG.PA', 'CA.PA', 'ALO.PA', 'MT.PA', 'HO.PA', 'ATO.PA', 'EN.PA', 'PUB.PA', 'RNO.PA', 'URW.PA']
data_unavailable_companies = []
intrinsic_price_meeting_companies = {}
mos_meeting_companies = {}


def upendra_simple_dcf(comp1, url1, url2, url3):
    try:
        urls = [url1, url2, url3]
        allData = []
        total_cash = 0
        wc_total_cash = 0
        bc_total_cash = 0
        datesBalance = []
        cce = []
        tcl = []
        ocf = []
        discount_rate = 0.05  # 0.04 means 4%. Change it to anything you like.
        # This is expected cash flow growth for years 1 to 5 in a normal scenario.
        cfg_y1_y5 = 0.15
        # This is expected cash flow growth for years 6 to 10 in a normal scenario.
        cfg_y6_y10 = 0.10
        # This is expected cash flow growth for years 1 to 5 in the best case scenario.
        bc_cfg_y1_y5 = 0.20
        # This is expected cash flow growth for years 6 to 10 in the best case scenario.
        bc_cfg_y6_y10 = 0.16
        # This is expected cash flow growth for years 1 to 5 in the worst case scenario.
        wc_cfg_y1_y5 = 0.05
        # This is expected cash flow growth for years 6 to 10  in the worst case scenario.
        wc_cfg_y6_y10 = 0.03
        # This will contain ten years' generated cash flow.
        generated_cash = []
        bc_generated_cash = []
        wc_generated_cash = []
        discount_factor = []  # This will contain ten years' discount factor.
        # This will contain ten years' discounted cash each year.
        discounted_cashflow = []
        bc_discounted_cashflow = []
        wc_discounted_cashflow = []
        mos = 0.5  # Enter your margin of safety here. 0.5 indicates 50%.
        year_list = []
        intrinsic_price = 0.0
        share_price = 0
        year_high = 0
        year_low = 0
        
        for url in urls:
            request = urlopen(url)
            time.sleep(1)
            response = request.read()
            data = json.loads(response)
            allData.append(data)
        #print (allData)
        request.close()

        if allData[0]:
            date = allData[0][0]["date"]
            print("The date is {}".format(date))
        else:
            print("An error occurred: %s") % (data["error"]["description"])

        # 1. Get operating cash flow, shares outstanding, current cash and equivalents and total current liabilities
        if allData[0]:
            datesBalance.append(allData[0][0]["date"])
            cce.append(allData[0][0]["cashAndCashEquivalents"]) 
            tcl.append(allData[0][0]["totalCurrentLiabilities"])
        else:
            print("An error occurred: %s") % (data["error"]["description"])
                           
        print(
            "The latest yearly Cash and Cash Equivalent: {cce}.".format(cce=cce[0]))
        print(
            "The latest yearly Total Current Liabilities: {tcl}.".format(tcl=tcl[0]))
        if allData[1]:
            #print (allData[2])
            for i in range(0, len(allData[1])):
                if i >= 10:
                    break
                ocf.append(allData[1][i]["operatingCashFlow"])
        else:
            print("Cash Flow Data not available")
        print(
            "The latest yearly operating cash flow: {ocf}.".format(ocf=ocf[0]))
        generated_cash.append(round(float(ocf[0])))
        bc_generated_cash.append(round(float(ocf[0])))
        wc_generated_cash.append(round(float(ocf[0])))
        for i in range(1, 6):
            generated_cash.append(round(generated_cash[i-1] * (1+cfg_y1_y5)))
            bc_generated_cash.append(
                round(bc_generated_cash[i-1] * (1+bc_cfg_y1_y5)))
            wc_generated_cash.append(
                round(wc_generated_cash[i-1] * (1+wc_cfg_y1_y5)))
        for i in range(6, 11):
            generated_cash.append(round(generated_cash[i-1] * (1+cfg_y6_y10)))
            bc_generated_cash.append(
                round(bc_generated_cash[i-1] * (1+bc_cfg_y6_y10)))
            wc_generated_cash.append(
                round(wc_generated_cash[i-1] * (1+wc_cfg_y6_y10)))
        year_list.append(round(float(datesBalance[0][0:4])))
        discount_factor.append(1.0)
        discounted_cashflow.append(generated_cash[0])
        bc_discounted_cashflow.append(generated_cash[0])
        wc_discounted_cashflow.append(generated_cash[0])
        for i in range(1, 11):
            year_list.append(year_list[i-1]+1)
            discount_factor.append(
                round(float(1/((1+discount_rate)**(year_list[i]-year_list[0]))), 2))
            discounted_cashflow.append(generated_cash[i]*discount_factor[i])
            bc_discounted_cashflow.append(
                bc_generated_cash[i]*discount_factor[i])
            wc_discounted_cashflow.append(
                wc_generated_cash[i]*discount_factor[i])

        for ele in range(1, len(discounted_cashflow)):
            total_cash = total_cash + discounted_cashflow[ele]
        for ele in range(1, len(wc_discounted_cashflow)):
            wc_total_cash = wc_total_cash + wc_discounted_cashflow[ele]
        for ele in range(1, len(bc_discounted_cashflow)):
            bc_total_cash = bc_total_cash + bc_discounted_cashflow[ele]

        if allData[2]:
            sharesOut = allData[2][0]["sharesOutstanding"]
            share_price = allData[2][0]["price"]
            share_name = allData[2][0]["name"]
            year_high = allData[2][0]["yearHigh"]
            year_low = allData[2][0]["yearLow"]
            print(
                "The current number of shares outstanding is {0:.2f}.".format(
                    sharesOut
                )
            )
            print("The current price is {0:.2f}.".format(share_price))
        else:
            print("An error occurred under items 3, 4 and 5: %s") % (
                data["error"]["description"])

        print("Years:")
        print(year_list)
        print("Discount factor:")
        print(discount_factor)
        tcso = round(total_cash/sharesOut, 2)
        wc_tcso = round(wc_total_cash/sharesOut, 2)
        bc_tcso = round(bc_total_cash/sharesOut, 2)
        ccash = round(float(cce[0])/sharesOut, 2)
        cdebt = round(float(tcl[0])/sharesOut, 2)
        print("\nWORST CASE:\n")
        print("Worst case: Generated cash over the next ten years")
        print(wc_generated_cash)
        print("Worst case: Discounted cash flow")
        print(wc_discounted_cashflow)
        print("Worst Case: Cash flow over the next 10 years:")
        print(round(wc_total_cash, 2))
        print("Worst case - Total cash over the next 10 years per outstanding share is: " + str(wc_tcso))
        print("Adding current cash per share {a} and subtracting current debt per share {b}.".format(
            a=ccash, b=cdebt))
        wc_intrinsic_price = wc_tcso+ccash-cdebt
        print("Worst case - Intrinsic value per share:")
        print(wc_intrinsic_price)
        print("\nNORMAL CASE:\n")
        print("Normal case: Generated cash over the next ten years")
        print(generated_cash)
        print("Normal case: Discounted cash flow")
        print(discounted_cashflow)
        print("Normal Case: Cash flow over the next 10 years:")
        print(round(total_cash, 2))
        print("Normal case - Total cash over the next 10 years per outstanding share is: " + str(tcso))
        print("Adding current cash per share {a} and subtracting current debt per share {b}.".format(
            a=ccash, b=cdebt))
        intrinsic_price = tcso+ccash-cdebt
        print("Normal case - Intrinsic value per share:")
        print(intrinsic_price)
        print("\nBEST CASE:\n")
        print("Best case: Generated cash over the next ten years")
        print(bc_generated_cash)
        print("Best case: Discounted cash flow")
        print(bc_discounted_cashflow)
        print("Best Case: Cash flow over the next 10 years:")
        print(round(bc_total_cash, 2))
        print("Best case - Total cash over the next 10 years per outstanding share is: " + str(bc_tcso))
        print("Adding current cash per share {a} and subtracting current debt per share {b}.".format(
            a=ccash, b=cdebt))
        bc_intrinsic_price = bc_tcso+ccash-cdebt
        print("Best case - Intrinsic value per share:")
        print(bc_intrinsic_price)
        print("-----------------------------------------------------------------------------------------------------------")
        avg_intrinsic_price = round(
            ((wc_intrinsic_price+intrinsic_price+bc_intrinsic_price)/3), 2)
        print("Average intrinsic value over the three scenarios:")
        print(avg_intrinsic_price)

        if avg_intrinsic_price > 0:
            dbase.execute("INSERT OR REPLACE INTO dcf_analysis_upen (DATE,TICKER,NAME,CURRENTPRICE,DCFPRICE,DISCOUNTINPERCENT,YEARLOW,YEARHIGH) \
            VALUES (?,?,?,?,?,?,?,?)", (datetime.today(), comp1, share_name, share_price, max(0, avg_intrinsic_price), round(((avg_intrinsic_price-share_price)/avg_intrinsic_price), 2), year_low, year_high))
            dbase.commit()

        else:
            dbase.execute("INSERT OR REPLACE INTO dcf_analysis_upen (DATE,TICKER,NAME,CURRENTPRICE,DCFPRICE,DISCOUNTINPERCENT,YEARLOW,YEARHIGH) \
            VALUES (?,?,?,?,?,?,?,?)", (datetime.today(), comp1, share_name, share_price, max(0, avg_intrinsic_price), None, year_low, year_high))
            dbase.commit()

        print("Applying margin of safety of {a}".format(a=mos))
        print(round(avg_intrinsic_price*mos, 2))
        if (share_price < avg_intrinsic_price):
            intrinsic_price_meeting_companies[comp1] = avg_intrinsic_price
        if (share_price < (avg_intrinsic_price*mos)):
            mos_meeting_companies[comp1] = round(avg_intrinsic_price*mos, 2)
        print("***********************************************************************************************************")

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        print(template.format(type(ex).__name__, ex.args))
        traceback.print_exc()
        data_unavailable_companies.append(comp1)
        print("***********************************************************************************************************")
        pass

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


def get_env_var(i):
    try:
        letter = ['A', 'B', 'H', 'I', 'M', 'K', 'L', 'J', 'F', 'G', 'C', 'D', 'E'][i // 82]
        return os.getenv("MY_VAR_" + letter)
    except IndexError:
        return "demo"


for i in range(0, len(mySymbols)):
    try:
        my_value_a = get_env_var(i)
        #my_value_a = "demo"
        #my_value_a =  os.getenv("MY_VAR_K")
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
        url_quote = (
            "https://financialmodelingprep.com/api/v3/quote/"
            + mySymbols[i]
            + "?apikey="
            + my_value_a
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        # print(i,'.',mySymbols[i],'Yearly:')
        print("%d. %s Yearly:" % (i, mySymbols[i]))

        upendra_simple_dcf(mySymbols[i], url_bs_y, url_cfs_y, url_quote)

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
print("Companies whose intrinsic value is less than the current price, shown here with avg. intrinsic value of 3 scenarios:")
print(intrinsic_price_meeting_companies)
print("Companies meeting your margin of safety, shown here with the safest price to pay:")
print(mos_meeting_companies)
print("\n******************************************ENF OF RESULTS***************************************************\n")
