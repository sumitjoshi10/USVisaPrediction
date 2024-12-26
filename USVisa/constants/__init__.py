import os
from datetime import date

from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")

COLLECTION_NAME = os.getenv("COLLECTION_NAME")

MONGODB_URL_KEY = os.getenv("MONGODB_URL")

PIPELINE_NAME: str = "USVisa"
ARTIFACT_DIR: str = "artifact"

FILE_NAME = "usvisa.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year

SCHEMA_FILE_PATH = os.path.join("config","schema.yaml")

PREPROCESSING_OBJECT_FILE_NAME = "preprocessor.pkl"

'''
Data Ingestion related constant start with DATA_INGESTION VAR NAME
'''
DATA_INGESTION_COLLECTION_NAME: str = COLLECTION_NAME
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

'''
Data Validation related constant start with DATA_VALIDATION VAR NAME
'''
DATA_VALIDAION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

'''
Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME
'''
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "tranformed_object"

'''
Model Trainer related constant start with MODEL_TRAINER VAR NAME
'''
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINER_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_CONFIG_FILE_PATH: str = os.path.join("config","model.yaml")