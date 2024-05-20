import os
import unittest
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

DB_PWD = os.environ.get("MONGO_DB_PASSWORD")
DB_URI = os.environ.get("MONGO_DB_URI")

class TestMongoDBConnection(unittest.TestCase):
    def test_mongo_connection(self):
        """ Test connection to MongoDB Atlas """
        uri = DB_URI
        
        # Replace <password> with the actual password or better yet, use environment variables or a config file to manage it
        # uri = uri.replace('<password>', DB_PWD)
        
        # Create a new client and connect to the server
        client = MongoClient(uri)
        
        try:
            # Send a ping to confirm a successful connection
            client.admin.command('ping')
        except ConnectionFailure as e:
            self.fail(f"MongoDB connection failed: {e}")
        except ConfigurationError as e:
            self.fail(f"Configuration error: {e}")
        except Exception as e:
            self.fail(f"An unexpected error occurred: {e}")
        else:
            print("Pinged your deployment. You successfully connected to MongoDB!")

        # List all the databases in the cluster:
        for db_info in client.list_database_names():
            print(db_info)

if __name__ == '__main__':
    unittest.main()
