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
# snpSymbols = ['MMM','ABT','ABBV','ABMD','ACN','ATVI','ADBE','AMD','AAP','AES','AMG','AFL','A','APD','AKAM','ALK','ALB','ARE','ALXN','ALGN','ALLE','AGN','ADS','LNT','ALL','GOOG','GOOG','MO','AMZN','AMCR','AEE','AAL','AEP','AXP','AIG','AMT','AWK','AMP','ABC','AME','AMGN','APH','ADI','ANSS','ANTM','AON','AOS','APA','AIV','AAPL','AMAT','APTV','ADM','ARNC','ANET','AJG','AIZ','ATO','T','ADSK','ADP','AZO','AVB','AVY','BHGE','BLL','BAC','BK','BAX','BBT','BDX','BRK','BBY','BIIB','BLK','HRB','BA','BKNG','BWA','BXP','BSX','BMY','AVGO','BR','BF','B','CHRW','COG','CDNS','CPB','COF','CPRI','CAH','KMX','CCL','CAT','CBOE','CBRE','CBS','CDW','CE','CELG','CNC','CNP','CTL','CERN','CF','SCHW','CHTR','CVX','CMG','CB','CHD','CI','XEC','CINF','CTAS','CSCO','C','CFG','CTXS','CLX','CME','CMS','KO','CTSH','CL','CMCS','CMA','CAG','CXO','COP','ED','STZ','COO','CPRT','GLW','CTVA','COST','COTY','CCI','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DAL','XRAY','DVN','FANG','DLR','DFS','DISCA','DISCC','DISH','DG','DLTR','D','DOV','DOW','DTE','DUK','DRE','DD','DXC','ETFC','EMN','ETN','EBAY','ECL','EIX','EW','EA','EMR','ETR','EOG','EFX','EQIX','EQR','ESS','EL','EVRG','ES','RE','EXC','EXPE','EXPD','EXR','XOM','FFIV','FB','FAST','FRT','FDX','FIS','FITB','FE','FRC','FISV','FLT','FLIR','FLS','FMC','F','FTNT','FTV','FBHS','FOXA','FOX','BEN','FCX','GPS','GRMN','IT','GD','GE','GIS','GM','GPC','GILD','GL','GPN','GS','GWW','HAL','HBI','HOG','HIG','HAS','HCA','HCP','HP','HSIC','HSY','HES','HPE','HLT','HFC','HOLX','HD','HON','HRL','HST','HPQ','HUM','HBAN','HII','IEX','IDXX','INFO','ITW','ILMN','IR','INTC','ICE','IBM','INCY','IP','IPG','IFF','INTU','ISRG','IVZ','IPGP','IQV','IRM','JKHY','JEC','JBHT','SJM','JNJ','JCI','JPM','JNPR','KSU','K','KEY','KEYS','KMB','KIM','KMI','KLAC','KSS','KHC','KR','LB','LHX','LH','LRCX','LW','LEG','LDOS','LEN','LLY','LNC','LIN','LKQ','LMT','L','LOW','LYB','MTB','MAC','M','MRO','MPC','MKTX','MAR','MMC','MLM','MAS','MA','MKC','MXIM','MCD','MCK','MDT','MRK','MET','MTD','MGM','MCHP','MU','MSFT','MAA','MHK','TAP','MDLZ','MNST','MCO','MS','MOS','MSI','MSCI','MYL','NDAQ','NOV','NKTR','NTAP','NFLX','NWL','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NBL','JWN','NSC','NTRS','NOC','NCLH','NRG','NUE','NVDA','NVR','ORLY','OXY','OMC','OKE','ORCL','PCAR','PKG','PH','PAYX','PYPL','PNR','PBCT','PEP','PKI','PRGO','PFE','PM','PSX','PNW','PXD','PNC','PPG','PPL','PFG','PG','PGR','PLD','PRU','PEG','PSA','PHM','PVH','QRVO','PWR','QCOM','DGX','RL','RJF','RTN','O','REG','REGN','RF','RSG','RMD','RHI','ROK','ROL','ROP','ROST','RCL','CRM','SBAC','SLB','STX','SEE','SRE','SHW','SPG','SWKS','SLG','SNA','SO','LUV','SPGI','SWK','SBUX','STT','SYK','STI','SIVB','SYMC','SYF','SNPS','SYY','TMUS','TROW','TTWO','TPR','TGT','TEL','FTI','TFX','TXN','TXT','TMO','TIF','TWTR','TJX','TSCO','TDG','TRV','TRIP','TSN','UDR','ULTA','USB','UAA','UA','UNP','UAL','UNH','UPS','URI','UTX','UHS','UNM','VFC','VLO','VAR','VTR','VRSN','VRSK','VZ','VRTX','VIAB','V','VNO','VMC','WAB','WMT','WBA','DIS','WM','WAT','WEC','WCG','WFC','WELL','WDC','WU','WRK','WY','WHR','WMB','WLTW','WYNN','XEL','XRX','XLNX','XYL','YUM','ZBH','ZION','ZTS']
# dowSymbols = ['ALIM', 'AB', 'ATHM', 'BSVN', 'BSTC', 'CAMT', 'CHKP', 'CORT', 'ENTA', 'ENDP', 'EPM', 'FFIV', 'GRMN', 'GNTX', 'LANC', 'LOGI', 'MX', 'MPX', 'MGI', 'PETS', 'QNST', 'RMR', 'SWKS', 'SMMT', 'THC', 'TGI', 'YRCW', 'ZEAL']
# snpSymbols = ['BSBR', 'BMO', 'CM', 'CNQ', 'COP', 'DAL', 'DFS', 'EC', 'ET', 'EPD', 'FOX', 'FOXA', 'GM', 'MU', 'MPLX', 'NEM', 'NTRS', 'PSX', 'PPL', 'RY', 'RCL', 'SNE', 'SO', 'SOLN', 'SLF', 'SYF', 'TRP', 'BNS', 'TD', 'USB', 'UAL', 'WBA']
# snpSymbols = ['WUBA','AB','AMSF','ARNA','ANET','ATH','ATHM','BRC','CHKP','CORT','EQC','ESNT','EXEL','FFIV','FANH','GNTX','GHG','HLI','HMI','INFY','IRBT','KBAL','KL','MMS','MED','FIZZ','CNXN','QNST','REGN','RMR','SEIC','SWKS','TROW','TPL','UVE','USNA','VNDA']
# snpSymbols = ['MMM','ABT','ABBV','ABMD','ACN','ATVI','ADBE','AMD','AAP','AES','AMG','AFL','A','APD','AKAM','ALK','ALB']
#snpSymbols = ['MMM','ABT','ABBV','ABMD','ACN','ATVI','ADBE','AMD','AAP','AES','AMG','AFL','A','APD','AKAM','ALK','ALB','ARE','ALXN','ALGN','ALLE','AGN','ADS','LNT','ALL','GOOG','GOOG','MO','AMZN','AMCR','AEE','AAL','AEP','AXP','AIG','AMT','AWK','AMP','ABC','AME','AMGN','APH','ADI','ANSS','ANTM','AON','AOS','APA','AIV','AAPL','AMAT','APTV','ADM','ARNC','ANET','AJG','AIZ','ATO','T','ADSK','ADP','AZO','AVB','AVY','BHGE','BLL','BAC','BK','BAX','BBT','BDX','BRK','BBY','BIIB','BLK','HRB','BA','BKNG','BWA','BXP','BSX','BMY','AVGO','BR','BF','B','CHRW','COG','CDNS','CPB','COF','CPRI','CAH','KMX','CCL','CAT','CBOE','CBRE','CBS','CDW','CE','CELG','CNC','CNP','CTL','CERN','CF','SCHW','CHTR','CVX','CMG','CB','CHD','CI','XEC','CINF','CTAS','CSCO','C','CFG','CTXS','CLX','CME','CMS','KO','CTSH','CL','CMCS','CMA','CAG','CXO','COP','ED','STZ','COO','CPRT','GLW','CTVA','COST','COTY','CCI','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DAL','XRAY','DVN','FANG','DLR','DFS','DISCA','DISCC','DISH','DG','DLTR','D','DOV','DOW','DTE','DUK','DRE','DD','DXC','ETFC','EMN','ETN','EBAY','ECL','EIX','EW','EA','EMR','ETR','EOG','EFX','EQIX','EQR','ESS','EL','EVRG','ES','RE','EXC','EXPE','EXPD','EXR','XOM','FFIV','FB','FAST','FRT','FDX','FIS','FITB','FE','FRC','FISV','FLT','FLIR','FLS','FMC','F','FTNT','FTV','FBHS','FOXA','FOX','BEN','FCX','GPS','GRMN','IT','GD','GE','GIS','GM','GPC','GILD','GL','GPN','GS','GWW','HAL','HBI','HOG','HIG','HAS','HCA','HCP','HP','HSIC','HSY','HES','HPE','HLT','HFC','HOLX','HD','HON','HRL','HST','HPQ','HUM','HBAN','HII','IEX','IDXX','INFO','ITW','ILMN','IR','INTC','ICE','IBM','INCY','IP','IPG','IFF','INTU','ISRG','IVZ','IPGP','IQV','IRM','JKHY','JEC','JBHT','SJM','JNJ','JCI','JPM','JNPR','KSU','K','KEY','KEYS','KMB','KIM','KMI','KLAC','KSS','KHC','KR','LB','LHX','LH','LRCX','LW','LEG','LDOS','LEN','LLY','LNC','LIN','LKQ','LMT','L','LOW','LYB','MTB','MAC','M','MRO','MPC','MKTX','MAR','MMC','MLM','MAS','MA','MKC','MXIM','MCD','MCK','MDT','MRK','MET','MTD','MGM','MCHP','MU','MSFT','MAA','MHK','TAP','MDLZ','MNST','MCO','MS','MOS','MSI','MSCI','MYL','NDAQ','NOV','NKTR','NTAP','NFLX','NWL','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NBL','JWN','NSC','NTRS','NOC','NCLH','NRG','NUE','NVDA','NVR','ORLY','OXY','OMC','OKE','ORCL','PCAR','PKG','PH','PAYX','PYPL','PNR','PBCT','PEP','PKI','PRGO','PFE','PM','PSX','PNW','PXD','PNC','PPG','PPL','PFG','PG','PGR','PLD','PRU','PEG','PSA','PHM','PVH','QRVO','PWR','QCOM','DGX','RL','RJF','RTN','O','REG','REGN','RF','RSG','RMD','RHI','ROK','ROL','ROP','ROST','RCL','CRM','SBAC','SLB','STX','SEE','SRE','SHW','SPG','SWKS','SLG','SNA','SO','LUV','SPGI','SWK','SBUX','STT','SYK','STI','SIVB','SYMC','SYF','SNPS','SYY','TMUS','TROW','TTWO','TPR','TGT','TEL','FTI','TFX','TXN','TXT','TMO','TIF','TWTR','TJX','TSCO','TDG','TRV','TRIP','TSN','UDR','ULTA','USB','UAA','UA','UNP','UAL','UNH','UPS','URI','UTX','UHS','UNM','VFC','VLO','VAR','VTR','VRSN','VRSK','VZ','VRTX','VIAB','V','VNO','VMC','WAB','WMT','WBA','DIS','WM','WAT','WEC','WCG','WFC','WELL','WDC','WU','WRK','WY','WHR','WMB','WLTW','WYNN','XEL','XRX','XLNX','XYL','YUM','ZBH','ZION','ZTS']
#snpSymbols = ['TDOC','GNRC','NVCR','LITE','TREX','AMED','HAE','POR','REXR','TECD','RGEN','HR','DECK','BKH','FR','EGP','CHGG','ACAD','OGS','MSA','BXMT','RDN','FCN','SAIC','TTEK','JCOM','XTSLA','MRCY','ENPH','FIVN','TNDM','EME','TGNA','EXPO','MMS','DAR','AAXN','XLRN','SR','RETA','ALE','SYNH','HQY','ESNT','PNM','IOVA','NWE','WMGI','CHDN','LHCG','CRUS','TRNO','HELE','EVBG','DOC','VAC','SWX','PFGC','NVRO','GBT','SSD','SITE','BCO','ROLL','CCOI','SLAB','FCFS','STAG','CCMP','AVA','OMCL','ACIW','AMN','ENV','NHI','IPHI','AJRD','LIVN','MUSA','TXRH','FFIN','PRSP','NJR','SBRA','BLD','PTCT','NEOG','RLI','QTS','VRNT','STRA','AWR','ADC','BLKB','SIGI','GMED','EHTH','QTWO','PSB','BPMC','VLY','CBRL','VIAV','FGEN','SAM','BCPC','SF','QDEL','CBU','LPX','ARWR','GBCI','EE','MNTA','NUVA','RXN','NOVT','KBR','EYE','LANC','HALO','AXE','UFPI','IMMU','ITGR','UNF','MYOK','NEO','BL','SAFM','SHOO','PDM','BJ','ORA','WTS','CWT','IRDM','QLYS','WDFC','JBT','MEDP','RARE','KBH','IVR','RH','LXP','TMHC','MGEE','SEM','ADSW','EBS','EXLS','ACIA','SJI','KNSL','FELE','UBSI','PCH','POWI','LAD','PEGI','NSP','ONB','IRTC','ITRI','MRTX','TNET','CVBF','JJSF','MTZ','IIVI','KW','THC','ENS','CNMD','PENN','CWST','ARI','RHP','B','SYNA','FHI','CNNE','ARES','HOMB','ISBC','WING','BRC','AAN','GATX','FRPT','ARNA','FOXF','BRKS','BLDR','SMTC','SHO','RAMP','CNO','ICPT','MOGA','FOLD','ESE','AAON','IBKC','UMBF','ABM','BXS','LSCC','CSFL','PRLB','VSH','FTSV','WRE','WAFD','MTH','NTRA','AEIS','VRNS','HLI','RDFN','GNW','RPD','HWC','HASI','NSA','FULT','NWN','SSB','LAUR','LCII','PEB','SHEN','COLB','FN','TPH','CSOD','ASGN','MMSI','EPC','INDB','INSM','POL','ESGR','AXSM','MANT','KWR','WMS','FCPT','CATY','AKR','GEO','SXT','RUN','AIT','STMP','ENSG','BOX','HCSG','RWT','NG','WWW','MDC','HMSY','CMPR','AUB','OTTR','AAT','CTRE','YELP','AIN','SAIA','ROG','CCXI','PDCO','PLXS','FSS','ACA','UE','PMT','CXW','DEA','BMI','CLDR','KMT','ERI','PBH','SPXC','SAIL','IRWD','RLJ','AEO','SKYW','APLS','EPRT','VG','SJW','CMC','INST','FUL','CWK','IOSP','APPF','ATI','MNRO','KFY','SPSC','AEL','NYMT','AYR','DOOR','ABCB','SANM','LTC','SFNC','FG','SCL','CVCO','NTCT','NSIT','FRME','WD','CMP','LGND','HMN','MWA','WSBC','MLHR','BYD','USD','SUM','ROIC','PRAA','ROCK','DIOD','BDC','ATKR','DORM','EVTC','CLI','EPAY','NGVT','CFFN','ATGE','CWEN','RARX','WSFS','BHVN','GNL','CVLT','EGHT','HI','FORM','EPZM','ABG','BECN','ALGT','IBOC','FMBI','VC','TRTN','CARG','TRMK','FATE','AVNS','IDCC','CUB','PCRX','NAV','DAN','LILAK','ADNT','UNIT','CROX','XHR','INT','NMIH','SAVE','LADR','APPN','CPK','UCBI','TWNK','NVTA','ARGO','XNCR','FFBC','DRH','LGIH','GDOT','FIX','ALRM','SBH','KOD','WERN','MLI','VRRM','HTH','SFBS','FWRD','AIMC','FIT','GKOS','TOWN','PRGS','KTOS','AMBA','ICFI','SHAK','WABC','CVA','ONTO','TERP','ATRC','WK','KAMN','JACK','HUBG','RNST','MGRC','CRS','KTB','CNS','SVMK','ELY','KEM','FBP','SMPL','OPI','CSGS','MC','OSIS','BMCH','MATX','CSII','UHT','MINI','RMBS','AMWD','INOV','KPTI','FLOW','FSCT','PRO','MTX','NBTB','WBT','BEAT','YETI','HLNE','KALU','MTOR','BANR','KRG','NWBI','THRM','YEXT','USPH','KN','GTLS','HRTX','ILPT','CBZ','CLF','SCS','AQUA','LPSN','VGR','STAA','AMSF','IBP','MGLN','HTLF','IBTX','CAR','CAKE','DLX','DHC','APAM','GPI','HOPE','CORE','PZZA','GTN','GWB','MNR','CATM','ECPG','AVAV','RGNX','NTB','CTB','PRFT','NGHC','HURN','LZB','BLMN','VRTU','RCM','EIG','PSMT','HNI','BCC','LTHM','WW','TPTX','CALM','PRA','UVV','ALLK','LMNX','ESPR','IRT','VCYT','TNC','JRVR','TTMI','PPBI','TBPH','ALTR','CHRS','SBCF','SAFT','HL','AX','WGO','EDIT','STBA','EGOV','BBBY','IRBT','MDRX','SNBR','MYGN','PRNB','DRQ','SKY','NMRK','EPAC','INSP','FIBK','JELD','MSTR','ALEX','SYKE','HLIO','CENTA','NSTG','PFS','FBC','ODP','CSWI','PRK','TMP','WOR','CORT','CNX','ARR','MSEX','CADE','EGBN','AVX','AVYA','TEX','LNN','GCP','TRS','BAND','AIR','CHCO','ATRI','ZGNX','ARVN','ALLO','BHE','BGS','SWM','ALG','DIN','AFIN','DRNA','PLUG','TRHC','SBSI','AKBA','MLAB','SASR','CDNA','CVGW','NPO','MTSI','MEI','SKT','SWAV','ECOL','CASH','BRKL','COKE','DK','IIPR','SIG','RAVN','OCFC','RPT','SRG','EAT','FCF','IPAR','DCPH','BUSE','OXM','RUSHA','GTY','FDP','ZUO','WIRE','SCHL','INO','STAR','ATSG','PLUS','CRY','PJT','PRDO','CDE','UTL','DDD','WDR','RCII','SFIX','ADUS','ENTA','BHLB','NHC','KAI','FARO','LKFN','TGTX','RRR','TRUP','NP','VBTX','SFL','PATK','NTUS','REGI','NXRT','MDP','TRTX','ITCI','SMP','MHO','SGMO','GOLF','NNI','USNA','AMKR','OPK','RAD','PLOW','AIMT','CHCT','FOE','AHH','GMS','RVNC','DENN','DNLI','SWN','MXL','MED','MODN','MTRN','FDEF','ENDP','INFN','AZZ','STC','TENB','CLNC','SP','PRIM','TCBK','PGTI','VREX','CCS','ALEC','BATRK','INVA','IRET','TCMD','SUPN','PLAB','MATW','INGN','HA','EVOP','GLNG','DNOW','BKD','GPMT','SEAS','KRNY','VVI','IMAX','FBNC','GIII','HTLD','DBI','TIVO','AMBC','OMER','RLGY','LRN','TILE','GEF','HFWA','HTZ','PIPR','HNGR','MAXR','TWST','VCRA','CLBK','OFG','CTS','CYTK','INN','COOP','NBHC','MRTN','CBB','XENT','RDNT','EFSC','GVA','ASTE','PDCE','HCC','UFCS','VICR','SONO','PLAY','FOCS','TGI','SSYS','GLUU','CERS','COHU','CWENA','UCTT','ACLS','FSP','RDUS','EBSB','ACCO','BANF','KNL','XPER','BRBR','RGR','TCDA','SSTK','WHD','SXI','UPLD','BCOR','STNG','PLCE','ALX','UVE','OEC','MBUU','ATNX','BIG','GABC','ANF','PLMR','SAFE','TSE','PSN','BPFH','LC','MMI','APOG','KDMN','TRST','PTLA','HSC','CMO','AGM','MDGL','JBSS','CMCO','NRC','COLL','WSC','PRSC','CVI','HRI','RTRX','CRMT','HSTM','CARO','AERI','SGMS','LILA','BBIO','SYBT','CDLX','INTL','CDXS','RESI','JOE','HSKA','VRTS','LBAI','VECO','CNOB','YORW','BKE','SCSC','TPRE','BMTC','GBX','AKS','YMAB','SAH','SILK','GFF','CYRX','MSGN','ATRA','PNTG','PFBC','ICHR','RCUS','KFRC','CEVA','AROC','CRVL','UIS','ATNI','HEES','GES','DY','CCF','ARCH','IMKTA','ENVA','CARA','CHEF','NXTC','TR','GLDD','UBA','CIR','WASH','VCEL','NCBS','WNC','EVH','TBK','PETS','GSHD','UVSP','MBI','RCKT','ANDE','LNTH','NTGR','KRYS','BOOT','IMGN','QUOT','BANC','OFIX','ADVM','CPF','GRC','WIFI','EIDX','FIZZ','AGX','TTEC','NWLI','AMPH','CAC','MGY','EXTR','CLDT','GOOD','CASS','MTSC','LLNW','AXL','GTHX','NFBK','TROX','VNDA','GLT','TBI','AXNX','HMST','CMTL','BLX','VEC','EBIX','AEGN','PACB','CTBI','RMR','SSP','ANIK','INSW','ABTX','NVEE','VRS','UEIC','NXGN','TPIC','URGN','CIO','ATEX','PETQ','GSBC','EVRI','SRCE','BJRI','PAHC','AGYS','ATRS','QCRH','AAWW','ARCB','DHT','THR','HLIT','ZUMZ','KELYA','QADA','CNST','WINA','RYTM','OBNK','WMC','NTLA','DDS','APPS','OII','TPC','FFWM','EFC','CUBI','KBAL','QNST','KREF','AMRC','EBF','HBNC','GOSS','RMAX','THFF','FIXX','DCOM','MYE','BCRX','TBBK','FBK','SRI','OSPN','BE','CARS','MCS','PBI','UPWK','BFS','ZIOP','NX','PEBO','SNR','FLXN','TCX','HSII','TTGT','MITT','PGC','OMN','HMHC','CKH','FLWS','LASR','AVD','HTBK','WETF','GRPN','BMRC','FBMS','MSBI','CNXN','MEET','LMAT','CRTX','NGM','GPRO','FFIC','UMH','SPWR','ECHO','GMRE','VSLR','TVTY','PHAT','RILY','EB','SPAR','PARR','WSR','AMSWA','CNDT','ANAB','ANGO','BSIG','OPCH','MYRG','DCO','ASMB','RC','WTRE','NPK','CNSL','FLIC','HLX','STFC','SLP','LXFR','HAFC','SRDX','GCO','APTS','OPB','SPTN','FFG','CLW','RUTH','AXGN','HY','AVRO','GTT','TSC','KIDS','MBWM','CORR','RUBI','MGPI','TGH','DBD','CTT','PQG','CALX','ATRO','MCRI','BBSI','BV','WPG','WSBF','ACRE','KRTX','PFSI','WAAS','CUE','ANIP','TLRA','CHS','FSB','LVGO','DHIL','PRTA','PDFS','NAT','PDLI','BDGE','WRLD','CBTX','CYH','JCAP','CVM','TG','TDW','OLP','IIIV','TRWH','ELF','SCHN','HCKT','IBCP','GCI','FORR','VKTX','HWKN','OSUR','PI','CAL','AMRX','ZIXI','BDSI','AROW','EGRX','AOBC','KURA','WMK','FMBH','PGNX','CRAI','ERII','FCBC','TNK','MOBL','ORC','DX','SWTX','LORL','RIGL','CETV','FMNB','SCU','BSTC','CPRX','TXMD','HCCI','ADTN','NCMI','KIN','RECN','IIIN','CDMO','RVI','GME','GTS','COWN','OSW','ACBI','NEX','BFC','CAI','USCR','BOOM','BNFT','MLR','APEI','HIBB','TRC','PUMP','FISI','ETM','PUB','VIVO','CSV','EQBK','DGII','CLVS','PFNX','BZH','VHC','CATO','RST','PLT','UFPT','MTRX','TISI','VSTO','AMK','RBCAA','KOP','HVT','FBM','MTW','MGNX','MSFUT','BY','REX','XAN','LOB','AXDX','MPAA','CPSI','CHUY','HTBI','WTBA','EVER','ETH','FRPH','MRC','UNFI','BFYT','ODT','DSPG','SGH','CARE','JOUT','DVAX','OMI','HABT','BHB','IOTS','PFIS','UTMD','PBYI','ANH','CCRN','ARDX','HT','GNMK','NVAX','CCBG','WLDN','MOFG','STRL','CTMX','CMRE','HRTG','KE','VIR','MIK','CCNE','CUTR','SPPI','DXPE','BSRR','ARTNA','BCOV','SIGA','CENT','CWH','NVEC','TEN','HZO','AMNB','NPTN','VIE','PGNY','AMTB','DOMO','QTRX','OOMA','SRNE','CNR','CTO','MGTX','ATEN','HCI','CALA','PING','MTEM','UFI','ASIX','MTDR','HAYN','SCVL','GBLI','SIBN','DTIL','SSTI','IGMS','MRSN','OCUL','ROAD','PHR','AGEN','NWPX','TBIO','CIVB','BLBD','PAR','CATC','LCI','MCB','BWB','DJCO','FC','BRY','MOD','SRRK','OSBC','CLNE','MITK','PCSB','LL','TRUE','PKE','VPG','CRBP','FF','SMBC','WTTR','GLRE','LMNR','RUBY','LNDC','KRA','AMAG','VYGR','GRBK','AMOT','FNLC','NOG','HUD','BFST','INSG','BTU','CIA','KNSA','RGS','POWL','DSSI','HONE','CWCO','SOI','LAND','SONA','BRG','GORO','IVC','FOSL','CPS','EBTC','NNBR','SGRY','MCFT','CPLG','SXC','AJX','MNKD','RGCO','STML','NOVA','ALBO','EZPW','BATRA','HCAT','CLAR','CAMP','CZNC','DFIN','SFST','FMAO','SNDX','OFLX','APLT','HIFS','SENEA','BRP','NSSC','RBB','SYX','AT','MCBC','RRBI','ECOM','PAYS','NKSH','ARAY','VSEC','FI','APRE','REAL','SPWH','SMMF','ARLO','LPG','STXB','BTAI','FOR','INS','NERV','DMRC','GNTY','CRNX','LOCO','RMTI','GEFB','MOV','STOK','CSTE','LIND','CENX','LTRPA','AOSL','MGTA','PCYO','RRGB','CNCE','NRIM','FCBP','XBIT','SYRS','HBCP','AMC','TMDX','AMAL','GPRE','WVE','ACNB','RM','BCEI','BREW','OPY','ITIC','ATLO','CHMI','REPH','LBRT','PFBI','TRNS','INBK','MCBS','FCAP','CRC','SMBK','ZYXI','FRTA','GDEN','GERN','APYX','TBNK','ATEC','SPNE','ADRO','OIS','FLDM','PWOD','JCP','NATH','UIHC','LCNB','CECE','BOMN','TPB','NBR','AKCA','AMRS','OYST','CBMG','MNK','CTSO','CLCT','HOFT','LBC','HMTV','SPOK','WNEB','REVG','RTIX','PGEN','TNAV','EXPR','DAKT','EIGI','ATHX','SHBI','CNBKA','AI','SNCR','CDR','IESC','ORBC','CVCY','EIGR','IHC','ITI','EXPI','PICO','JYNT','KRO','GRTS','MFSF','CTRN','NDLS','VBIV','KALA','TITN','ZAGG','BCML','CVLY','AVID','CELH','DNR','ORRF','FPI','RBBN','PKOH','HURC','SM','IMMR','CSTR','MNLO','RBNC','LFVN','IMXI','REPL','TALO','FSBW','RFL','RUSHB','I','ONDK','TPCO','GTYH','BOCH','BHR','PKBK','ENZ','FVCB','TMST','CPE','WHG','LDL','BBX','FBIZ','ASC','MNRL','ODC','SENS','SPFI','AGLE','NESR','TK','NWFL','RCKY','HOME','BYSI','HBMD','FRBA','FRGI','VRA','RMBI','ISTR','VRAY','MNOV','KALV','MRLN','CEIX','CHMA','EXTN','STRS','GOGO','TLRD','GHL','BCBP','AVXL','UBX','ESXB','FSTR','TSBK','RLGT','BWFG','AGS','SLCT','MVBF','VLGEA','USLM','AFMD','KVHI','CLPR','AAOI','ERA','OSG','WTI','CDXC','TIPT','EVBN','NR','SFE','QEP','MMAC','EROS','SBBX','CRMD','DGICA','GLOG','ARA','TACO','MBIN','BRT','OPRT','BCEL','HFFG','CNTY','CVTI','BGSF','PTGX','EEX','EGAN','GHM','FNKO','AKTS','AHT','PBFS','LAWS','RES','SALT','ESSA','VAPO','PCB','BPRN','ADMA','GWRS','VRCA','RICK','BFIN','NBN','FCCY','SIC','OSTK','CDZI','PLPC','ESQ','RYI','NODK','AMSC','BNED','UNTY','FNHC','OCN','FDBC','NC','PIRS','FRBK','INWK','MNSB','SCOR','EVC','ADES','OPTN','OVBC','PTVCB','MEIP','PRTK','FNWB','MPB','CFFI','TCFC','WEYS','ALCO','HBT','SIEN','PBIP','ULH','PROS','NBEV','CCB','TCRR','GNC','RVSB','EOLS','FARM','EML','QUAD','PEBK','SPRO','CONN','IPI','FPRX','PTN','TLYS','MCRB','UBFO','MLVF','REV','CRDA','WLFC','CMLS','FRAF','WOW','STSA','DSKE','SLCA','CURO','AXTI','GCAP','SGC','SPKE','LQDT','HWBK','MDCA','DO','CLFD','FREQ','CBAY','PRVL','ETNB','UNB','GEOS','SHSP','CSTL','BGG','PZN','EGLE','SMHI','PEI','OPBK','XFOR','RRD','DHX','GPX','GLYC','EPM','HOOK','GEN','HARP','MESA','MFNC','OAS','AKRO','UUUU','LEVL','TUP','MSON','IDT','CHMG','CATS','FLMN','IIN','MG','TREC','ACRX','CVGI','LJPC','MPX','MRNS','GFN','PDLB','SGA','BLFS','OVLY','FNCB','RDI','TH','OPRX','IRMD','DLA','UEC','SCWX','ZEUS','HALL','CBNK','PMBC','PROV','GSIT','GENC','XXII','AMEH','STRO','FFNW','PRPL','LXRX','BELFB','VRTV','CBAN','AC','GCBC','SVRA','EVI','DS','CASI','SYNL','III','GNK','JAX','LCTX','GALT','FLXS','CRK','GPOR','GBL','CABA','CSLT','PLSE','LE','SAMG','TELL','CASA','NGS','SBT','PBPB','CULP','MFIN','ADMS','TAST','ZYNE','TWIN','BH','GNE','ELOX','ABEO','BSET','ESCA','BBCP','FGBI','ACTG','LPI','SBBP','RMNI','MCHX','FLNT','CMRX','TEUM','HBB','CTRA','MBIO','GAIA','AKRX','USX','NATR','MORF','PVAC','TWI','WLL','EVFM','PVBC','CYCN','RYAM','LOVE','PRTY','LEGH','SRT','CBL','ASRT','TTI','ALDX','NE','XGN','CCO','ELVT','KLDO','BXC','KZR','PTSI','LEE','FULC','CFB','PHX','ALOT','EYPT','AIRG','MLND','PSNL','TYME','MLP','LCUT','JNCE','EVLO','PRGX','SB','DLTH','MRKR','SLDB','SOLY','LOGC','CERC','YRCW','MR','NGVC','BSGM','SIEB','MJCO','RLH','ALRS','FTK','XERS','ALTM','OSMT','GRIF','TCI','LQDA','BXG','ASPS','OCX','KRUS','BSVN','PHAS','FTR','ESTE','MBII','PNRG','ACOR','RNET','INSE','TZOO','CVIA','WRTC','TCS','TOCA','BXRX','SI','CFMS','DZSI','MEC','REI','CELC','CKPT','ENOB','LEAF','CLXT','LXU','SD','MIRM','CNTG','ACRS','VHI','VALU','GDP','SDRL','LIVX','CTRC','ORGO','HPR','AFI','RAPT','WATT','BRID','AVCO','TESS','AXLA','STIM','PYX','CODA','PHUN','XOG','GWGH','RRTS','KLXE','SYBX','CHRA','ASNA','ARL','METC','NEXT','CMBM','NL','NTGN','VNCE','GNLN','CIX','FET','SND','SONM','NINE','PACD','AGE','AMPY','GRTX','AXAS','TORC','WTRH','HNRG','FTSI','CMCT','USWS','ACER','PTE','IDEX','CHAP','UNT','XELA','SBOW','PRTH','ICD','JILL','YGYI','NCSM','YCBD','ECOR','RTW','TUSK','ROSE','TRXC','GTXI','RTYH0','P5N994','CLMS']
snpSymbols = ['TDOC','GNRC','NVCR','LITE','TREX','AMED']
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
            if (key == 'financials'):
                tmp = value
                #print("tmp:")
                #print (tmp)
                for lst_item in tmp:
                    for key, value in lst_item.items():
                        # print('key: {} value: {}'.format(key, value))
                        if (key == 'date'):
                            datesIncome.append(value)
                        elif (key == 'EBIT'):
                            ebit.append(value)
                        elif (key == 'EPS'):
                            eps.append(value)
        # print (datesIncome)
        # print ("EBIT: \n")
        # print (ebit)
        #print(eps[-1])
        if (int(float(eps[-1])) >= 0):
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
            if (key == 'financials'):
                tmp = value
                # print (tmp)
                for lst_item in tmp:
                    for key, value in lst_item.items():
                        # print('key: {} value: {}'.format(key, value))
                        if (key == 'date'):
                            datesBalance.append(value)
                        elif (key == 'Total assets'):
                            ta.append(value)
                        elif (key == 'Total current liabilities'):
                            tcl.append(value)

        # print ("TA: \n")
        # print (ta)
        # print ("TCL: \n")
        # print (tcl)
        request.close()
        # print ("Done")
        n = len(datesIncome)
        m = len(datesBalance)

        if (areEqual(datesIncome, datesBalance, n, m)):
            print("******************************Data available*******************************************" + "\n")
            for i in range(0, len(ta)):
                # print (float(re.sub("[^\d\.\-]", "", tcl[i])))
                roce = 100 * float(re.sub("[^\d\.\-]", "", ebit[i])) / (
                        float((re.sub("[^\d\.\-]", "", ta[i]))) - float((re.sub("[^\d\.\-]", "", tcl[i]))))
                if (roce > 0):
                    print(
                        f'Inc. Stmt Date: {datesIncome[i]}, Balance Sheet Date: {datesBalance[i]} and ROCE on that date was {roce:.2f}%')
                    print("EBIT: " + ebit[i])
                    print("TA: " + ta[i])
                    print("TCL: " + tcl[i] + "\n")
                    if comp1 in roce_dict.keys():
                        roce_dict.setdefault(comp1, []).append(round(roce, 2))
                elif (roce < 0):
                    if comp1 not in negative_roce_companies:
                        negative_roce_companies.append(comp1)
                    print(Fore.RED + "Negative ROCE" + "\n")
                    # print(Style.RESET_ALL)
                    # print (f'Date: {datesIncome[i]} and ROCE on that date was {roce:.2f}%'+"\n")
                    # if comp1 in roce_dict.keys():
                    # roce_dict.setdefault(comp1, []).append(round(roce, 2))
        else:
            print("The income statement and balance sheet could not be found for the same dates.")
            data_unavailable_companies.append(comp1)


    except ZeroDivisionError:
        print("Some data not available (Zero division error)" + "\n")
        data_unavailable_companies.append(comp1)
        print("*****************************************************************************" + "\n")
    except ValueError:
        print("Some data not available (Value)" + "\n")
        data_unavailable_companies.append(comp1)
        print("*****************************************************************************" + "\n")
    except IndexError:
        print("Data not available (Index)" + "\n")
        data_unavailable_companies.append(comp1)
        print("*****************************************************************************" + "\n")
    except AttributeError as err:
        print("Data not available (Attribute)" + "\n")
        data_unavailable_companies.append(comp1)
        print("*****************************************************************************" + "\n")
        logger.warning("The data was not available: {}".format(err) + "\n")
    return

