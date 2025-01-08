import os

import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger import training_logger
from src.data_access.vehicle_data import VehicleData
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact


class DataIngestion:
    def __init__(self, config: DataIngestionConfig) -> None:
        """
        Initializes the DataIngestion class.
        :param config: The configuration object containing the necessary parameters for data ingestion.
        """
        self.config = config

    def export_data_into_feature_store(self) -> pd.DataFrame:
        """
        Exports data from MongoDB and saves it to a CSV file.
        ----------------------------
        :return: A pandas DataFrame containing the exported data.
        """
        training_logger.info("Exporting data from MongoDB")
        try:
            # load the data from mongoDB
            data = VehicleData()
            vehicle_data = data.get_data(collection_name=self.config.collection_name)
            training_logger.info(f"Data shape: {vehicle_data.shape}")

            # create directory if it does not exist
            feature_store_dir = os.path.dirname(self.config.feature_store_filepath)
            os.makedirs(feature_store_dir, exist_ok=True)

            # return the data
            training_logger.info(f"Exporting data to {self.config.feature_store_filepath}")
            vehicle_data.to_csv(self.config.feature_store_filepath, index=False)

            return vehicle_data
        except Exception as e:
            training_logger.error(f"Error exporting data from MongoDB: {e}")
            raise e

    def split_data(self, dataframe: pd.DataFrame) -> None:
        """
        Splits the data into training and testing sets.
        - param dataframe: The pandas DataFrame containing the data to split.
        ----------------------------
        - return: None"""
        training_logger.info("Splitting data into training and testing sets")
        try:
            train_data, test_data = train_test_split(dataframe,
                                                        test_size=self.config.train_test_split_ratio,
                                                        random_state=42
                                                    )
            training_logger.info(f"Training data shape: {train_data.shape}")
            training_logger.info(f"Testing data shape: {test_data.shape}")

            # create directory for data ingestion if it does not exist
            ingested_dir = os.path.dirname(self.config.train_filepath)
            os.makedirs(ingested_dir, exist_ok=True)

            training_logger.info(f"Exporting training data to {self.config.train_filepath}")
            train_data.to_csv(self.config.train_filepath, index=False)
            test_data.to_csv(self.config.test_filepath, index=False)

            training_logger.info("Data split successfully")
                                                     
        except Exception as e:
            training_logger.error(f"Error splitting data: {e}")
            raise e

    def run(self) -> DataIngestionArtifact:
        """
        Runs the data ingestion process.
        ----------------------------
        : return: A DataIngestionArtifact object containing the file paths of the training and testing data."""
        
        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.config.train_filepath,
                test_file_path=self.config.test_filepath
            )

            return data_ingestion_artifact
        except Exception as e:
            training_logger.error(f"Error running data ingestion: {e}")
            raise e