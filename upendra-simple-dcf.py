#Author: Upendra Rajan
#This makes 3 API calls per company listed in mySymbols

from os import environ
from datetime import datetime
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
import sqlite3

dbase = sqlite3.connect('stock-dcf-data.db') # Open a database File
cursor = dbase.cursor()
print ('Database opened')
print ('Cursor created')

dbase.execute(''' CREATE TABLE IF NOT EXISTS dcf_analysis_upen(
    DATE TIMESTAMP NOT NULL,
    NAME TEXT NOT NULL UNIQUE,
    CURRENTPRICE INT NULL, 
    DCFPRICE INT NULL,    
    DISCOUNT INT NULL) ''')

print ('Table created')

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
init(convert=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Upendra: Enter your list of symbols here
mySymbols = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'BRK.B', 'NVDA', 'FB', 'V', 'UNH', 'JPM', 'JNJ', 'BAC', 'PG', 'WMT', 'HD', 'MA', 'XOM', 'PFE', 'DIS', 'CVX', 'KO', 'ABBV', 'AVGO', 'ADBE', 'WFC', 'PEP', 'CSCO', 'COST', 'ACN', 'LLY', 'TMO', 'ABT', 'NKE', 'CMCSA', 'VZ', 'ORCL', 'CRM', 'DHR', 'QCOM', 'INTC', 'MS', 'UPS', 'MCD', 'MRK', 'NFLX', 'SCHW', 'T', 'TXN', 'PM', 'TMUS', 'AMD', 'INTU', 'LOW', 'UNP', 'AXP', 'NEE', 'BMY', 'RTX', 'PYPL', 'MDT', 'CVS', 'C', 'HON', 'AMGN', 'AMAT', 'BA', 'GS', 'BLK', 'NOW', 'COP', 'IBM', 'DE', 'EL', 'PLD', 'AMT', 'ANTM', 'SBUX', 'CHTR', 'CAT', 'GE', 'BKNG', 'LMT', 'ISRG', 'TGT', 'MU', 'SPGI', 'SYK', 'ZTS', 'MDLZ', 'MMM', 'MO', 'BX', 'CB', 'CME', 'PNC', 'ADP', 'USB', 'SNOW', 'TFC', 'TJX', 'LRCX', 'TEAM', 'DUK', 'GILD', 'MMC', 'BDX', 'CCI', 'CSX', 'CI', 'HCA', 'SHW', 'UBER', 'GM', 'ICE', 'F', 'SO', 'ITW', 'EW', 'FIS', 'NSC', 'CL', 'COF', 'FISV', 'MRNA', 'EOG', 'MRVL', 'REGN', 'D', 'PSA', 'AON', 'FDX', 'EQIX', 'FCX', 'MCO', 'BSX', 'ATVI', 'PGR', 'ETN', 'VRTX', 'WM', 'KLAC', 'GD', 'NOC', 'MET', 'EMR', 'RIVN', 'APD', 'ILMN', 'VMW', 'MAR', 'HUM', 'XLNX', 'NXPI', 'ADSK', 'SLB', 'KDP', 'ECL', 'PXD', 'FTNT', 'PANW', 'BK', 'SCCO', 'AIG', 'NEM', 'CNC', 'SNPS', 'MPC', 'IQV', 'JCI', 'INFO', 'CTSH', 'SQ', 'ROP', 'APH', 'DG', 'SPG', 'WDAY', 'MSCI', 'PRU', 'MNST', 'DOW', 'CMG', 'IDXX', 'STZ', 'AEP', 'BAX', 'PAYX', 'KMB', 'ADI', 'DELL', 'SRE', 'AFL', 'MCHP', 'DXCM', 'A', 'LHX', 'ADM', 'WBA', 'ORLY', 'ALGN', 'CDNS', 'ZM', 'KHC', 'HLT', 'DD', 'TRV', 'GPN', 'HSY', 'LULU', 'MCK', 'SYY', 'DLR', 'EXC', 'CARR', 'HPQ', 'AZO', 'GIS', 'CTAS', 'RSG', 'MSI', 'KKR', 'PH', 'DDOG', 'EBAY', 'KMI', 'ZS', 'PSX', 'CRWD', 'EA', 'TT', 'APTV', 'OXY', 'CTVA', 'SIVB', 'YUM', 'XEL', 'PPG', 'STT', 'WMB', 'GLW', 'DFS', 'ODFL', 'VLO', 'TDG', 'RMD', 'TSN', 'SBAC', 'ALL', 'MTD', 'LVS', 'WELL', 'OTIS', 'AMP', 'CBRE', 'DVN', 'NET', 'TTD', 'AVB', 'TROW', 'ROST', 'DASH', 'NUE', 'LYB', 'PEG', 'TWLO', 'EQR', 'IFF', 'FITB', 'BIIB', 'ROK', 'AJG', 'KR', 'MTCH', 'U', 'VEEV', 'PCAR', 'LSXMA', 'LSXMK', 'FWONK', 'FWONA', 'CMI', 'VRSK', 'WY', 'DLTR', 'SPOT', 'BF.B', 'BF.A', 'AME', 'KEYS', 'DHI', 'FAST', 'CPRT', 'FRC', 'ARE', 'ED', 'GFS', 'BLL', 'PCG', 'WST', 'TWTR', 'NDAQ', 'ES', 'ABC', 'ANSS', 'WEC', 'MDB', 'LNG', 'HAL', 'EFX', 'OKTA', 'HES', 'ON', 'EXPE', 'BKR', 'WTW', 'OKE', 'AWK', 'LEN.B', 'LEN', 'DAL', 'CSGP', 'LUV', 'O', 'ALB', 'SWK', 'EXR', 'MKC', 'EPAM', 'CERN', 'ZBRA', 'LBRDA', 'LBRDK', 'LH', 'LYV', 'NTRS', 'SIRI', 'HRL', 'PLTR', 'SGEN', 'CDW', 'BILL', 'CCL', 'INVH', 'TSCO', 'DOCU', 'GWW', 'ZBH', 'VMC', 'VFC', 'MAA', 'IT', 'KEY', 'HIG', 'GRMN', 'HUBS', 'BBY', 'CHD', 'SYF', 'VRSN', 'URI', 'DOV', 'FOX', 'FOXA', 'RJF', 'MLM', 'PKI', 'FTV', 'STE', 'RF', 'SWKS', 'CFG', 'MTB', 'EIX', 'FANG', 'DTE', 'HBAN', 'VIACA', 'VIAC', 'FE', 'AVTR', 'IR', 'MGM', 'PPL', 'SUI', 'AEE', 'RCL', 'HPE', 'DRE', 'ETR', 'HZNP', 'PAYC', 'ENPH', 'COO', 'ESS', 'K', 'SSNC', 'ROKU', 'PFG', 'VTR', 'SBNY', 'FLT', 'WAT', 'JBHT', 'NTAP', 'ULTA', 'CLR', 'YUMC', 'TDY', 'TRU', 'TYL', 'TTWO', 'CINF', 'TER', 'BRO', 'MPWR', 'SPLK', 'OMC', 'BIO', 'EXPD', 'GPC', 'AKAM', 'DRI', 'CMS', 'POOL', 'ACGL', 'NVR', 'VTRS', 'ETSY', 'GNRC', 'CZR', 'CTLT', 'HOLX', 'CTRA', 'IP', 'KMX', 'BXP', 'VICI', 'ALNY', 'ENTG', 'CG', 'MOH', 'TRMB', 'NLOK', 'PEAK', 'AMCR', 'CNP', 'AGR', 'NUAN', 'PODD', 'UDR', 'BR', 'CLX', 'CRL', 'CE', 'ALLY', 'WAB', 'RPRX', 'MKL', 'XYL', 'CPT', 'WDC', 'BMRN', 'HEI', 'HEI.A', 'MOS', 'DISH', 'CAG', 'DGX', 'MRO', 'TECH', 'LKQ', 'PINS', 'J', 'EMN', 'WRB', 'DPZ', 'UAL', 'FDS', 'TXT', 'BEN', 'BBWI', 'CF', 'AVY', 'UI', 'TFX', 'BURL', 'IPG', 'CEG', 'ROL', 'AES', 'LPLA', 'L', 'KIM', 'PWR', 'IEX', 'INCY', 'DISCK', 'DISCA', 'EVRG', 'CAH', 'FMC', 'QRVO', 'LNT', 'ATO', 'CCK', 'HWM', 'SJM', 'EQH', 'LYFT', 'FNF', 'MAS', 'AAP', 'ELS', 'ABMD', 'PKG', 'TRGP', 'EXAS', 'RNG', 'PTC', 'MKTX', 'WPC', 'BG', 'NWS', 'NWSA', 'RHI', 'FICO', 'NDSN', 'OLPX', 'BLDR', 'ARES', 'ACI', 'DT', 'AA', 'IRM', 'LNC', 'HAS', 'PLUG', 'WLK', 'JLL', 'AMH', 'HST', 'LUMN', 'CPB', 'MPW', 'CMA', 'CNA', 'JKHY', 'CBOE', 'MASI', 'PHM', 'CTXS', 'EWBC', 'MORN', 'FBHS', 'GGG', 'ZEN', 'WHR', 'FFIV', 'GDDY', 'STLD', 'WRK', 'LDOS', 'REG', 'Z', 'ZG', 'WOLF', 'CDAY', 'ELAN', 'TDOC', 'AAL', 'APA', 'UHAL', 'PCTY', 'AOS', 'CSL', 'WSM', 'FND', 'XRAY', 'CGNX', 'W', 'WTRG', 'PTON', 'CONE', 'UHS', 'CHRW', 'SNA', 'DVA', 'QGEN', 'RE', 'CUBE', 'JNPR', 'ZION', 'NI', 'LSI', 'IAC', 'RPM', 'MTN', 'AFG', 'ALLE', 'REXR', 'TPR', 'RRX', 'MIDD', 'NLY', 'BKI', 'BSY', 'BRKR', 'RGEN', 'IVZ', 'SCI', 'VST', 'WYNN', 'CNXC', 'TREX', 'ACM', 'GLPI', 'WSO', 'GL', 'BWA', 'DAR', 'GLOB', 'MHK', 'TAP', 'HSIC', 'CLVT', 'WAL', 'DOX', 'TTC', 'HUBB', 'RS', 'CLF', 'CPRI', 'PNR', 'SNX', 'LEA', 'ZNGA', 'COUP', 'CIEN', 'AXON', 'LII', 'BAH', 'NRG', 'LAMR', 'GXO', 'FHN', 'FIVE', 'ANET', 'AGCO', 'AVLR', 'ARMK', 'NWL', 'LW', 'SEE', 'AZPN', 'LAD', 'JEF', 'FRT', 'DKNG', 'SYNH', 'AIZ', 'GME', 'KNX', 'CABO', 'DXC', 'Y', 'OC', 'G', 'RL', 'CFR', 'ST', 'UTHR', 'UPST', 'TW', 'RH', 'JBL', 'FIVN', 'PBCT', 'PCOR', 'ARW', 'JAZZ', 'TXG', 'ESTC', 'PEN', 'OGN', 'KSS', 'PENN', 'WMS', 'MKSI', 'VRT', 'ERIE', 'BERY', 'USFD', 'DNB', 'OLN', 'CHDN', 'IPGP', 'UA', 'UAA', 'SEIC', 'SITE', 'NVCR', 'MANH', 'DECK', 'SF', 'AIRC', 'UGI', 'WH', 'STOR', 'CBSH', 'FAF', 'PEGA', 'BFAM', 'CHH', 'TPL', 'GWRE', 'SMAR', 'ITT', 'ORI', 'EQT', 'HUN', 'AGL', 'PAG', 'CACC', 'TPX', 'PSTG', 'PNW', 'XPO', 'BLD', 'VNO', 'MAT', 'FR', 'VOYA', 'FSLR', 'COTY', 'KRC', 'DBX', 'PLNT', 'BYD', 'TNDM', 'RGA', 'OSK', 'NBIX', 'LECO', 'ATR', 'SNV', 'GH', 'PNFP', 'BRX', 'NNN', 'CVNA', 'COLD', 'EEFT', 'CHE', 'AGNC', 'OGE', 'WU', 'SMG', 'HII', 'WEX', 'BPOP', 'GNTX', 'BC', 'WWD', 'DKS', 'NXST', 'ALK', 'BOKF', 'TWKS', 'PII', 'IBKR', 'VAC', 'ACC', 'PLTK', 'PVH', 'STWD', 'OLED', 'GMED', 'OMF', 'AN', 'NVST', 'NYT', 'FCNCA', 'LITE', 'PPC', 'PB', 'PLAN', 'ATUS', 'NTRA', 'NVAX', 'WIX', 'HTA', 'CASY', 'TOL', 'RGLD', 'AZTA', 'SRPT', 'RNR', 'AXTA', 'MTZ', 'OHI', 'INFA', 'DCI', 'NLSN', 'AYI', 'HOG', 'POST', 'COLM', 'LFUS', 'COHR', 'GPS', 'X', 'OPEN', 'SKX', 'SHC', 'NOV', 'EHC', 'CHNG', 'LPX', 'JHG', 'IAA', 'CR', 'EXEL', 'PRI', 'VVV', 'BEPC', 'LSTR', 'CFX', 'MAN', 'NVT', 'NTNX', 'AMG', 'CACI', 'YETI', 'ADT', 'ESI', 'FLO', 'REYN', 'MRTX', 'OZK', 'PACW', 'HFC', 'MDU', 'CC', 'WTFC', 'GPK', 'INGR', 'NCR', 'SRC', 'UNM', 'SLM', 'CUZ', 'EXP', 'AMBP', 'HBI', 'QS', 'ALGM', 'SON', 'IART', 'WBS', 'ASH', 'DEI', 'TDC', 'NFG', 'THO', 'SRCL', 'VSCO', 'RYN', 'MSA', 'IDA', 'NYCB', 'CW', 'NATI', 'HHC', 'CLH', 'RUN', 'SPR', 'TNL', 'TMX', 'FCN', 'EVR', 'LEG', 'MCW', 'MTG', 'DTM', 'AZEK', 'NEWR', 'WEN', 'DLB', 'PRGO', 'TKR', 'CDK', 'NCLH', 'RARE', 'THG', 'NRZ', 'JBLU', 'DRVN', 'SLG', 'UNVR', 'H', 'CRUS', 'PYCR', 'AL', 'IONS', 'SLGN', 'ACHC', 'TFSL', 'AXS', 'CHGG', 'SAIC', 'NFE', 'BHF', 'MCFE', 'ICUI', 'LAZ', 'AWI', 'VMI', 'VNT', 'HE', 'HLF', 'PK', 'DV', 'SEB', 'UMPQ', 'AMED', 'CHPT', 'MNDT', 'HXL', 'GTES', 'SAM', 'PINC', 'FL', 'FLS', 'WOOF', 'HAYW', 'CERT', 'HIW', 'FNB', 'NCNO', 'JAMF', 'MSP', 'FRPT', 'BWXT', 'ALSN', 'HRB', 'QDEL', 'AVT', 'R', 'OSH', 'CRI', 'AGO', 'VIRT', 'MRVI', 'SIX', 'CNM', 'SWCH', 'XRX', 'KEX', 'MSM', 'LESL', 'JWN', 'FHB', 'SPB', 'KD', 'TRIP', 'HPP', 'ADS', 'STNE', 'JBGS', 'CVAC', 'BOH', 'MSGS', 'FSLY', 'KMPR', 'DSEY', 'EPR', 'HAIN', 'LOPE', 'LZ', 'AYX', 'NEU', 'DCT', 'FIGS', 'WTM', 'SABR', 'VSAT', 'FTDR', 'TSP', 'MRCY', 'OLLI', 'MCY', 'QRTEA', 'FOUR', 'CPA', 'IOVA', 'AI', 'SAGE', 'GO', 'SNDR', 'ADPT', 'WWE', 'SPCE', 'SGFY', 'DH', 'EVBG', 'SWI', 'VMEO', 'NABL', 'NKTR', 'COMM', 'LMND', 'BYND', 'RKT', 'SKLZ', 'SHLS', 'SLVM', 'VRM', 'ONL', 'FLNC', 'LYLT', 'PSFE', 'UWMC', 'GOCO']
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
        discount_rate = 0.05 # 0.04 means 4%. Change it to anything you like.
        cfg_y1_y5 = 0.15 # This is expected cash flow growth for years 1 to 5 in a normal scenario.
        cfg_y6_y10 = 0.10 # This is expected cash flow growth for years 6 to 10 in a normal scenario.
        bc_cfg_y1_y5 = 0.20 # This is expected cash flow growth for years 1 to 5 in the best case scenario. 
        bc_cfg_y6_y10 = 0.16     # This is expected cash flow growth for years 6 to 10 in the best case scenario.
        wc_cfg_y1_y5 = 0.05 # This is expected cash flow growth for years 1 to 5 in the worst case scenario. 
        wc_cfg_y6_y10 = 0.03 # This is expected cash flow growth for years 6 to 10  in the worst case scenario.
        generated_cash = [] # This will contain ten years' generated cash flow.
        bc_generated_cash = []
        wc_generated_cash = []
        discount_factor = [] # This will contain ten years' discount factor.
        dicsounted_cashFlow = [] # This will contain ten years' discounted cash each year.
        bc_dicsounted_cashFlow = []
        wc_dicsounted_cashFlow = []
        mos = 0.5 # Enter your margin of safety here. 0.5 indicates 50%.
        year_list = []
        intrinsic_price = 0.0
        share_price = 0
        for url in urls:
            request = urlopen(url)
            response = request.read()
            data = json.loads(response)
            allData.append(data)
        #print (allData)
        request.close()
        # 1. Get operating cash flow, shares outstanding, current cash and equivalents and total current liabilities
        for key, value in allData[0].items():
            if key == "financials":
                for lst_item in value:
                    for key, value in lst_item.items():
                        #print('key: {} value: {}'.format(key, value))
                        if key == "date":
                            datesBalance.append(value)
                        elif key == "Cash and cash equivalents":
                            cce.append(value)
                        elif key == "Total current liabilities":
                            tcl.append(value)
        print ("The latest yearly Cash and Cash Equivalent: {cce}.".format(cce = cce[0]))
        print ("The latest yearly Total Current Liabilities: {tcl}.".format(tcl = tcl[0]))
        if allData[1]:
            #print (allData[2])
            for i in range(0, len(allData[1])):
                if i >= 10:
                    break
                ocf.append(allData[1][i]["operatingCashFlow"])
        else:
            print("Cash Flow Data not available")
        print ("The latest yearly operating cash flow: {ocf}.".format(ocf = ocf[0]))
        generated_cash.append(round(float(ocf[0])))
        bc_generated_cash.append(round(float(ocf[0])))
        wc_generated_cash.append(round(float(ocf[0])))
        for i in range (1, 6):
            generated_cash.append(round(generated_cash[i-1] * (1+cfg_y1_y5)))
            bc_generated_cash.append(round(bc_generated_cash[i-1] * (1+bc_cfg_y1_y5)))
            wc_generated_cash.append(round(wc_generated_cash[i-1] * (1+wc_cfg_y1_y5)))
        for i in range (6, 11):
            generated_cash.append(round(generated_cash[i-1] * (1+cfg_y6_y10)))
            bc_generated_cash.append(round(bc_generated_cash[i-1] * (1+bc_cfg_y6_y10)))
            wc_generated_cash.append(round(wc_generated_cash[i-1] * (1+wc_cfg_y6_y10)))
        year_list.append(round(float(datesBalance[0][0:4])))
        discount_factor.append(1.0)
        dicsounted_cashFlow.append(generated_cash[0])
        bc_dicsounted_cashFlow.append(generated_cash[0])
        wc_dicsounted_cashFlow.append(generated_cash[0])
        for i in range (1,11):
            year_list.append(year_list[i-1]+1)
            discount_factor.append(round(float(1/((1+discount_rate)**(year_list[i]-year_list[0]))), 2))
            dicsounted_cashFlow.append(generated_cash[i]*discount_factor[i])
            bc_dicsounted_cashFlow.append(bc_generated_cash[i]*discount_factor[i])
            wc_dicsounted_cashFlow.append(wc_generated_cash[i]*discount_factor[i])

        for ele in range(1, len(dicsounted_cashFlow)):
            total_cash = total_cash + dicsounted_cashFlow[ele]
        for ele in range(1, len(wc_dicsounted_cashFlow)):
            wc_total_cash = wc_total_cash + wc_dicsounted_cashFlow[ele]
        for ele in range(1, len(bc_dicsounted_cashFlow)):
            bc_total_cash = bc_total_cash + bc_dicsounted_cashFlow[ele]

        if allData[2]:
            sharesOut = allData[2][0]["sharesOutstanding"]
            share_price = allData[2][0]["price"]
            print(
                "The current number of shares outstanding is {0:.2f}.".format(
                    sharesOut
                )
            )
            print("The current price is {0:.2f}.".format(share_price))
        else:
            print("An error occurred under items 3, 4 and 5: %s") % (data["error"]["description"])

        print ("Years:")
        print(year_list)
        print ("Discount factor:")
        print (discount_factor)
        tcso = round (total_cash/sharesOut, 2)
        wc_tcso = round (wc_total_cash/sharesOut, 2)
        bc_tcso = round (bc_total_cash/sharesOut, 2)
        ccash = round (float(cce[0])/sharesOut, 2)
        cdebt = round (float(tcl[0])/sharesOut, 2)
        print ("\nWORST CASE:\n")
        print ("Worst case: Generated cash over the next ten years")
        print (wc_generated_cash)
        print ("Worst case: Discounted cash flow")
        print (wc_dicsounted_cashFlow)
        print ("Worst Case: Cash flow over the next 10 years:")
        print (round(wc_total_cash, 2))
        print ("Worst case - Total cash over the next 10 years per outstanding share is: " + str(wc_tcso))
        print ("Adding current cash per share {a} and subtracting current debt per share {b}.".format(a = ccash, b = cdebt))
        wc_intrinsic_price = wc_tcso+ccash-cdebt
        print ("Worst case - Intrinsic value per share:")
        print (wc_intrinsic_price)
        print ("\nNORMAL CASE:\n")
        print ("Normal case: Generated cash over the next ten years")
        print (generated_cash)    
        print ("Normal case: Discounted cash flow")
        print (dicsounted_cashFlow)
        print ("Normal Case: Cash flow over the next 10 years:")
        print (round(total_cash, 2))  
        print ("Normal case - Total cash over the next 10 years per outstanding share is: " + str(tcso))
        print ("Adding current cash per share {a} and subtracting current debt per share {b}.".format(a = ccash, b = cdebt))
        intrinsic_price = tcso+ccash-cdebt
        print ("Normal case - Intrinsic value per share:")
        print (intrinsic_price)
        print ("\nBEST CASE:\n")
        print ("Best case: Generated cash over the next ten years")
        print (bc_generated_cash)
        print ("Best case: Discounted cash flow")
        print (bc_dicsounted_cashFlow)   
        print ("Best Case: Cash flow over the next 10 years:")
        print (round(bc_total_cash, 2))
        print ("Best case - Total cash over the next 10 years per outstanding share is: " + str(bc_tcso))
        print ("Adding current cash per share {a} and subtracting current debt per share {b}.".format(a = ccash, b = cdebt))
        bc_intrinsic_price = bc_tcso+ccash-cdebt
        print ("Best case - Intrinsic value per share:")
        print (bc_intrinsic_price)
        print ("-----------------------------------------------------------------------------------------------------------")
        avg_intrinsic_price = round(((wc_intrinsic_price+intrinsic_price+bc_intrinsic_price)/3), 2)
        print ("Average intrinsic value over the three scenarios:")
        print (avg_intrinsic_price)

        if avg_intrinsic_price > 0:
            dbase.execute("INSERT OR REPLACE INTO dcf_analysis_upen (DATE,NAME,CURRENTPRICE,DCFPRICE,DISCOUNT) \
            VALUES (?,?,?,?,?)", (datetime.today(),comp1,share_price,max(0,avg_intrinsic_price),round(((avg_intrinsic_price-share_price)/avg_intrinsic_price),2)));
            dbase.commit()

        else:
            dbase.execute("INSERT OR REPLACE INTO dcf_analysis_upen (DATE,NAME,CURRENTPRICE,DCFPRICE,DISCOUNT) \
            VALUES (?,?,?,?,?)", (datetime.today(),comp1,share_price,max(0,avg_intrinsic_price),None));
            dbase.commit()

        print ("Applying margin of safety of {a}".format(a = mos))
        print (round(avg_intrinsic_price*mos, 2))
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
        letter = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'B'][i // 82]
        return os.getenv("MY_VAR_" + letter)
    except IndexError:
        return "demo"


for i in range(0, len(mySymbols)):
    try:
        my_value_a = get_env_var(i)
        #my_value_a = "demo"
        #my_value_a =  os.getenv("MY_VAR_K")
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

        upendra_simple_dcf( mySymbols[i], url_bs_y, url_cfs_y, url_quote)

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        traceback.print_exc()
    continue
# print output here
print("\n*************************************************RESULTS***************************************************\n")
print ("Data unavailable companies:")
print(data_unavailable_companies)
print ("Companies whose intrinsic value is less than the current price, shown here with avg. intrinsic value of 3 scenarios:")
print (intrinsic_price_meeting_companies)
print ("Companies meeting your margin of safety, shown here with the safest price to pay:")
print (mos_meeting_companies)
print("\n******************************************ENF OF RESULTS***************************************************\n")