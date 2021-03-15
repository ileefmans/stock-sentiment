import finnhub
import yaml
import pandas as pd
import datetime



# Extract IDs from yaml file
with open("IDs.yml") as file:
			IDs = yaml.load(file, Loader=yaml.FullLoader)
api_key = IDs["Finnhub"]["api_key"]

# Set up client
finnhub_client = finnhub.Client(api_key=api_key)

res = finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249)
df = pd.DataFrame(res)
df['t'] = list(map(lambda x: datetime.datetime.fromtimestamp(int(str(x))).strftime('%Y-%m-%d %H:%M:%S'), df.t))

print(df)
