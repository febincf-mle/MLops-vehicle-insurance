import os
import sys

from src.pipline.training_pipeline import TrainingPipeline

from src.logger import training_logger
from src.exception import CustomException


training_pipeline = TrainingPipeline()
training_pipeline.run_data_ingestion()