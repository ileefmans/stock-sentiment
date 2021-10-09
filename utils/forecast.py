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
		# Convert date clumn to datetime
		self.sentiment['date'] = pd.to_datetime(self.sentiment['date'])
		self.sentiment.sort_values(by=['date'], inplace=True)
		self.sentiment.reset_index(inplace=True)
		self.sentiment.drop(columns=['index'], inplace=True)
		self.sentiment = self.sentiment.groupby(['date']).mean()
		self.sentiment.reset_index(inplace=True)

		# Get stock data
		self.start = get_start()
		self.stock = Stock()
		self.stock.set_start(self.start)
		# Pull Data
		self.stock_data = self.stock.pull_data(stock_id)
		# Convert timestamp to datetime in dataframe
		self.stock_data['timestamp'] = pd.to_datetime(self.stock_data.timestamp)

	def assign_sentiment(self):
		"""
			Method to match sentiment with stock prices
		"""

		# Initialize target array
		target = []

		# Initialize index of sentiment dataframe
		j = 0
		# Iterate over all stock prices to assign sentiment
		for i in range(len(self.stock_data)):
			

			# Search for closest date in sentiment dataframe
			searching = True
			while searching:

				# Ensure no index out of range error
				if j != (len(self.sentiment)-1):

					# Increase index until closest date is found and assign corresponding sentiment
					if abs((self.stock_data.iloc[i].timestamp - self.sentiment.iloc[j].date).total_seconds()) <= abs((self.stock_data.iloc[i].timestamp - self.sentiment.iloc[j+1].date).total_seconds()):
						target.append(self.sentiment.iloc[j].sentiment)
						searching = False
					else:
						#target.append(self.sentiment.iloc[j+1].sentiment)
						j+=1

				# if last date in sentiment dataframe is reached this is the closest date
				else:
					target.append(self.sentiment.iloc[j].sentiment)	
					searching=False

		# Add new column to stock price dataframe
		self.stock_data['sentiment'] = target

		return





	def arima(self):
		"""
			Method to make predictions using ARIMA
		"""


		# drop NAs resulting from lagged values
		#data = self.stock_data.dropna(axis=0)

		# Retrieve associated sentiment for stock prices
		self.assign_sentiment()

		mod = ARIMA(endog=self.stock_data.close, exog = self.stock_data.highlow_percent, order=(1, 0, 0))
		res = mod.fit()

		return res














