# import libraries
import requests
import re
from bs4 import BeautifulSoup
import logging

f = open("roce_results_new.txt", "a")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

snpSymbols = [
    "MMM",
    "ABT",
    "ABBV",
    "ABMD",
    "ACN",
    "ATVI",
    "ADBE",
    "AMD",
    "AAP",
    "AES",
    "AMG",
    "AFL",
    "A",
    "APD",
    "AKAM",
    "ALK",
    "ALB",
    "ARE",
    "ALXN",
    "ALGN",
    "ALLE",
    "AGN",
    "ADS",
    "LNT",
    "ALL",
    "GOOG",
    "GOOG",
    "MO",
    "AMZN",
    "AMCR",
    "AEE",
    "AAL",
    "AEP",
    "AXP",
    "AIG",
    "AMT",
    "AWK",
    "AMP",
    "ABC",
    "AME",
    "AMGN",
    "APH",
    "ADI",
    "ANSS",
    "ANTM",
    "AON",
    "AOS",
    "APA",
    "AIV",
    "AAPL",
    "AMAT",
    "APTV",
    "ADM",
    "ARNC",
    "ANET",
    "AJG",
    "AIZ",
    "ATO",
    "T",
    "ADSK",
    "ADP",
    "AZO",
    "AVB",
    "AVY",
    "BHGE",
    "BLL",
    "BAC",
    "BK",
    "BAX",
    "BBT",
    "BDX",
    "BRK",
    "BBY",
    "BIIB",
    "BLK",
    "HRB",
    "BA",
    "BKNG",
    "BWA",
    "BXP",
    "BSX",
    "BMY",
    "AVGO",
    "BR",
    "BF",
    "B",
    "CHRW",
    "COG",
    "CDNS",
    "CPB",
    "COF",
    "CPRI",
    "CAH",
    "KMX",
    "CCL",
    "CAT",
    "CBOE",
    "CBRE",
    "CBS",
    "CDW",
    "CE",
    "CELG",
    "CNC",
    "CNP",
    "CTL",
    "CERN",
    "CF",
    "SCHW",
    "CHTR",
    "CVX",
    "CMG",
    "CB",
    "CHD",
    "CI",
    "XEC",
    "CINF",
    "CTAS",
    "CSCO",
    "C",
    "CFG",
    "CTXS",
    "CLX",
    "CME",
    "CMS",
    "KO",
    "CTSH",
    "CL",
    "CMCS",
    "CMA",
    "CAG",
    "CXO",
    "COP",
    "ED",
    "STZ",
    "COO",
    "CPRT",
    "GLW",
    "CTVA",
    "COST",
    "COTY",
    "CCI",
    "CSX",
    "CMI",
    "CVS",
    "DHI",
    "DHR",
    "DRI",
    "DVA",
    "DE",
    "DAL",
    "XRAY",
    "DVN",
    "FANG",
    "DLR",
    "DFS",
    "DISCA",
    "DISCC",
    "DISH",
    "DG",
    "DLTR",
    "D",
    "DOV",
    "DOW",
    "DTE",
    "DUK",
    "DRE",
    "DD",
    "DXC",
    "ETFC",
    "EMN",
    "ETN",
    "EBAY",
    "ECL",
    "EIX",
    "EW",
    "EA",
    "EMR",
    "ETR",
    "EOG",
    "EFX",
    "EQIX",
    "EQR",
    "ESS",
    "EL",
    "EVRG",
    "ES",
    "RE",
    "EXC",
    "EXPE",
    "EXPD",
    "EXR",
    "XOM",
    "FFIV",
    "FB",
    "FAST",
    "FRT",
    "FDX",
    "FIS",
    "FITB",
    "FE",
    "FRC",
    "FISV",
    "FLT",
    "FLIR",
    "FLS",
    "FMC",
    "F",
    "FTNT",
    "FTV",
    "FBHS",
    "FOXA",
    "FOX",
    "BEN",
    "FCX",
    "GPS",
    "GRMN",
    "IT",
    "GD",
    "GE",
    "GIS",
    "GM",
    "GPC",
    "GILD",
    "GL",
    "GPN",
    "GS",
    "GWW",
    "HAL",
    "HBI",
    "HOG",
    "HIG",
    "HAS",
    "HCA",
    "HCP",
    "HP",
    "HSIC",
    "HSY",
    "HES",
    "HPE",
    "HLT",
    "HFC",
    "HOLX",
    "HD",
    "HON",
    "HRL",
    "HST",
    "HPQ",
    "HUM",
    "HBAN",
    "HII",
    "IEX",
    "IDXX",
    "INFO",
    "ITW",
    "ILMN",
    "IR",
    "INTC",
    "ICE",
    "IBM",
    "INCY",
    "IP",
    "IPG",
    "IFF",
    "INTU",
    "ISRG",
    "IVZ",
    "IPGP",
    "IQV",
    "IRM",
    "JKHY",
    "JEC",
    "JBHT",
    "SJM",
    "JNJ",
    "JCI",
    "JPM",
    "JNPR",
    "KSU",
    "K",
    "KEY",
    "KEYS",
    "KMB",
    "KIM",
    "KMI",
    "KLAC",
    "KSS",
    "KHC",
    "KR",
    "LB",
    "LHX",
    "LH",
    "LRCX",
    "LW",
    "LEG",
    "LDOS",
    "LEN",
    "LLY",
    "LNC",
    "LIN",
    "LKQ",
    "LMT",
    "L",
    "LOW",
    "LYB",
    "MTB",
    "MAC",
    "M",
    "MRO",
    "MPC",
    "MKTX",
    "MAR",
    "MMC",
    "MLM",
    "MAS",
    "MA",
    "MKC",
    "MXIM",
    "MCD",
    "MCK",
    "MDT",
    "MRK",
    "MET",
    "MTD",
    "MGM",
    "MCHP",
    "MU",
    "MSFT",
    "MAA",
    "MHK",
    "TAP",
    "MDLZ",
    "MNST",
    "MCO",
    "MS",
    "MOS",
    "MSI",
    "MSCI",
    "MYL",
    "NDAQ",
    "NOV",
    "NKTR",
    "NTAP",
    "NFLX",
    "NWL",
    "NEM",
    "NWSA",
    "NWS",
    "NEE",
    "NLSN",
    "NKE",
    "NI",
    "NBL",
    "JWN",
    "NSC",
    "NTRS",
    "NOC",
    "NCLH",
    "NRG",
    "NUE",
    "NVDA",
    "NVR",
    "ORLY",
    "OXY",
    "OMC",
    "OKE",
    "ORCL",
    "PCAR",
    "PKG",
    "PH",
    "PAYX",
    "PYPL",
    "PNR",
    "PBCT",
    "PEP",
    "PKI",
    "PRGO",
    "PFE",
    "PM",
    "PSX",
    "PNW",
    "PXD",
    "PNC",
    "PPG",
    "PPL",
    "PFG",
    "PG",
    "PGR",
    "PLD",
    "PRU",
    "PEG",
    "PSA",
    "PHM",
    "PVH",
    "QRVO",
    "PWR",
    "QCOM",
    "DGX",
    "RL",
    "RJF",
    "RTN",
    "O",
    "REG",
    "REGN",
    "RF",
    "RSG",
    "RMD",
    "RHI",
    "ROK",
    "ROL",
    "ROP",
    "ROST",
    "RCL",
    "CRM",
    "SBAC",
    "SLB",
    "STX",
    "SEE",
    "SRE",
    "SHW",
    "SPG",
    "SWKS",
    "SLG",
    "SNA",
    "SO",
    "LUV",
    "SPGI",
    "SWK",
    "SBUX",
    "STT",
    "SYK",
    "STI",
    "SIVB",
    "SYMC",
    "SYF",
    "SNPS",
    "SYY",
    "TMUS",
    "TROW",
    "TTWO",
    "TPR",
    "TGT",
    "TEL",
    "FTI",
    "TFX",
    "TXN",
    "TXT",
    "TMO",
    "TIF",
    "TWTR",
    "TJX",
    "TSCO",
    "TDG",
    "TRV",
    "TRIP",
    "TSN",
    "UDR",
    "ULTA",
    "USB",
    "UAA",
    "UA",
    "UNP",
    "UAL",
    "UNH",
    "UPS",
    "URI",
    "UTX",
    "UHS",
    "UNM",
    "VFC",
    "VLO",
    "VAR",
    "VTR",
    "VRSN",
    "VRSK",
    "VZ",
    "VRTX",
    "VIAB",
    "V",
    "VNO",
    "VMC",
    "WAB",
    "WMT",
    "WBA",
    "DIS",
    "WM",
    "WAT",
    "WEC",
    "WCG",
    "WFC",
    "WELL",
    "WDC",
    "WU",
    "WRK",
    "WY",
    "WHR",
    "WMB",
    "WLTW",
    "WYNN",
    "XEL",
    "XRX",
    "XLNX",
    "XYL",
    "YUM",
    "ZBH",
    "ZION",
    "ZTS",
]
dowSymbols = ["AAPL", "MSFT", "NKE"]
for i in range(0, len(dowSymbols)):  # len(dowSymbols
    try:
        # set the URL you want to webscrape from
        ticker = dowSymbols[i]
        # url = 'http://www.locationary.com/home/index2.jsp'
        url = "https://finance.yahoo.com/quote/{}/balance-sheet?p={}".format(
            ticker, ticker
        )
        url2 = "https://finance.yahoo.com/quote/{}/financials?p={}".format(
            ticker, ticker
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }

        #################
        # first page
        #################

        print("\n" + ticker + "\n")
        total_assets = {}
        total_current_liabilities = {}
        operating_income_or_loss = {}
        page1_table_keys = []
        page2_table_keys = []

        # connect to the first page URL
        response = requests.get(url, headers=headers)

        # parse HTML and save to BeautifulSoup object¶
        soup = BeautifulSoup(response.text, "html.parser")
        # the nearest id to get the result
        sheet = soup.find(id="Col1-1-Financials-Proxy")
        sheet_section_divs = sheet.section.find_all("div", recursive=False)
        # last child
        sheet_data_div = sheet_section_divs[-1]
        div_ele_table = (
            sheet_data_div.find("div").find("div").find_all("div", recursive=False)
        )
        # table header
        div_ele_header = div_ele_table[0].find("div").find_all("div", recursive=False)
        # first element is label, the remaining element containing data, so use range(1, len())
        for i in range(1, len(div_ele_header)):
            page1_table_keys.append(div_ele_header[i].find("span").text)
        # table body
        div_ele = div_ele_table[-1]
        div_eles = div_ele.find_all("div", recursive=False)
        tgt_div_ele1 = div_eles[0].find_all("div", recursive=False)[-1]
        tgt_div_ele1_row = tgt_div_ele1.find_all("div", recursive=False)[-1]
        tgt_div_ele1_row_eles = tgt_div_ele1_row.find("div").find_all(
            "div", recursive=False
        )
        # first element is label, the remaining element containing data, so use range(1, len())
        for i in range(1, len(tgt_div_ele1_row_eles)):
            total_assets[page1_table_keys[i - 1]] = (
                tgt_div_ele1_row_eles[i].find("span").text
            )
        tgt_div_ele2 = div_eles[1].find_all("div", recursive=False)[-1]
        tgt_div_ele2 = tgt_div_ele2.find("div").find_all("div", recursive=False)[-1]
        # tgt_div_ele2 = tgt_div_ele2.find('div').find_all('div', recursive=False)[-1]
        tgt_div_ele2_row = tgt_div_ele2.find_all("div", recursive=False)[-1]
        tgt_div_ele2_row_eles = tgt_div_ele2_row.find("div").find_all(
            "div", recursive=False
        )
        # first element is label, the remaining element containing data, so use range(1, len())
        for i in range(1, len(tgt_div_ele2_row_eles)):
            total_current_liabilities[page1_table_keys[i - 1]] = (
                tgt_div_ele2_row_eles[i].find("span").text
            )

        print("Total Assets", total_assets)
        print("Total Current Liabilities", total_current_liabilities)
        #################
        # second page, same logic as the first page
        #################
        # print('*' * 10, ' SECOND PAGE RESULT ', '*' * 10)
        # Connect to the second page URL
        response = requests.get(url2, headers=headers)
        # Parse HTML and save to BeautifulSoup object¶
        soup = BeautifulSoup(response.text, "html.parser")
        # the nearest id to get the result
        sheet = soup.find(id="Col1-1-Financials-Proxy")
        sheet_section_divs = sheet.section.find_all("div", recursive=False)
        # last child
        sheet_data_div = sheet_section_divs[-1]
        div_ele_table = (
            sheet_data_div.find("div").find("div").find_all("div", recursive=False)
        )
        # table header
        div_ele_header = div_ele_table[0].find("div").find_all("div", recursive=False)
        # first element is label, the remaining element containing data, so use range(1, len())
        for i in range(1, len(div_ele_header)):
            page2_table_keys.append(div_ele_header[i].find("span").text)
        # table body
        div_ele = div_ele_table[-1]
        div_eles = div_ele.find_all("div", recursive=False)
        tgt_div_ele_row = div_eles[4]
        tgt_div_ele_row_eles = tgt_div_ele_row.find("div").find_all(
            "div", recursive=False
        )
        for i in range(1, len(tgt_div_ele_row_eles)):
            operating_income_or_loss[page2_table_keys[i - 1]] = (
                tgt_div_ele_row_eles[i].find("span").text
            )
        print("Operating Income or Loss", operating_income_or_loss)
        dates = []
        ta = []
        tca = []
        oil = []
        for key, val in total_assets.items():
            dates.append(key)
            ta.append(val)
        for key, val in total_current_liabilities.items():
            tca.append(val)
        for key, val in operating_income_or_loss.items():
            oil.append(val)
        for i in range(0, len(ta)):
            # print (float(re.sub("[^\d\.\-]", "", oil[i])))
            roce = (
                100
                * float(re.sub("[^\d\.\-]", "", oil[i + 1]))
                / (
                    float((re.sub("[^\d\.\-]", "", ta[i])))
                    - float((re.sub("[^\d\.\-]", "", tca[i])))
                )
            )
            if roce > 0:
                print(f"Date: {dates[i]} and ROCE on that date was {roce:.2f} %" + "\n")
            else:
                print("Negative ROCE" + "\n")
        print(
            "*****************************************************************************"
            + "\n"
        )
        # output Year: 09292016, Total assets: 321,686,000, Total current liabilities: 79,006,000
    except IndexError:
        print("Data not available (Index)" + "\n")
        print(
            "*****************************************************************************"
            + "\n"
        )
        pass
    except AttributeError as err:
        print("Data not available (Attribute)" + "\n")
        print(
            "*****************************************************************************"
            + "\n"
        )
        logger.warning("The data was not available: {}".format(err) + "\n")
        pass
    continue

f.close()
print("Done")
