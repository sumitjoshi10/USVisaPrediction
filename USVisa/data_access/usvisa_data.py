from USVisa.configuration.mongo_db_connector import MongoDBClient
from USVisa.constants import DATABASE_NAME
from USVisa.exception import CustomeException
import pandas as pd
import sys
from typing import Optional
import numpy as np
from dotenv import load_dotenv


class USvisaData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise CustomeException(e,sys)
        

    def export_collection_as_dataframe(self,collection_name:str,database_name:Optional[str]=None)->pd.DataFrame:
        '''
        Method Name :   eexport_collection_as_dataframe
        Description :   This method converts the collection to dataframe
        
        Output      :   Dataframe
        On Failure  :   Raise an Exception
        '''
        try:
          
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise CustomeException(e,sys)