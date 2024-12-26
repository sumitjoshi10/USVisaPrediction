import os
import sys

from USVisa.logger import logging
from USVisa.exception import CustomeException

from USVisa.constants import TARGET_COLUMN, CURRENT_YEAR, SCHEMA_FILE_PATH
from USVisa.entity.config_entity import DataTransformationConfig
from USVisa.entity.artifact_entity import (DataTransformationArtifact,
                                           DataValidationArtifact,
                                           DataIngestionArtifact)
from USVisa.utils.main_utils import (read_yaml_file,
                                     save_numpy_array_data,
                                     drop_columns,
                                     save_object)
from USVisa.entity.estimator_entity import TargetMapping

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder,OrdinalEncoder,PowerTransformer
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTEENN
from sklearn.impute import SimpleImputer

class DataTransformation:
    def __init__(self,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_ingestaion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomeException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomeException(e, sys)
        
    def get_data_transformer_object(self) -> Pipeline:
        """
        Method Name :   get_data_transformer_object
        Description :   This method creates and returns a data transformer object for the data
        
        Output      :   data transformer object is created and returned 
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info("Entered get_data_transformer_object method of DataTransformation class")
            num_features = self._schema_config["num_features"]
            or_columns = self._schema_config["or_columns"]
            oh_columns = self._schema_config["oh_columns"]
            transform_columns = self._schema_config['transform_columns']
            
            logging.info("Got all cols from schema config")
            
            logging.info(f"One Hot Columns: {oh_columns}") 
            oh_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
            ])
            logging.info("Initialized One Hot Column Pipeline")
            
            logging.info(f"Ordinal Columns: {or_columns}")
            or_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("ordinal_encoder",OrdinalEncoder()),
                ("scaler",StandardScaler(with_mean=False))
            ])
            logging.info("Initialized Ordinal Column Pipeline")
            
            logging.info(f"Power Transform Column: {transform_columns}")
            transform_pipeline = Pipeline(steps=[
                ('transformer', PowerTransformer(method='yeo-johnson'))
            ])
            logging.info("Initialized Power Transform Column Pipeline")
            
            logging.info(f"Numrical Column: {num_features}")
            numerical_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
            ])
            logging.info("Initialized Numerical Column Pipeline")
            
            preprocessor = ColumnTransformer(
                [
                    ("oh_pipeline",oh_pipeline,oh_columns),
                    ("or_pipeline",or_pipeline,or_columns),
                    ("transform_pipeline",transform_pipeline,transform_columns),
                    ("numerical_pipeline",numerical_pipeline,num_features)
                ]
            )
            logging.info("Created preprocessor object from ColumnTransformer")
            
            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )
            return preprocessor
        
        except Exception as e:
            raise CustomeException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Method Name :   initiate_data_transformation
        Description :   This method initiates the data transformation component for the pipeline 
        
        Output      :   data transformer steps are performed and preprocessor object is created  
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting data transformation")
                preprocessor = self.get_data_transformer_object()
                logging.info("Got the preprocessor object")
                
                train_df = DataTransformation.read_data(file_path=self.data_ingestaion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path=self.data_ingestaion_artifact.test_file_path)
                
                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
                
                target_feature_train_df = train_df[TARGET_COLUMN]
                target_feature_test_df = test_df[TARGET_COLUMN]
                
                logging.info("Got train features and test features of Training and Test dataset")
                
                input_feature_train_df['company_age'] = CURRENT_YEAR-input_feature_train_df['yr_of_estab']
                input_feature_test_df['company_age'] = CURRENT_YEAR-input_feature_test_df['yr_of_estab']
                
                logging.info("Added company_age column to the Training and Test dataset")
                
                drop_cols = self._schema_config['drop_columns']
                input_feature_train_df = drop_columns(df=input_feature_train_df, cols = drop_cols)
                input_feature_test_df = drop_columns(df=input_feature_test_df, cols = drop_cols)
                
                logging.info("drop the columns in drop_cols of Training and Test dataset")
                
                target_feature_train_df = target_feature_train_df.replace(
                    TargetMapping()._asdict()
                )
                target_feature_test_df = target_feature_test_df.replace(
                    TargetMapping()._asdict()
                )
                
                logging.info("Target Mapping of Training and Test Target Column")
                
                logging.info("Applying preprocessing object on training dataframe and testing dataframe")
                
                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

                logging.info("Used the preprocessor object to fit transform the train features")

                input_feature_test_arr = preprocessor.transform(input_feature_test_df)

                logging.info("Used the preprocessor object to transform the test features")
                
                logging.info("Applying SMOTEENN on Training dataset")

                smt = SMOTEENN(sampling_strategy="minority")

                input_feature_train_final, target_feature_train_final = smt.fit_resample(
                    input_feature_train_arr, target_feature_train_df
                )

                logging.info("Applied SMOTEENN on training dataset")

                logging.info("Applying SMOTEENN on testing dataset")

                input_feature_test_final, target_feature_test_final = smt.fit_resample(
                    input_feature_test_arr, target_feature_test_df
                )

                logging.info("Applied SMOTEENN on testing dataset")

                logging.info("Created train array and test array")
                
                train_arr = np.c_[
                    input_feature_train_final, np.array(target_feature_train_final)
                ]

                test_arr = np.c_[
                    input_feature_test_final, np.array(target_feature_test_final)
                ]
                
                save_object(file_path= self.data_transformation_config.transformed_object_file_path, obj= preprocessor)
                save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr)
                
                logging.info("Saved the preprocessor object")
                
                logging.info(
                    "Exited initiate_data_transformation method of Data_Transformation class"
                    )

                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )
                return data_transformation_artifact
                
            else:
                raise Exception(self.data_validation_artifact.message)
        except Exception as e:
            raise CustomeException(e, sys)