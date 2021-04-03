# My Python scripts to extract stock values from Financial Modeling Prep and other sources 🔍

These are value investing related Python scripts I wrote to search and filter for stock-related metrics I like.

## Working Python scripts relying on Financial Modeling Prep 

- `upendra-screen` - My screen based on Professor Kenneth Jeffrey Marshall's book [Good Stocks Cheap](https://www.amazon.com/Good-Stocks-Cheap-Confidence-Outperformance/dp/125983607X)
- `fprep-basic` - Get started by making a basic call, view the output and extract a value you like
- `fprep-roce_best` - Calculations for getting Return on Capital Employed (ROCE) of any company that meets a threshold along with other metrics like average ROCE over the years and my magic number to compute ROCE growth, with output sorted in descending order
- `fprep-52week-low` - Identifies companies that are close to their 52 week lows, meeting a threshold, with output sorted from closest to low
- `fprep-dcf-discount` - Identifies companies that are trading at a discount compared to their DCF-based intrinsic value, with output sorted in descending order
- `list-of-companies` - Gets a list of companies that are available with Financial Modeling Prep

## Buy or Hold Strategy

- `buy_or_hold` - This Python script analyzes S&P 500 data from 1999 to early 2020 (supplied as a CSV file) and figures out if buying after a threshold (%) drop in the markets is better or if dollar cost averaging is better.

## Other Methods from Aug, 2019 (may be obsolete now):

- Scraping Yahoo Finance with LXML (I have a working, published Android app on this if you're interested: https://play.google.com/store/apps/details?id=com.upen.rocecalculator)
- Scraping Yahoo Finance with Beautiful Soup

## Running Locally 💻

- Clone this project, then run the Python scripts using the `python` command.

## Built using 🧰

- [Python](https://python.org/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [LXML](https://lxml.de)
- Data from [Financial Modeling Prep](https://financialmodelingprep.com) and [Yahoo Finance](https://finance.yahoo.com)