def get_positive(val1):
        try:
            val = int(val1)
            if val >= 0:
                return true
            else:
                return false
        except ValueError:
            return false

def areEqual(arr1, arr2, n, m):
    if (n != m):
        return False
    # Sort both arrays 
    arr1.sort()
    arr2.sort()
    # Linearly compare elements 
    for i in range(0, n - 1):
        if (arr1[i] != arr2[i]):
            return False
    # If all elements were same.
    return True


for i in range(0, len(snpSymbols)):  # len(dowSymbols
    try:
        # Basic API URL
        url_is_y = 'https://financialmodelingprep.com/api/v3/financials/income-statement/' + snpSymbols[i]
        url_bs_y = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/' + snpSymbols[i]
        url_is_q = 'https://financialmodelingprep.com/api/v3/financials/income-statement/' + snpSymbols[
            i] + '?period=quarter'
        url_bs_q = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/' + snpSymbols[
            i] + '?period=quarter'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        roce_dict[snpSymbols[i]] = []
        # print (dowSymbols[i] + " Quarterly:")
        # roce_q = calc_roce (dowSymbols[i], url_is_q,url_bs_q)
        print(snpSymbols[i] + " Yearly:")
        roce_y = calc_roce(snpSymbols[i], url_is_y, url_bs_y)
        #print("ROCE Dict")
        #print(roce_dict)
        tmp = np.diff(roce_dict[snpSymbols[i]])
        # print ('The magic number is {}'.format(sum(tmp)*-1))
        sort_dict[snpSymbols[i]] = round(((sum(tmp) * -1) / (len(tmp) + 1)), 2)  # This is the magic number: Upen
        # print ("Sorted Dict:")
        # print (sort_dict)
        avg_dict[snpSymbols[i]] = round(sum(roce_dict[snpSymbols[i]]) / len(roce_dict[snpSymbols[i]]), 2)
    # print("Avg. Dict")
    # print(avg_dict)
    except ValueError:
        print("More data not available (Value)" + "\n")
        print("*****************************************************************************" + "\n")
    except ZeroDivisionError:
        print("Some data not available (Zero division error)" + "\n")
        print("*****************************************************************************" + "\n")
    except IndexError:
        print("Data not available (Index)" + "\n")
        print("*****************************************************************************" + "\n")
    except AttributeError as err:
        print("Data not available (Attribute)" + "\n")
        print("*****************************************************************************" + "\n")
        logger.warning("The data was not available: {}".format(err) + "\n")
    continue
#print("The order of companies from best to worst (based on year-on-year growth of ROCE):")
#print(sorted(sort_dict.items(), key=lambda x: x[1], reverse=True))
#print("List of data available companies: ")
data_available_companies = set(snpSymbols) ^ set(data_unavailable_companies)
#print(data_available_companies)
print("List excluding negative ROCE companies: ")
print(set(snpSymbols) ^ set(negative_roce_companies))
final_companies = dict((k, v) for k, v in avg_dict.items() if v >= threshold)
#print("Final companies: ")
#print (final_companies)
print("List of companies meeting the threshold: ")
print(sorted(final_companies.items(), key=lambda x: x[1], reverse=True))
print("List of companies meeting the threshold and whose data is available: ")
kv = [(k, final_companies[k]) for k in data_available_companies if k in final_companies]
lv = sorted(kv, key=lambda x: x[1], reverse=True)
print (lv)
print("List of companies meeting the threshold, whose data is available and have positive EPS: ")
kv = [(k, final_companies[k]) for k in positive_eps_companies if k in final_companies]
lv = sorted(kv, key=lambda x: x[1], reverse=True)
print (lv)
print("********************************************" + "\n")
