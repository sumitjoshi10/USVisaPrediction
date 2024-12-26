from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    '''
    Class Name  :   DataIngestionArtifact
    Description :   This class has all the filepath of the output of the Data Ingestion
    '''
    trained_file_path: str
    test_file_path: str
    
@dataclass
class DataValidationArtifact:
    '''
    Class Name  :   DataValidationArtifact
    Description :   This class has all the filepath of the output of the Data Validation
    '''
    validation_status: bool
    message: str
    drift_report_file_path: str
    
@dataclass
class DataTransformationArtifact:
    '''
    Class Name  :   DataTransformationArtifact
    Description :   This class has all the filepath of the output of the Data Transformation
    '''
    transformed_object_file_path:str 
    transformed_train_file_path:str
    transformed_test_file_path:str
    
@dataclass
class ClassificationMetricArtifact:
    acuracy: float
    f1_score: float
    precision_score: float
    recall_score: float
    
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    metric_artifact: ClassificationMetricArtifact