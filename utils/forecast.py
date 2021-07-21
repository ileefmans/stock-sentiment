from data import Stock
from datetime import datetime






def get_start():
	"""
		Helper function to retrieve the start of the time period from which to gather stock data

	"""
	weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	day = weekdays[datetime.today().weekday()]
	now = datetime.today()
	if day in ['Thursday', 'Friday', 'Saturday']:
		startdt = now-timedelta(days=3)

	elif day in ['Monday', 'Tuesday', 'Wednesday']:
		startdt = now-timedelta(days=5)

	elif day == 'Sunday':
		startdt = now-timedelta(days=4)

	start = [startdt.year, startdt.month, startdt.day, startdt.hour, startdt.minute, startdt.second]

	return start


class Forecast:
	"""
		Class to forecast direction of stock
	"""
	def __init__(self, stock_id, type='close'):

		"""
			Args:

				stock_id (str): Stock symbol of desired stock
				type (str):		Type of stock price to be predicted, options: ['open', 'high', 'low', 'close']

		"""
		self.stockid = stock_id

		self.start = get_start()

		self.stock = Stock()
		self.stock.set_start(self.start)

		self.stock_data = self.stock.pull_data(stock_id)


