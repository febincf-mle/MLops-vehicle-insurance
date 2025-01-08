import os
from dataclasses import dataclass


from src.constants import *


@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR_NAME) # /artifact/data_ingestion
    feature_store_filepath: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    train_filepath: str = os.path.join(data_ingestion_dir, DATA_INGESTION_DIR_NAME, TRAIN_FILE_NAME)
    test_filepath: str = os.path.join(data_ingestion_dir, DATA_INGESTION_DIR_NAME, TEST_FILE_NAME)
    train_test_split_ratio = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name = DATA_INGESTION_COLLECTION_NAME