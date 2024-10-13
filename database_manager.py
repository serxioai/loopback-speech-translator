import os
from pymongo.mongo_client import MongoClient
import logging
from pymongo.errors import ConnectionFailure, ConfigurationError
from dotenv import load_dotenv

DB_PWD = os.environ.get("MONGO_DB_PASSWORD")
DB_URI = os.environ.get("MONGO_DB_URI")
DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")

# Load .env file
load_dotenv()

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, uri=DB_URI, dbname=DATABASE_NAME):
        self.client = None
        self.dbname = dbname
        self.uri = uri

    def connect(self):
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)  # Timeout for initial connection attempt
            self.client.server_info()  # Force a call to check if the connection is successful
            return True
        except ConnectionFailure as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            return False
        except ConfigurationError as e:
            logging.error(f"Configuration error: {e}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return False

    def get_database(self):
        if self.client:
            return self.client[self.dbname]
        return None

    def close_connection(self):
        self.client.close()