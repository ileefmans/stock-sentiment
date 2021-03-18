import pymongo
from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017) 

db = client["RedditComments"]

#db["GME"].drop()

print(db.list_collection_names())
print(db['GME'].find_one({'_id':0}))

# count = 0
# for i in cursor:
# 	if count<5:
# 		print(i)
# 	count+=1

