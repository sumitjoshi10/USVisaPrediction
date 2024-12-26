import sys

from USVisa.logger import logging
from USVisa.exception import CustomeException

from pandas import DataFrame


class TargetMapping:
    '''
    class Name  :   TargetMapping
    Desc        :   Mapping the Catergorical Target Column to Numberical Target Column
    '''
    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1
    
    def _asdict(self):
        try:
            return self.__dict__
        except Exception as e:
            raise CustomeException(e, sys)
    
    def reverse_mapping(self):
        try: 
            mapping_response = self._asdict()
            return dict(zip(mapping_response.values(),mapping_response.keys()))
        except Exception as e:
            raise CustomeException(e, sys)