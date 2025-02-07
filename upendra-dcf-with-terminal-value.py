# Author: Upendra Rajan
# This makes 3 API calls per company listed in mySymbols

import json
import logging
import sqlite3
import sys
import os
import traceback
import time
from datetime import datetime
from urllib.request import urlopen
from dotenv import load_dotenv

dbase = sqlite3.connect('stock-dcf-terminal.db')  # Open a database File
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
    YEARHIGH INT NULL,
    MARKETCAP INT NULL) ''')

dbase.execute(''' CREATE TABLE IF NOT EXISTS data_unavailable_companies(
    DATE TIMESTAMP NOT NULL,
    TICKER TEXT NOT NULL UNIQUE) ''')

print('Tables created')

load_dotenv()

class Unbuffered:
    """
    This class provides unbuffered output for the stdout stream. It writes 
    data to both the standard output (stdout) and appends the same data to 
    a log file ('dcfScreen.txt') every time something is printed.

    Attributes:
        stream: The stream object to write to (e.g., sys.stdout).
    """

    def __init__(self, stream):
        """
        Initializes the Unbuffered class with the specified stream.
        
        Args:
            stream: The stream object to write data to (usually sys.stdout).
        """
        self.stream = stream

    def write(self, data):
        """
        Writes the given data to both the standard output and the log file.
        
        Args:
            data (str): The data to write to the output and log file.
        """
        self.stream.write(data)
        self.stream.flush()
        with open("dcfScreen.txt", "a", encoding="utf-8") as te:
            te.write(data)

    def flush(self):
        """
        Flushes the stream to ensure that the written data is output immediately.
        """
        pass


sys.stdout = Unbuffered(sys.stdout)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Upendra: Enter your list of symbols here
mySymbols = ['NVDA']
#mySymbols = ['BABA', 'MMM', 'AOS', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADM', 'ADBE', 'ADP', 'AAP', 'AES', 'AFL', 'A', 'AIG', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AMD', 'AEE', 'AAL', 'AEP', 'AXP', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ANET', 'AIZ', 'T', 'ATO', 'ADSK', 'AZO', 'AVB', 'AVY', 'BKR', 'BLL', 'BAC', 'BBWI', 'BAX', 'BDX', 'WRB', 'BRK.B', 'BBY', 'BIO', 'TECH', 'BIIB', 'BLK', 'BK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BF.B', 'CHRW', 'CDNS', 'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CTLT', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'CNC', 'CNP', 'CDAY', 'CERN', 'CF', 'CRL', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'COP', 'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CTVA', 'COST', 'CTRA', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'XRAY', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DISH', 'DIS', 'DG', 'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DTE', 'DUK', 'DRE', 'DD', 'DXC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ENPH', 'ETR', 'EOG', 'EPAM', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ETSY', 'RE', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS', 'FAST', 'FRT', 'FDX', 'FITB', 'FRC', 'FE', 'FIS', 'FISV', 'FLT', 'FMC', 'F', 'FTNT', 'FTV', 'FBHS', 'FOXA', 'FOX', 'BEN', 'FCX', 'AJG', 'GRMN', 'IT', 'GE', 'GNRC', 'GD', 'GIS', 'GPC', 'GILD', 'GL', 'GPN', 'GM', 'GS', 'GWW', 'HAL', 'HIG', 'HAS', 'HCA', 'PEAK', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUM', 'HII', 'HBAN', 'IEX', 'IDXX', 'ITW', 'ILMN', 'INCY', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IPGP', 'IQV', 'IRM', 'JBHT', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN', 'LLY', 'LNC', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LUMN', 'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'META', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NDSN', 'NSC', 'NTRS', 'NOC', 'NLOK', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC', 'OKE', 'ORCL', 'OGN', 'OTIS', 'PCAR', 'PKG', 'PARA', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PENN', 'PNR', 'PEP', 'PKI', 'PFE', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PTC', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RHI', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SEE', 'SRE', 'NOW', 'SHW', 'SBNY', 'SPG', 'SWKS', 'SJM', 'SNA', 'SEDG', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STE', 'SYK', 'SIVB', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO', 'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TWTR', 'TYL', 'TSN', 'USB', 'UDR', 'ULTA', 'UAA', 'UA', 'UNP', 'UAL', 'UNH', 'UPS', 'URI', 'UHS', 'VLO', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VFC', 'VTRS', 'V', 'VNO', 'VMC', 'WAB', 'WMT', 'WBA', 'WBD', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WRK', 'WY', 'WHR', 'WMB', 'WTW', 'WYNN', 'XEL', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']
# cacSymbols = ['MC.PA', 'SAN.PA', 'FP.PA', 'OR.PA', 'AI.PA', 'SU.PA', 'KER.PA', 'AIR.PA', 'BN.PA', 'EL.PA', 'DG.PA', 'BNP.PA', 'CS.PA', 'RI.PA', 'RMS.PA', 'VIV.PA', 'DSY.PA', 'ENGI.PA', 'LR.PA',
#              'CAP.PA', 'SGO.PA', 'STM.PA', 'ORA.PA', 'ML.PA', 'TEP.PA', 'WLN.PA', 'VIE.PA', 'GLE.PA', 'ACA.PA', 'UG.PA', 'CA.PA', 'ALO.PA', 'MT.PA', 'HO.PA', 'ATO.PA', 'EN.PA', 'PUB.PA', 'RNO.PA', 'URW.PA']


# Read the symbols from mySymbols-1.txt
with open('mySymbols-x.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# Remove quotes and split by comma to form a list
#mySymbols = [symbol.strip().strip("'\"") for symbol in data.split(',')]

# Now you can use mySymbols in your program
print(mySymbols)  # Example usage

data_unavailable_companies = []
intrinsic_price_meeting_companies = {}
mos_meeting_companies = {}


def upendra_simple_dcf(comp1, url1, url2, url3):
    try:
        #time.sleep(0.4)
        urls = [url1, url2, url3]
        allData = []
        total_cash = 0
        wc_total_cash = 0
        bc_total_cash = 0
        ltgr = 0.02  # Long Term Growth Rate, 10 years to infinity, in decimals - 2% would be 0.02
        wacc = 0.05  # Weighted Average Cost of Capital or WACC in decimals - 2% would be 0.02
        datesBalance = []
        cce = []
        total_liabilities = []
        ocf = []
        discount_rate = 0.08  # 0.04 means 4%. Change it to anything you like.
        # This is expected cash flow growth for years 1 to 5 in a normal scenario.
        cfg_y1_y5 = 0.11
        # This is expected cash flow growth for years 6 to 10 in a normal scenario.
        cfg_y6_y10 = 0.06
        # This is expected cash flow growth for years 1 to 5 in the best case scenario.
        bc_cfg_y1_y5 = 0.15
        # This is expected cash flow growth for years 6 to 10 in the best case scenario.
        bc_cfg_y6_y10 = 0.10
        # This is expected cash flow growth for years 1 to 5 in the worst case scenario.
        wc_cfg_y1_y5 = 0.04
        # This is expected cash flow growth for years 6 to 10  in the worst case scenario.
        wc_cfg_y6_y10 = 0.02
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
        wc_terminal_value = 0.0
        terminal_value = 0.0  # Normal case terminal value
        bc_terminal_value = 0.0
        share_price = 0
        year_high = 0
        year_low = 0
        share_name = ""

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
            total_liabilities.append(allData[0][0]["totalLiabilities"])
        else:
            print("An error occurred: %s") % (data["error"]["description"])

        print(
            "The latest yearly Cash and Cash Equivalent: {cce}.".format(cce=cce[0]))
        print(
            "The latest yearly Total Liabilities: {total_liabilities}.".format(total_liabilities=total_liabilities[0]))
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

        # Terminal value formula from Wall Street Prep
        wc_terminal_value = (
            (wc_discounted_cashflow[-1]*(1+ltgr))/(discount_rate-ltgr))
        # Terminal value formula from Wall Street Prep
        terminal_value = (
            (discounted_cashflow[-1]*(1+ltgr))/(discount_rate-ltgr))
        # Terminal value formula from Wall Street Prep
        bc_terminal_value = (
            (bc_discounted_cashflow[-1]*(1+ltgr))/(discount_rate-ltgr))
        pv_terminal_value = round(((wc_terminal_value/((1+wacc)**10))+(terminal_value/((1+wacc)**10))+(
            bc_terminal_value/((1+wacc)**10)))/3, 2)  # Present value of terminal value is the average of 3 cases

        if allData[2]:
            sharesOut = allData[2][0]["sharesOutstanding"]
            share_price = allData[2][0]["price"]
            share_name = allData[2][0]["name"]
            year_high = allData[2][0]["yearHigh"]
            year_low = allData[2][0]["yearLow"]
            market_cap = allData[2][0]["marketCap"]
            print(
                "The current number of shares outstanding is {0:.2f}.".format(
                    sharesOut
                )
            )
            print("The current price is {0:.2f}.".format(share_price))
        else:
            print("An error occurred: %s") % (data["error"]["description"])

        print("Years:")
        print(year_list)
        print("Discount factor:")
        print(discount_factor)
        tcso = round(total_cash/sharesOut, 2)
        wc_tcso = round(wc_total_cash/sharesOut, 2)
        bc_tcso = round(bc_total_cash/sharesOut, 2)
        ccash = round(float(cce[0])/sharesOut, 2)
        cdebt = round(float(total_liabilities[0])/sharesOut, 2)
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
        wc_intrinsic_price = round((wc_tcso+ccash-cdebt), 2)
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
        intrinsic_price = round((tcso+ccash-cdebt),2)
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
        print(round(bc_intrinsic_price, 2))
        print("-----------------------------------------------------------------------------------------------------------")
        per_share_pv_terminal_value = round((pv_terminal_value/sharesOut), 2)
        pv_of_future_cash_flows_for_10_years = round(
            ((wc_intrinsic_price+intrinsic_price+bc_intrinsic_price)/3), 2)
        print("Average of ten-year cashflow based intrinsic over the three scenarios:")
        print(pv_of_future_cash_flows_for_10_years)
        print("Present value of terminal value per share ({a}):".format(
            a=pv_terminal_value))
        print(per_share_pv_terminal_value)
        print("Final intrinsic value (Sum of 10-year cash flows and terminal value):")
        print(round ((per_share_pv_terminal_value+pv_of_future_cash_flows_for_10_years), 2))
        print(
            "Final intrinsic value with Margin of Safety of {a}:".format(a=mos))
        final_intrinsic_value_with_mos = round(
            (mos * (per_share_pv_terminal_value+pv_of_future_cash_flows_for_10_years)), 2)
        print(final_intrinsic_value_with_mos)

        if pv_of_future_cash_flows_for_10_years > 0:
            dbase.execute("INSERT OR REPLACE INTO dcf_analysis_upen (DATE,TICKER,NAME,CURRENTPRICE,DCFPRICE,DISCOUNTINPERCENT,YEARLOW,YEARHIGH,MARKETCAP) \
            VALUES (?,?,?,?,?,?,?,?,?)", (datetime.today(), comp1, share_name, share_price, max(0, final_intrinsic_value_with_mos), round(((final_intrinsic_value_with_mos-share_price)/final_intrinsic_value_with_mos), 2), year_low, year_high, market_cap))
            dbase.commit()

        else:
            dbase.execute("INSERT OR REPLACE INTO dcf_analysis_upen (DATE,TICKER,NAME,CURRENTPRICE,DCFPRICE,DISCOUNTINPERCENT,YEARLOW,YEARHIGH,MARKETCAP) \
            VALUES (?,?,?,?,?,?,?,?,?)", (datetime.today(), comp1, share_name, share_price, max(0, final_intrinsic_value_with_mos), None, year_low, year_high, market_cap))
            dbase.commit()

        if (share_price < (per_share_pv_terminal_value+pv_of_future_cash_flows_for_10_years)):
            intrinsic_price_meeting_companies[comp1] = (
                round((per_share_pv_terminal_value+pv_of_future_cash_flows_for_10_years), 2))
        if (share_price < (final_intrinsic_value_with_mos)):
            mos_meeting_companies[comp1] = round(
                final_intrinsic_value_with_mos, 2)
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
        letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'][i // 82]
        return os.getenv("MY_VAR_" + letter)
    except IndexError:
        return "demo"


for i in range(0, len(mySymbols)):
    try:
        #my_value_a = get_env_var(i)
        #my_value_a = "demo"
        my_value_a =  os.getenv("MY_VAR_C")
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
print("Companies meeting your margin of safety, shown here with the safest price to pay (after 50% Margin of Safety):")
print(mos_meeting_companies)
print("\n******************************************ENF OF RESULTS***************************************************\n")
for item in data_unavailable_companies:
    dbase.execute("INSERT OR REPLACE INTO data_unavailable_companies (DATE, TICKER) \
            VALUES (?,?)", (datetime.today(), item))
dbase.commit()
