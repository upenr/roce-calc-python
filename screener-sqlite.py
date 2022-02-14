import sqlite3

dbase = sqlite3.connect('stock-data.db') # Open a database File
cursor = dbase.cursor()
print ('Database opened')
print ('Cursor created')

dbase.execute(''' CREATE TABLE IF NOT EXISTS stock_analysis_upen(
    ID INT PRIMARY KEY NOT NULL,
    NAME TEXT NOT NULL,
    DCFPRICE INT NULL,
    CURRENTPRICE INT NULL, 
    DISCOUNT INT NULL) ''')

print ('Table created')

def add_Data():
    dbase.execute("INSERT INTO stock_analysis_upen (ID,NAME,DCFPRICE,CURRENTPRICE,DISCOUNT) \
      VALUES (1, 'GOOG', 3200, 2950, 10)");
    dbase.commit()

def read_Data():
    # from math import *
    data = cursor.execute(''' SELECT * FROM stock_analysis_upen ORDER BY NAME''')
    for record in data:
        print ('ID : '+str(record[0]))
        print ('NAME : '+str(record[1]))
        print ('DCFPRICE : '+str(record[2]))
        print ('CURRENTPRICE : '+str(record[3]))
        print ('DISCOUNT : '+str(record[4])+'\n')

add_Data()
read_Data()

""" def check_Data():
    # from math import *
    data = cursor.execute(''' SELECT NAME FROM stock_analysis_upen WHERE ID =2''')
    x = data.fetchall()
    if x == []:
        print ('Doesnt exist')
    else:
        print (x) """

""" for record in data:
        print ('ID : '+str(record[0]))
        print ('NAME : '+str(record[1]))
        print ('DCFPRICE : '+str(record[2]))
        print ('CURRENTPRICE : '+str(record[3]))
        print ('DISCOUNT : '+str(record[4])+'\n') """


""" check_Data() """

""" def update_record():
    dbase.execute(''' UPDATE stock_analysis_upen set STARS=3 WHERE ID=2 ''')
    dbase.commit()
    print ('Updated') """

dbase.close()
print ('Database Closed')