import finnhub
import yaml
import pandas as pd
import datetime
import time




class Stock:
	def __init__(self):


		# Extract IDs from yaml file
		with open("IDs.yml") as file:
					self.IDs = yaml.load(file, Loader=yaml.FullLoader)
		self.api_key = IDs["Finnhub"]["api_key"]

		# Set up client
		self.finnhub_client = finnhub.Client(api_key=api_key)
		self.start = int(time.mktime((datetime.datetime.now()- datetime.timedelta(days=1)).timetuple()))
		self.end = int(time.time())


	def set_start(self, date):
		self.start = self.create_unix_stamp(date[0], date[1], date[2], date[3], date[4], date[5])

	def set_end(self, current=True, date=None):
		if current:
			self.end = int(time.time())
		else:
			self.end = self.create_unix_stamp(date[0], date[1], date[2], date[3], date[4], date[5])


	# Create unix timestamp
	def create_unix_stamp(self, year, month, day hour minute, second):
		dt = datetime.datetime(year, month, day, hour, minute, second)
		return int(time.mktime(dt.timetuple()))


	def pull_data(self):
		start = create_unix_stamp(2021, 3, 15, 0, 0, 0)
		end = int(time.time())

		res = self.finnhub_client.stock_candles('AAPL', '1', start, end)
		df = pd.DataFrame(res)
		df['t'] = list(map(lambda x: datetime.datetime.fromtimestamp(int(str(x))).strftime('%Y-%m-%d %H:%M:%S'), df.t))

		print(df)

