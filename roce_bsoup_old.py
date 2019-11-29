import requests
from datetime import datetime
from bs4 import BeautifulSoup

operating_income_or_loss_keys = []
operating_income_or_loss_values = []
year = input("Enter your year: ")

def get_operating_income_or_loss(soup):
  for rows in soup.find_all('div', {'class': 'D(tbr)'}):
    for date_row in rows.find_all('div', {'class': 'D(ib)'}):
        if date_row.text == 'Breakdown':
            chart_dates = date_row.find_all_next('span', limit=5)
            for dates in chart_dates[2:]:
                reformatted_date = datetime.strptime(dates.text, '%m/%d/%Y').strftime('%m%d%Y')
                operating_income_or_loss_keys.append(reformatted_date)

    for sub_row in rows.find_all('div', {'class': 'D(tbc)'}):
        for row_item in sub_row.find_all('span', {'class': 'Va(m)'}):
            if row_item.text == 'Operating Income or Loss':
                operating_income_or_loss = row_item.find_all_next('span', limit=4)
                for item in operating_income_or_loss[1:]:
                    operating_income_or_loss_values.append(item.text)
  return
total_assets_values = []
total_current_liabilities = []
balance_sheet_keys = []

def get_total_assets(soup):
  for rows in soup.find_all('div', {'class': 'D(tbr)'}):
    for date_row in rows.find_all('div', {'class': 'D(ib)'}):
        if date_row.text == 'Breakdown':
            chart_dates = date_row.find_all_next('span', limit=4)
            for dates in chart_dates[1:]:
                print (dates)
                reformatted_date = datetime.strptime(dates.text, '%m/%d/%Y').strftime('%m%d%Y')
                balance_sheet_keys.append(reformatted_date)

  for rows in soup.find_all('div', {'class': 'D(tbr)'}):
    for sub_row in rows.find_all('div', {'class': 'D(tbc)'}):
        for row_item in sub_row.find_all('span', {'class': 'Va(m)'}):
                if row_item.text == 'Total Assets':
                    total_assets = row_item.find_all_next('span', limit=3)
                    for item in total_assets:
                        total_assets_values.append(item.text)
  return
def get_total_current_liabilities(soup):
  for rows in soup.find_all('div', {'class': 'D(tbr)'}):
    for sub_row in rows.find_all('div', {'class': 'D(tbc)'}):
        for row_item in sub_row.find_all('span', {'class': 'Va(m)'}):
            if row_item.text == 'Total Current Liabilities':
                current_liabilities = row_item.find_all_next('span', limit=3)
                for item in current_liabilities:
                    total_current_liabilities.append(item.text)
  return
urls = ['https://finance.yahoo.com/quote/AAPL/balance-sheet?p=AAPL', 'https://finance.yahoo.com/quote/AAPL/financials?p=AAPL']

for url in urls:
  if 'balance-sheet' in url:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    get_total_assets(soup)
    get_total_current_liabilities(soup)
    balance_sheet_dict = {k: v for k, v in zip(balance_sheet_keys, zip(total_assets_values,total_current_liabilities))}
    print (balance_sheet_dict)
    # output{'09292018': ('365,725,000', '116,866,000'), '09292017': ('375,319,000', '100,814,000'), '09292016': ('321,686,000', '79,006,000')}

  elif 'financials' in url:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    get_operating_income_or_loss(soup)
    financials_dict = {k: v for k, v in zip(operating_income_or_loss_keys, operating_income_or_loss_values)}
    print (financials_dict)
    # output{'09292018': '70,898,000', '09292017': '61,344,000', '09292016': '60,024,000'}

for key, values in balance_sheet_dict.items():
  if key.endswith('{}'.format(year)):
   total_asset = values[0]
   current_liabilities = values[1]
   balance_sheet_keys = values [0]
   print (f'Year: {key}, Total assets: {total_asset}, Total current liabilities: {current_liabilities}, Operating Income or Loss: {balance_sheet_keys}')
   # output Year: 09292016, Total assets: 321,686,000, Total current liabilities: 79,006,000
