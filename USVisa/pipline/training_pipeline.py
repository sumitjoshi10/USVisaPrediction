import sys
from USVisa.exception import CustomeException
from USVisa.logger import logging

from USVisa.components.data_ingestion import DataIngestion
from USVisa.components.data_validation import DataValidation
from USVisa.components.data_transformation import DataTransformation

from USVisa.entity.config_entity import (DataIngestionConfig,
                                         DataValidationConfig,
                                         DataTransformationConfig)

from USVisa.entity.artifact_entity import(DataIngestionArtifact,
                                          DataValidationArtifact,
                                          DataTransformationArtifact)

class TrainingPipeline:
    def __init__(self):
        '''
        This class is responsible for the Training Pipeline to be executed
        '''
        try:
            self.data_ingestion_config = DataIngestionConfig()
            self.data_validation_config = DataValidationConfig()
            self.data_transformation_config = DataTransformationConfig()
        except Exception as e:
            raise CustomeException(e, sys)
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        '''
        This method of TrainPipeline class is responsible for starting data ingestion component
        '''
        try:
            logging.info(f">>>>>>>>>>>>>>>>>>>>>>>>>Data Ingestion Stage<<<<<<<<<<<<<<<<<<<")
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config= self.data_ingestion_config)
            
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set")
            logging.info(f"\n\n\n")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomeException(e, sys)
        
    def start_data_validation(self, data_ingestion_atrifact: DataIngestionArtifact) -> DataValidationArtifact:
        '''
        This method of TrainPipeline class is responsible for starting data validation component
        '''
        try:
            logging.info(f">>>>>>>>>>>>>>>>>>>>>>>>>Data Validation Stage<<<<<<<<<<<<<<<<<<<")
            logging.info("Entered the start_data_validation method of TrainPipeline class")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_atrifact,
                                             data_validation_config=self.data_validation_config)
            
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"\n\n\n")
            return data_validation_artifact
        
        except Exception as e:
            raise CustomeException(e, sys)
        
    def start_data_transformation(self,
                                  data_ingestion_artifact: DataIngestionArtifact,
                                  data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        
        '''
        This method of TrainPipeline class is responsible for starting data transformation component
        '''
        try:
            logging.info(f">>>>>>>>>>>>>>>>>>>>>>>>>Data Transformation Stage<<<<<<<<<<<<<<<<<<<")
            logging.info("Entered the start_data_transformation method of TrainPipeline class")
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"\n\n\n")
            return data_transformation_artifact
            
        except Exception as e:
            raise CustomeException(e, sys)
    def run_pipeline(self) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_atrifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                          data_validation_artifact=data_validation_artifact)
            
        except Exception as e:
            raise CustomeException(e,sys)