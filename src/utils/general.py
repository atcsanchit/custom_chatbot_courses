import sys
import os

from src.logger import logging
from src.exception import CustomException

def save_csv(dataframe, location, filename):
    try:
        if not os.path.exists(location):
            os.makedirs(location, exist_ok=True)

        dataframe.to_csv(os.path.join(location, filename + ".csv"), index=False)

    except Exception as e:
        logging.info("Error in save_csv utils")
        raise CustomException(e,sys)    
