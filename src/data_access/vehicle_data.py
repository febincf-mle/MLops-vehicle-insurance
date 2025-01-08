import numpy as np
import pandas as pd

from typing import Optional

from src.constants import DATABASE_NAME
from src.configuration.mongo_db_connection import MongoDBClient



class VehicleData:

    def __init__(self):
        self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

    def get_data(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Retrieves data from the MongoDB database and returns it as a pandas DataFrame.

        :param collection_name: The name of the collection to retrieve data from.
        :param database_name: The name of the database to retrieve data from.
        :return: A pandas DataFrame containing the retrieved data.
        """
        if database_name is None:
            database_name = DATABASE_NAME

        collection = self.mongo_client.client[database_name][collection_name]
        cursor = collection.find()

        df = pd.DataFrame(list(cursor))

        # drop id column from the dataframe
        if 'id' in df.columns.to_list():
            df.drop(columns=['id'], axis=1, inplace=True)

        # replace na values using np.nan
        df.replace({"na": np.nan}, inplace=True)
        return df