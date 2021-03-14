import pymongo
from pymongo import MongoClient

# Create and connect to client
client = MongoClient()
client = MongoClient(host="localhost", port=27017) 



# Create database
db = client["RedditComments"]
#print collections
print(client.list_database_names())



# Create collection
collection = db["teststock"]
# Print collections
print(db.list_collection_names())





post = {"post1": ["comment1", "comment2"], "post2": ["comment1", "comment2"]}



collection.insert_one(post)


cursor = db["teststock"].find({})

for i in cursor:
	print(i)


