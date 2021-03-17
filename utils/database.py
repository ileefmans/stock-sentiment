import pymongo
from pymongo import MongoClient
import argparse
import yaml
from data import ScrapeWSB, Stock


def get_args():
    parser = argparse.ArgumentParser(description="Model Options")
    parser.add_argument("stock_name", type=str, help="stock searched and added to database")
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

	# Get name from argument parser
	ops = get_args()
	name = ops.stock_name
	# client_id = ops.client_id
	# client_secret = ops.client_secret

	# Instantiate Database object
	database = Database("RedditComments")
	# Create a collection for desired stock
	database.create_collection(name)
	# Instantiate object to scrape Reddit for desired stock
	scrapewsb = ScrapeWSB(name, 10, 10)
	



	# Insert data into database
	post = scrapewsb.process()
	

	for doc in post:

		database.insert_document(name, "posts", doc)
	


	# Printing for testing purposes only
	cursor = database.db[name].find({})
	
	count = 0
	for i in cursor:
		if count<1:
			print(i)
		count+=1





