import pymongo
from pymongo import MongoClient

from data import ScrapeWSB
from data import Stock



stock = Stock()
stock.set_start([2020, 4, 8, 0, 0, 0])
stock.set_end([2020, 4, 8, 2, 0, 0])


print(stock.pull_data("AMC"))

# scrapewsb = ScrapeWSB('GME', 10, 10)
# df = scrapewsb.scrape()
# scrapewsb.convert(df)
# print("DONE")





