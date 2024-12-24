from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    '''
    Class Name  :   DataIngestionArtifact
    Description :   This class has all the filepath of the output of the Data Ingestion
    '''
    trained_file_path: str
    test_file_path: str
    