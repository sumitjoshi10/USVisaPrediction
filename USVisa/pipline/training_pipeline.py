import sys
from USVisa.exception import CustomeException
from USVisa.logger import logging

from USVisa.components.data_ingestion import DataIngestion

from USVisa.entity.config_entity import DataIngestionConfig

from USVisa.entity.artifact_entity import DataIngestionArtifact

class TrainingPipeline:
    def __init__(self):
        '''
        This class is responsible for the Training Pipeline to be executed
        '''
        try:
            self.data_ingestion_config = DataIngestionConfig()
        except Exception as e:
            raise CustomeException(e, sys)
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        '''
        This method of TrainPipeline class is responsible for starting data ingestion component
        '''
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config= self.data_ingestion_config)
            
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            
            return data_ingestion_artifact
        except Exception as e:
            raise CustomeException(e, sys)
        
    def run_pipeline(self) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise CustomeException(e,sys)