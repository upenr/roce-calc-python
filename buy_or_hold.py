import sys
from datetime import datetime

sys.path.append('../')
from stock_candle import StockCandle

# Experiment Parameters
nifty_olhc_filename = "../Data/Index/NIFTY 50_OLHC_DAILY_01011999_01012020.csv"
monthly_cash_increment = 1000
percentage_from_all_time_high = 10

"""
This method reads the NIFTY OLHC data from a csv file.
Please note that the data is originally sorted by date in descending order.
"""
def readNiftyCandles(reverse_candles=False):
	file = open(nifty_olhc_filename, "r")
	candles = []

	# The first line in the csv is the header, so we need to skip that.
	first_line_skipped = False
	for line in file:
		if not first_line_skipped:
			first_line_skipped = True
			continue

		# The rows have data in the format Date, Open, High, Low, Close
		row_splits = line.split(",")

		date = datetime.strptime(row_splits[0], "%d %b %Y")
		candle = StockCandle("NIFTY50",
			date,
			float(row_splits[1]),
			float(row_splits[3]),
			float(row_splits[2]),
			float(row_splits[4]))
		candles.append(candle)

	if reverse_candles:
		candles.reverse()

	return candles

"""
This method populates all time high in candles.
NOTE: This method assumes that candles are sorted in chronological order, i.e. oldest candle comes first.
"""
def populateAllTimeHighs(candles):
	all_time_high = 0
	for candle in candles:
		all_time_high = max(all_time_high, candle.close)
		candle.all_time_high = all_time_high
	return candles

candles = populateAllTimeHighs(readNiftyCandles(True))


def hasMonthChanged(previous_date, current_date):
	if previous_date.month < current_date.month:
		return True

	if previous_date.year < current_date.year:
		return True

	return False


def runExperiment(candles, buyCandle):
	# Setting up initialization parameters.
	cash = 0
	units_held = 0
	previous_date = datetime.strptime("31 Dec 1998", "%d %b %Y")
	current_value = 0
	max_cash_held = 0
	max_cash_held_buy_date = None

	for candle in candles:
		# Add to cash account on beginning of the month.
		if hasMonthChanged(previous_date, candle.date):
			cash += monthly_cash_increment

		units_to_buy = buyCandle(candle, cash)
		if units_to_buy > 0:
			if cash > max_cash_held:
				max_cash_held = cash
				max_cash_held_buy_date = candle.date

			units_held += units_to_buy
			cash -= units_to_buy*candle.close

		current_value = cash + units_held*candle.close
		previous_date = candle.date

	print ("Cash to begin with: 0")
	print ("Monthly cash increment: 1000")
	print ("Final holding value: " + str(current_value))
	print ("Max cash held at one point: " + str(max_cash_held))
	print ("Max cash held buy date: " + max_cash_held_buy_date.__str__())


def buyCandleAsSoonAsYouHaveCash(candle, cash):
	units_to_buy = round(cash/candle.close, 2)

	# Taking care of rounding up errors
	if(units_to_buy*candle.close > cash):
		units_to_buy -= 0.01

	return units_to_buy


def buyOnFallFromAllTimeHigh(candle, cash):
	fall_percentage = ((candle.all_time_high - candle.close)/candle.all_time_high)*100;
	if fall_percentage < percentage_from_all_time_high:
		return 0

	return buyCandleAsSoonAsYouHaveCash(candle, cash)


print ("Running strategy: BuyAsSoonAsYouHaveCash")
runExperiment(candles, buyCandleAsSoonAsYouHaveCash)
print ("")

print ("Running strategy: BuyOnFallFromAllTimeHigh")
print ("Fall Percentage: " + str(percentage_from_all_time_high) + "%")
runExperiment(candles, buyOnFallFromAllTimeHigh)
