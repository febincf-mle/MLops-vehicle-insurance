import os
import sys
import certifi
import pymongo


from src.constants import DATABASE_NAME, MONGO_DB_URI_KEY
from src.logger import general_logger
from src.exception import CustomException

ca = certifi.where()

class MongoDBClient:

    client = None # client shared across all instances of the class

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initializes the MongoDB client and connects to the specified database.

        :param database_name: The name of the database to connect to."""
        
        try:
            general_logger.info("Connecting to MongoDB database")
            # check if the client is already connected
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv("MONGO_DB_URI_KEY")
                if mongo_db_url is None:
                    raise KeyError("MongoDB URI not found in environment variables.")
                
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

            # connect to the database
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

            general_logger.info(f"Connected to MongoDB database: {database_name}")
        except Exception as e:
            raise CustomException(e, sys) from e