import pymongo
from pymongo import MongoClient
import argparse
from scrape import GetData


def get_args():
    parser = argparse.ArgumentParser(description="Model Options")
    parser.add_argument("stock", type=str, help="stock searched and added to database")
    return parser.parse_args()


class Database:
	"""
		MongoDB database
	"""

	def __init__(self, name):
		"""
			Args:

				name (str): Name of database
		"""

		# Connect to client
		self.client = MongoClient(host="localhost", port=27017) 

		# Create database
		self.db = self.client["RedditComments"]
		# print list of databases after creation
		# print(client.list_database_names())


	def create_collection(self, name):
		"""
		Args: 

			name (str): Name of collection to be created

		"""
		
		# Create collection
		collection = self.db[name]
		# Print collections
		print(self.db.list_collection_names())


		# FOR DELETING COLLECTIONS
		#collection.delete_many({})


	def insert_document(self, collection_name, name, post):

		self.db[collection_name].insert_one(post)


		# cursor = db["teststock"].find({})

		# for i in cursor:
		# 	print(i)


if __name__ == "__main__":
	ops = get_args()
	name = ops.stock

	database = Database("RedditComments")
	print("DONE INSTATNIATING DATABASE")
	database.create_collection(name)
	print("DONE CREATING COLLECTION")
	getdata = GetData(name)
	database.insert_document(name, "posts",getdata.process())





	cursor = database.db[name].find({})

	count = 0
	for i in cursor:
		if count<10:
			print(i)
		count+=1





