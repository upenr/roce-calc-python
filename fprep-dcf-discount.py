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
dowSymbols = [
    "SONM",
    "NVEC",
    "REGI",
    "LQDT",
    "ABG",
    "NG",
    "PATK",
    "CYTK",
    "TUSK",
    "EOLS",
    "CODA",
    "VALU",
    "CRUS",
    "OSTK",
    "PSMT",
    "ASRT",
    "NCMI",
    "FCFS",
    "HCKT",
    "CROX",
    "FLMN",
    "KFRC",
    "PLCE",
    "XPER",
    "SMP",
    "TPCO",
    "ACTG",
    "LLNW",
    "STMP",
    "LTHM",
    "TCX",
    "AKRX",
    "MGPI",
    "ROAD",
    "TRWH",
    "KRO",
    "CCF",
    "CNXN",
    "MTSC",
    "OXM",
    "DBI",
    "FIX",
    "ULH",
    "IMXI",
    "LGND",
    "TXRH",
    "BLKB",
    "LCI",
    "REV",
    "MJCO",
    "AEIS",
    "BCPC",
    "FWRD",
    "MXL",
    "RILY",
    "JJSF",
    "HTLD",
    "TELL",
    "DMRC",
    "GEOS",
    "LORL",
    "RLGT",
    "CMP",
    "PRIM",
    "GES",
    "FN",
    "ANIK",
    "AMN",
    "EBIX",
    "NMRK",
    "MLAB",
    "CLMS",
    "UFPT",
    "MSTR",
    "LAD",
    "AMWD",
    "JBT",
    "OII",
    "LEE",
    "CAKE",
    "HA",
    "PUMP",
    "UIS",
    "WGO",
    "TISI",
    "ENSG",
    "HQY",
    "CARG",
    "CSGS",
    "MPAA",
    "TESS",
    "VSEC",
    "WNC",
    "JBSS",
    "THRM",
    "LPX",
    "ZUMZ",
    "SIG",
    "GNRC",
    "OPBK",
    "LXU",
    "NP",
    "CVI",
    "SCL",
    "LHCG",
    "NEOG",
    "MLR",
    "LZB",
    "GNC",
    "TPB",
    "IMMR",
    "GRC",
    "CHS",
    "IOSP",
    "CLF",
    "FLXS",
    "SM",
    "LEGH",
    "KNL",
    "GPX",
    "WTI",
    "ONTO",
    "TTEC",
    "NTCT",
    "ROLL",
    "AMOT",
    "ENDP",
    "PDCO",
    "PGTI",
    "VLGEA",
    "LNN",
    "TEN",
    "ALG",
    "UNF",
    "DK",
    "FG",
    "KOP",
    "USLM",
    "CCMP",
    "CTB",
    "ECOL",
    "MEI",
    "UNFI",
    "MYRG",
    "SND",
    "CPE",
    "HUBG",
    "ATRC",
    "TVTY",
    "GPI",
    "FF",
    "ENS",
    "GCO",
    "AZZ",
    "EVC",
    "MBIN",
    "TRS",
    "CHRA",
    "ETH",
    "HNI",
    "MTRX",
    "SXI",
    "KAI",
    "EPM",
    "SSD",
    "OMI",
    "LPSN",
    "KBAL",
    "SBT",
    "TTEK",
    "BRID",
    "JOUT",
    "SB",
    "POWI",
]
threshold = 4  # Enter DCF discount you want
final_companies = []
discount_dict = {}

for i in range(0, len(dowSymbols)):  # len(dowSymbols)
    try:
        my_value_b = os.getenv("MY_VAR_B")
        url = (
            "https://financialmodelingprep.com/api/v3/company/discounted-cash-flow/"
            + dowSymbols[i]
            + "?apikey="
            + my_value_b
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        # print (url)
        request = urlopen(url)
        response = request.read()
        data = json.loads(response)
        # print (data)
        if data:
            symbol = data["symbol"]
            date = data["date"]
            price = data["Stock Price"]
            dcf = data["dcf"]
            print("This is for stock " + symbol + " on " + date)
            print("The price is {0:.2f}".format(price))
            print("The dcf is {0:.2f}".format(float(dcf)))
            discount = ((dcf - price) / dcf) * 100
            print("The discount is {0:.2f}%".format(discount))
            if discount >= threshold:
                discount_dict[dowSymbols[i]] = []
                # final_companies.append(symbol)
                discount_dict.setdefault(symbol, []).append(round(discount, 2))
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
    except KeyError as e:
        print("API Key probably exceeded max requests" + "\n" + str(e))
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
# print("These are the companies meeting your DCF threshold: ")
# print(final_companies)
print("Descending order of DCF discount and companies meeting threshold")
sorted_d = dict(sorted(discount_dict.items(), key=lambda x: x[1], reverse=True))
print(sorted_d)
print("\n")
