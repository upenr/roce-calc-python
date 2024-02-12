from operator import contains
import sqlite3
dbase = sqlite3.connect('stock-dcf-terminal.db') # Open a database File
cursor = dbase.cursor()
print ('Database opened')
print ('Cursor created')
list1 = {'ADM','ALK','APA','T','BBWI','BBY','BWA','CE','CF','CHTR','CMCSA','COP','GLW','CVS','DVA','DVN','FANG','DISH','DOW','DXC','EMN','RE','EXPE','FDX','F','FOXA','FOX','FCX','GILD','GM','HCA','HPE','HOLX','HPQ','INTC','IP','IPG','KMI','KR','LH','LUMN','LYB','MRO','FB','MU','MRNA','MHK','MOH','MOS','NEM','NWSA','NWS','NUE','OXY','OGN','PFE','PXD','PVH','QRVO','DGX','STX','SYF','TROW','UAA','UA','URI','VZ','VTRS','WDC','WRK','WY','WHR'}
list2 = {'MMM','ADM','AKAM','ALK','APA','T','BBWI','BBY','BWA','CE','CF','CHTR','CMCSA','COP','GLW','CVS','DVA','FANG','DISH','DOW','DXC','EMN','EBAY','EOG','RE','EXPE','XOM','FDX','F','FOXA','FOX','FCX','GILD','GM','HCA','HPE','HOLX','HPQ','INTC','IP','IPG','IPGP','KMI','KR','LH','LEN','LUMN','LYB','MRO','FB','MU','MRNA','MHK','TAP','MOS','NEM','NWSA','NWS','NUE','NVR','OXY','OGN','PFE','PSX','PHM','PVH','QRVO','DGX','STX','SWKS','SYF','TROW','TGT','TXT','TSN','UAA','UA','URI','VZ','VTRS','WDC','WRK','WY','WHR'}

#Differences between list1 and list2
list3 = set(list1) - set(list2)
print (list3)

#Find stock names from items in list3

ticker_list = ['MRNA', 'UAA', 'LEN', 'PSX', 'TGT', 'OXY', 'CHTR', 'DXC', 'IPGP', 'LH', 'LYB', 'BWA', 'TROW', 'PFE', 'WHR', 'URI', 'PVH', 'CE', 'NEM', 'ALK', 'GILD', 'UA', 'FOXA', 'HPQ', 'FOX', 'EBAY', 'HCA', 'MMM', 'KR', 'FB', 'EXPE', 'APA', 'NWSA', 'VTRS', 'ADM', 'CVS', 'OGN', 'QRVO', 'TXT', 'CF', 'GLW', 'MU', 'DGX', 'MOS', 'STX', 'FANG', 'CMCSA', 'IPG', 'LUMN', 'PHM', 'NVR', 'COP', 'BBWI', 'NUE', 'SWKS', 'WY', 'EMN', 'MRO', 'FCX', 'WDC', 'XOM', 'AKAM', 'TSN', 'EOG', 'NWS', 'KMI']

