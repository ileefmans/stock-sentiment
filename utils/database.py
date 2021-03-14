from pymongo import MongoClient

# Create and connect to client
client = MongoClient()
client = MongoClient(host="localhost", port=27017) 

# Create database
db = client["RedditComments"]

# Create Admin User for Database
db.createUser({
	user: "Ian" 
	pwd: "12345"
	roles: ["readWrite", "dbAdmin"]
	}
	)


