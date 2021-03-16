import pymongo
from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017) 

db = client["RedditComments"]

# db["stock=GME"].drop()

print(db.list_collection_names())