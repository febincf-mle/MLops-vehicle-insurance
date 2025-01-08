from src.components.data_ingestion import DataIngestion
from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.logger import training_logger


class TrainingPipeline:
    def __init__(self):
        """
        Initializes the TrainingPipeline class."""
        self.data_ingestion_config = DataIngestionConfig()


    def run_data_ingestion(self) -> DataIngestionArtifact:
        """
        Runs the data ingestion process.
        ----------------------------
        : return: The artifact containing the data ingestion results."""
        try:
            data_ingestion = DataIngestion(config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.run()
            return data_ingestion_artifact
        except Exception as e:
            training_logger.error(f"Error running data ingestion: {e}")
            raise e