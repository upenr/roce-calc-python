import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.93 Safari/537.36"
}

urls = [
    "https://www.dataroma.com/m/g/portfolio.php?pct=2&L=1",
    "https://www.dataroma.com/m/g/portfolio.php?pct=2&L=2",
    "https://www.dataroma.com/m/g/portfolio.php?pct=2&L=3",
    "https://www.dataroma.com/m/g/portfolio.php?pct=2&L=4",
    "https://www.dataroma.com/m/g/portfolio.php?pct=2&L=5",
    "https://www.dataroma.com/m/g/portfolio.php?pct=2&L=6"
]

tickers = set()

for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Debug: print(soup) to check the content
    #print(soup.prettify())

    rows = soup.select("table tr")
    for row in rows:
        cols = row.find_all("td")
        if cols:
            ticker = cols[0].text.strip()
            tickers.add(ticker)

formatted_tickers = ", ".join(f"'{ticker}'" for ticker in sorted(tickers))
print(formatted_tickers)
print (f"Total tickers: {len(tickers)}")
