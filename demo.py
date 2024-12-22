from USVisa.logger import logging
from USVisa.exception import CustomeException
import sys

try:
   a = 2/0
except Exception as e:
    raise CustomeException(e,sys)
    