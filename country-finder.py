import csv
import requests
import os
from dotenv import load_dotenv
import time
import sqlite3
from datetime import datetime

# Load API key from .env file
load_dotenv()
apikey = os.getenv("MY_VAR_C")

def get_company_country(symbol):
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={apikey}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            return data[0].get('country', 'Unknown')
        else:
            return 'Unknown'
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return 'Error'

def read_tickers_from_csv(filename):
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [ticker.strip() for row in reader for ticker in row]

# Connect to your SQLite database
dbase = sqlite3.connect('stock-dcf-terminal.db')
cursor = dbase.cursor()
print('Database opened')
print('Cursor created')

dbase.execute(''' CREATE TABLE IF NOT EXISTS country_codes(
    DATE TIMESTAMP NOT NULL,
    TICKER TEXT NOT NULL UNIQUE,
    COUNTRY TEXT NULL) ''')

# Read tickers from the CSV file
symbols = read_tickers_from_csv('mySymbols.txt')

print(f"Total symbols read from file: {len(symbols)}")

# Process each symbol
for i, symbol in enumerate(symbols, 1):
    print(f"Processing symbol {i}/{len(symbols)}: {symbol}")
    country = get_company_country(symbol)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert or replace data in the database
    cursor.execute('''
        INSERT OR REPLACE INTO country_codes (DATE, TICKER, COUNTRY)
        VALUES (?, ?, ?)
    ''', (current_date, symbol, country))

    print(f"Ticker: {symbol}, Country: {country}")

    # Commit after each insert to save the data
    dbase.commit()

    # Add a delay to avoid overwhelming the API
    #time.sleep(0.1)

print("Processing complete.")

# Close the database connection
dbase.close()
