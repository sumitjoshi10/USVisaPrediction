import sys
import os

from USVisa.logger import logging
from USVisa.exception import CustomeException
from USVisa.constants import DATABASE_NAME, MONGODB_URL_KEY

import pymongo
import certifi

ca = certifi.where()

class MongoDBClient:
    '''
    class Name  :   MongoDBClient
    description :   Will Connect to the Mongo DB Database
    
    Output      :   connection to mongodb database
    On Failure  :   raises an exception
    '''
    
    client = None
    
    def __init__(self, database_name = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = MONGODB_URL_KEY
                if mongo_db_url is None:
                    raise Exception(f"Environment key : {MONGODB_URL_KEY} is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAfile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful")
        except Exception as e:
            raise CustomeException(e, sys)
