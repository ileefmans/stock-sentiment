import finnhub
import yaml
import pandas as pd
import datetime
import time



# Extract IDs from yaml file
with open("IDs.yml") as file:
			IDs = yaml.load(file, Loader=yaml.FullLoader)
api_key = IDs["Finnhub"]["api_key"]

# Set up client
finnhub_client = finnhub.Client(api_key=api_key)


# Create unix timestamp
def create_unix_stamp(year, month, day, hour, minute, second):
	dt = datetime.datetime(year, month, day, hour, minute, second)
	return int(time.mktime(dt.timetuple()))

start = create_unix_stamp(2021, 3, 15, 0, 0, 0)
end = int(time.time())

res = finnhub_client.stock_candles('AAPL', '1', start, end)
df = pd.DataFrame(res)
df['t'] = list(map(lambda x: datetime.datetime.fromtimestamp(int(str(x))).strftime('%Y-%m-%d %H:%M:%S'), df.t))

print(df)

