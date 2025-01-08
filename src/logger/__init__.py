import os

import logging
from logging.handlers import RotatingFileHandler
from from_root import from_root

# make the necessary directories
os.makedirs(from_root('logs'), exist_ok=True)



class LoggerInstance():
    def __init__(self, name: str, level: str, file_path: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # configure formatter and the stream handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_hancdler = logging.StreamHandler()
        console_hancdler.addFilter(formatter)

        # create a file handler
        file_handler = RotatingFileHandler(
            from_root(file_path), 
            mode='a', 
            maxBytes=1e6, 
            backupCount=10
            )
        
        # set the level and formatter for the file handler
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_hancdler)

    def get_logger(self) -> logging.Logger:
        """
        Returns the logger instance."""
        return self.logger


# Logger for the training process
class TrainingLogger(LoggerInstance):
    def __init__(self):
        super().__init__('training_logger', 'DEBUG', 'logs/training.log')


    def get_logger(self) -> logging.Logger:
        return self.logger


# Logger for the deployment process
class DeploymentLogger(LoggerInstance):
    def __init__(self):
        super().__init__('deployment_logger', 'DEBUG', 'logs/deployment.log')


    def get_logger(self) -> logging.Logger:
        return self.logger
    

# logger for general purpose
class GeneralLogger(LoggerInstance):
    def __init__(self):
        super().__init__('general_logger', 'DEBUG', 'logs/general.log')


    def get_logger(self) -> logging.Logger:
        return self.logger
    


# create the logger instances
training_logger = TrainingLogger().get_logger()
deployment_logger = DeploymentLogger().get_logger()
general_logger = GeneralLogger().get_logger()