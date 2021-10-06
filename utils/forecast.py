from data import Stock
from inference import RunInference
import pandas as pd
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA






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
	def __init__(self, stock_id, sentiment, type='close'):

		"""
			Args:

				stock_id (str): Stock symbol of desired stock
				type (str):		Type of stock price to be predicted, options: ['open', 'high', 'low', 'close']

		"""
		self.stockid = stock_id
		self.sentiment = sentiment


		# Lambda functions for formating dataframe containing dates and sentiment for posts and comments
		get_prob = lambda x: float(x[1])
		get_date = lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')


		# Create post and comment dataframes for associated sentiment by date
		post_sentiment = pd.DataFrame({'date': list(map(get_date, self.sentiment['all_post_dates'])), 
										'sentiment': list(map(get_prob, self.sentiment['all_post_probs']))})
		comment_sentiment = pd.DataFrame({'date': list(map(get_date, self.sentiment['all_comment_dates'])), 
											'sentiment': list(map(get_prob, self.sentiment['all_comment_probs']))})


		# Merge into sentiment dataframe
		self.sentiment = pd.concat([post_sentiment, comment_sentiment])

		# Get stock data
		self.start = get_start()
		self.stock = Stock()
		self.stock.set_start(self.start)
		self.stock_data = self.stock.pull_data(stock_id)



	def arima(self):
		"""
			Method to make predictions using ARIMA
		"""


		# drop NAs resulting from lagged values
		#data = self.stock_data.dropna(axis=0)

		mod = ARIMA(endog=self.stock_data.close, exog = self.stock_data.highlow_percent, order=(1, 0, 0))
		res = mod.fit()

		return res














