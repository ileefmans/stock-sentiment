import pymongo
from pymongo import MongoClient




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
		self.db = client["RedditComments"]
		# print list of databases after creation
		# print(client.list_database_names())


	def create_collection(self, name):
		"""
		Args: 

			name (str): Name of collection to be created

		"""
		
		# Create collection
		collection = db[name]
		# Print collections
		print(db.list_collection_names())


		# FOR DELETING COLLECTIONS
		#collection.delete_many({})


	def insert_documents(self, name):


		post = {"post1": ["comment1", "comment2"], "post2": ["comment1", "comment2"]}



		collection.insert_one(post)


		cursor = db["teststock"].find({})

		for i in cursor:
			print(i)


