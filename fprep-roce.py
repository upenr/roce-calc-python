import requests
import json
import re
import logging
from urllib.request import urlopen
from collections import defaultdict
import numpy as np
from colorama import init, Fore, Back, Style
init(convert=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#snpSymbols = ['MMM','ABT','ABBV','ABMD','ACN','ATVI','ADBE','AMD','AAP','AES','AMG','AFL','A','APD','AKAM','ALK','ALB','ARE','ALXN','ALGN','ALLE','AGN','ADS','LNT','ALL','GOOG','GOOG','MO','AMZN','AMCR','AEE','AAL','AEP','AXP','AIG','AMT','AWK','AMP','ABC','AME','AMGN','APH','ADI','ANSS','ANTM','AON','AOS','APA','AIV','AAPL','AMAT','APTV','ADM','ARNC','ANET','AJG','AIZ','ATO','T','ADSK','ADP','AZO','AVB','AVY','BHGE','BLL','BAC','BK','BAX','BBT','BDX','BRK','BBY','BIIB','BLK','HRB','BA','BKNG','BWA','BXP','BSX','BMY','AVGO','BR','BF','B','CHRW','COG','CDNS','CPB','COF','CPRI','CAH','KMX','CCL','CAT','CBOE','CBRE','CBS','CDW','CE','CELG','CNC','CNP','CTL','CERN','CF','SCHW','CHTR','CVX','CMG','CB','CHD','CI','XEC','CINF','CTAS','CSCO','C','CFG','CTXS','CLX','CME','CMS','KO','CTSH','CL','CMCS','CMA','CAG','CXO','COP','ED','STZ','COO','CPRT','GLW','CTVA','COST','COTY','CCI','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DAL','XRAY','DVN','FANG','DLR','DFS','DISCA','DISCC','DISH','DG','DLTR','D','DOV','DOW','DTE','DUK','DRE','DD','DXC','ETFC','EMN','ETN','EBAY','ECL','EIX','EW','EA','EMR','ETR','EOG','EFX','EQIX','EQR','ESS','EL','EVRG','ES','RE','EXC','EXPE','EXPD','EXR','XOM','FFIV','FB','FAST','FRT','FDX','FIS','FITB','FE','FRC','FISV','FLT','FLIR','FLS','FMC','F','FTNT','FTV','FBHS','FOXA','FOX','BEN','FCX','GPS','GRMN','IT','GD','GE','GIS','GM','GPC','GILD','GL','GPN','GS','GWW','HAL','HBI','HOG','HIG','HAS','HCA','HCP','HP','HSIC','HSY','HES','HPE','HLT','HFC','HOLX','HD','HON','HRL','HST','HPQ','HUM','HBAN','HII','IEX','IDXX','INFO','ITW','ILMN','IR','INTC','ICE','IBM','INCY','IP','IPG','IFF','INTU','ISRG','IVZ','IPGP','IQV','IRM','JKHY','JEC','JBHT','SJM','JNJ','JCI','JPM','JNPR','KSU','K','KEY','KEYS','KMB','KIM','KMI','KLAC','KSS','KHC','KR','LB','LHX','LH','LRCX','LW','LEG','LDOS','LEN','LLY','LNC','LIN','LKQ','LMT','L','LOW','LYB','MTB','MAC','M','MRO','MPC','MKTX','MAR','MMC','MLM','MAS','MA','MKC','MXIM','MCD','MCK','MDT','MRK','MET','MTD','MGM','MCHP','MU','MSFT','MAA','MHK','TAP','MDLZ','MNST','MCO','MS','MOS','MSI','MSCI','MYL','NDAQ','NOV','NKTR','NTAP','NFLX','NWL','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NBL','JWN','NSC','NTRS','NOC','NCLH','NRG','NUE','NVDA','NVR','ORLY','OXY','OMC','OKE','ORCL','PCAR','PKG','PH','PAYX','PYPL','PNR','PBCT','PEP','PKI','PRGO','PFE','PM','PSX','PNW','PXD','PNC','PPG','PPL','PFG','PG','PGR','PLD','PRU','PEG','PSA','PHM','PVH','QRVO','PWR','QCOM','DGX','RL','RJF','RTN','O','REG','REGN','RF','RSG','RMD','RHI','ROK','ROL','ROP','ROST','RCL','CRM','SBAC','SLB','STX','SEE','SRE','SHW','SPG','SWKS','SLG','SNA','SO','LUV','SPGI','SWK','SBUX','STT','SYK','STI','SIVB','SYMC','SYF','SNPS','SYY','TMUS','TROW','TTWO','TPR','TGT','TEL','FTI','TFX','TXN','TXT','TMO','TIF','TWTR','TJX','TSCO','TDG','TRV','TRIP','TSN','UDR','ULTA','USB','UAA','UA','UNP','UAL','UNH','UPS','URI','UTX','UHS','UNM','VFC','VLO','VAR','VTR','VRSN','VRSK','VZ','VRTX','VIAB','V','VNO','VMC','WAB','WMT','WBA','DIS','WM','WAT','WEC','WCG','WFC','WELL','WDC','WU','WRK','WY','WHR','WMB','WLTW','WYNN','XEL','XRX','XLNX','XYL','YUM','ZBH','ZION','ZTS']
#dowSymbols = ['ALIM', 'AB', 'ATHM', 'BSVN', 'BSTC', 'CAMT', 'CHKP', 'CORT', 'ENTA', 'ENDP', 'EPM', 'FFIV', 'GRMN', 'GNTX', 'LANC', 'LOGI', 'MX', 'MPX', 'MGI', 'PETS', 'QNST', 'RMR', 'SWKS', 'SMMT', 'THC', 'TGI', 'YRCW', 'ZEAL']
snpSymbols = ["AAPL", "TROW", "M"]
roce_dict = {}
sort_dict = {}
negative_roce_companies = []

def calc_roce (comp1, url, url2):
  try:
    request = urlopen(url)
    response = request.read()
    data = json.loads(response)
    #print (data)
    dates = []
    ta = []
    tcl = []
    ebit = []
    
    #for i in data['financials']:
    #  print (i.date)
    for key, value in data.items():
      if (key =='financials'):
        tmp = value
        for lst_item in tmp:
          for key, value in lst_item.items():
            #print('key: {} value: {}'.format(key, value))
            if (key == 'date'):
              dates.append(value)
            elif (key == 'EBIT'):
              ebit.append (value)
    #print (dates)
    #print (ebit)
    request.close()
    #Second Page
    #print (url2)
    request = urlopen(url2)
    response = request.read()
    data = json.loads(response)
    if not data.get("financials"):
      print ("Data not available. Manual check may be needed for this company.")
    for key, value in data.items():
      if (key =='financials'):
        tmp = value
        for lst_item in tmp:
          for key, value in lst_item.items():
            #print('key: {} value: {}'.format(key, value))
            if (key == 'Total assets'):
              ta.append(value)
            elif (key == 'Total current liabilities'):
              tcl.append (value)
    print (ta)
    print (tcl)
    request.close()
    #print ("Done")
    for i in range(0, len(ta)):
        #print (float(re.sub("[^\d\.\-]", "", tcl[i])))
        roce = 100*float(re.sub("[^\d\.\-]", "", ebit[i]))/(float((re.sub("[^\d\.\-]", "", ta[i])))-float((re.sub("[^\d\.\-]", "", tcl[i]))))
        if (roce>0):
          print (f'Date: {dates[i]} and ROCE on that date was {roce:.2f}%'+"\n")
          if comp1 in roce_dict.keys(): 
              roce_dict.setdefault(comp1, []).append(round(roce,2))
        elif (roce<0):
          if comp1 not in negative_roce_companies:
            negative_roce_companies.append(comp1)
          print (Fore.RED+"Negative ROCE"+"\n")
          print(Style.RESET_ALL) 
          #print (f'Date: {dates[i]} and ROCE on that date was {roce:.2f}%'+"\n")
          if comp1 in roce_dict.keys(): 
              roce_dict.setdefault(comp1, []).append(round(roce,2))
    print ("******************************DONE*******************************************"+"\n")
  except ZeroDivisionError:
    print ("Some data not available (Zero division error)"+"\n")
    print ("*****************************************************************************"+"\n")
  except ValueError:
    print ("Some data not available (Value)"+"\n")
    print ("*****************************************************************************"+"\n")
  except IndexError:
    print ("Data not available (Index)"+"\n")
    print ("*****************************************************************************"+"\n")
  except AttributeError as err:
    print ("Data not available (Attribute)"+"\n")
    print ("*****************************************************************************"+"\n")
    logger.warning("The data was not available: {}".format(err)+"\n")
  return


for i in range (0, len(snpSymbols)): #len(dowSymbols
  try:
    # Basic API URL
    url_is_y = 'https://financialmodelingprep.com/api/v3/financials/income-statement/'+snpSymbols[i]
    url_bs_y = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/'+snpSymbols[i]
    url_is_q = 'https://financialmodelingprep.com/api/v3/financials/income-statement/'+snpSymbols[i]+'?period=quarter'
    url_bs_q = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/'+snpSymbols[i]+'?period=quarter'
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
    roce_dict[snpSymbols[i]] = []
    #print (dowSymbols[i] + " Quarterly:")
    #roce_q = calc_roce (dowSymbols[i], url_is_q,url_bs_q)
    print (snpSymbols[i] + " Yearly:")
    roce_y = calc_roce (snpSymbols[i], url_is_y,url_bs_y)
    #print(roce_dict)
    tmp = np.diff(roce_dict[snpSymbols[i]])
    #print ('The magic number is {}'.format(sum(tmp)*-1))
    sort_dict [snpSymbols[i]] = round(((sum(tmp)*-1)/(len(tmp)+1)),2) #This is the magic number: Upen
    #print (sort_dict)
  except ValueError:
    print ("More data not available (Value)"+"\n")
    print ("*****************************************************************************"+"\n")
  except IndexError:
    print ("Data not available (Index)"+"\n")
    print ("*****************************************************************************"+"\n")
  except AttributeError as err:
    print ("Data not available (Attribute)"+"\n")
    print ("*****************************************************************************"+"\n")
    logger.warning("The data was not available: {}".format(err)+"\n")
    continue
print ("The order of companies from best to worst (based on year-on-year growth of ROCE):")
print (sorted(sort_dict.items(), key = lambda x : x[1], reverse=True))
print ("Negative ROCE companies: ")
print (negative_roce_companies)
print ("List excluding negative ROCE companies: ")
print("**************"+"\n")
