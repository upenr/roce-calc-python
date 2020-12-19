import requests
import re
from lxml import html

ticker = input("Enter your stock ticker: ")

url = "https://finance.yahoo.com/quote/{}/balance-sheet?p={}".format(ticker, ticker)
url2 = "https://finance.yahoo.com/quote/{}/financials?p={}".format(ticker, ticker)

page = requests.get(url)
page2 = requests.get(url2)

tree = html.fromstring(page.content)
tree2 = html.fromstring(page2.content)

total_assets = []
Total_Current_Liabilities = []
Operating_Income_or_Loss = []

path = '//div[@class="rw-expnded"][@data-test="fin-row"][@data-reactid]'
data_path = "../../div/span/text()"

dats = [tree.xpath(path), tree2.xpath(path)]

for entry in dats:
    for d in entry[0]:
        for s in d.xpath("//div[@title]"):
            if s.attrib["title"] == "Total Assets":
                total_assets.append(s.xpath(data_path))
            if s.attrib["title"] == "Total Current Liabilities":
                Total_Current_Liabilities.append(s.xpath(data_path))
            if s.attrib["title"] == "Operating Income or Loss":
                Operating_Income_or_Loss.append(s.xpath(data_path))

del total_assets[0]
del Total_Current_Liabilities[0]
del Operating_Income_or_Loss[0]

for i in range(0, len(total_assets[0])):
    # print (float(re.sub("[^\d\.]", "", total_assets[0][i])))
    roce = (
        100
        * float(re.sub("[^\d\.]", "", Operating_Income_or_Loss[0][i + 1]))
        / (
            float((re.sub("[^\d\.]", "", total_assets[0][i])))
            - float((re.sub("[^\d\.]", "", Total_Current_Liabilities[0][i])))
        )
    )
    print(f"ROCE is {roce:.2f} %")

print(total_assets[0])
print(Total_Current_Liabilities[0])
print(Operating_Income_or_Loss[0])
