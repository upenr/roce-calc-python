import yfinance as yf
import sys, logging, traceback
from dotenv import load_dotenv
import requests_cache
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'

load_dotenv()
te = open("yfinance-dcf-output.txt", "a")  # File where I keep the logs

class Unbuffered:
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
        te.write(data)  # Write the data of stdout here to a text file as well

    def flush(self):
        pass

sys.stdout = Unbuffered(sys.stdout)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Upendra: Enter your list of symbols here
mySymbols = ['GOOG']

"""
 msft = yf.Ticker("MSFT")
# get stock info
msft.info """

def upendra_simple_dcf(ticker):
    ticker_data = yf.Ticker(ticker, session=session)
    """ for k, v in ticker_data.financials.items():
        print(k, v) """
    print(ticker_data.financials.get('Income Before Tax'))

for i in range(0, len(mySymbols)):
    try:
        print("%d. %s Yearly:" % (i, mySymbols[i]))
        upendra_simple_dcf(mySymbols[i])

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        traceback.print_exc()
    continue
