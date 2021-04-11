import pymongo
from pymongo import MongoClient

from data import ScrapeWSB



# stock = Stock()
# stock.set_start([2020, 4, 8, 0, 0, 0])
# stock.set_end([2020, 4, 8, 2, 0, 0])


# print(stock.pull_data("AMC"))

scrapewsb = ScrapeWSB('GME', 10, 10)
print(scrapewsb.process()[0].keys())





#####################################################################################

# client = MongoClient(host="localhost", port=27017) 

# db = client["RedditComments"]

# #db["GME"].drop()

# print(db.list_collection_names())
# print(db['GME'].find_one({'_id':0}))

# count = 0
# for i in cursor:
# 	if count<5:
# 		print(i)
# 	count+=1

