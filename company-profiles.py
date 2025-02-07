import sqlite3
import requests
import os
import json
from datetime import datetime
import time
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://financialmodelingprep.com/api/v3/profile/"
API_KEY = os.getenv("MY_VAR_C")

if not API_KEY:
    raise ValueError("API key not found. Please set the MY_VAR_C environment variable.")

conn = sqlite3.connect('stock-dcf-terminal.db')
cursor = conn.cursor()

# Drop the existing table if it exists
cursor.execute('DROP TABLE IF EXISTS company_profiles')

# Create the table with the new column order
cursor.execute('''
CREATE TABLE company_profiles (
    timestamp TEXT,
    symbol TEXT,
    companyName TEXT,
    description TEXT,
    currency TEXT,
    mktCap REAL,
    fullTimeEmployees INTEGER,
    industry TEXT,
    sector TEXT,
    country TEXT,
    state TEXT,
    image TEXT,
    website TEXT,
    exchangeShortName TEXT,
    isAdr INTEGER,
    PRIMARY KEY (timestamp, symbol)
)
''')

with open('mySymbols.txt', 'r') as file:
    content = file.read()
    tickers = [ticker.strip().strip('"') for ticker in content.split(',')]

timestamp = datetime.now().isoformat()

# Variables for rate limiting
start_time = time.time()
request_count = 0

for ticker in tickers:
    # Check if we've made 300 requests
    if request_count >= 300:
        elapsed_time = time.time() - start_time
        if elapsed_time < 60:
            # If less than a minute has passed, sleep for the remaining time
            time.sleep(60 - elapsed_time)
        # Reset the counter and start time
        start_time = time.time()
        request_count = 0

    url = f"{BASE_URL}{ticker}?apikey={API_KEY}"
    response = requests.get(url)
    
    # Increment the request counter
    request_count += 1
    
    print(f"Fetching data for {ticker}. Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            profile = data[0]
            try:
                cursor.execute('''
                INSERT OR REPLACE INTO company_profiles
                (timestamp, symbol, companyName, description, currency, mktCap, 
                 fullTimeEmployees, industry, sector, country, state, image, 
                 website, exchangeShortName, isAdr)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    timestamp,
                    profile['symbol'],
                    profile.get('companyName', ''),
                    profile.get('description', ''),
                    profile.get('currency', ''),
                    profile.get('mktCap', 0),
                    int(profile.get('fullTimeEmployees', '0').replace(',', '')),
                    profile.get('industry', ''),
                    profile.get('sector', ''),
                    profile.get('country', ''),
                    profile.get('state', ''),
                    profile.get('image', ''),
                    profile.get('website', ''),
                    profile.get('exchangeShortName', ''),
                    1 if profile.get('isAdr', False) else 0
                ))
                print(f"Added data for {ticker}")
            except Exception as e:
                print(f"Error inserting data for {ticker}: {str(e)}")
                print(f"Data received: {json.dumps(profile, indent=2)}")
        else:
            print(f"No data found for {ticker}. Response: {json.dumps(data, indent=2)}")
    else:
        print(f"Failed to fetch data for {ticker}. Status code: {response.status_code}")

    # Add a small delay between requests to avoid overwhelming the API
    time.sleep(0.2)  # 200ms delay between requests

conn.commit()
conn.close()

print("Data collection complete.")