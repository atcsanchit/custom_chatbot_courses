import sys
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation


@dataclass
class DataIngestionPipeline:
    def __init__(self):
        pass

    def initiate_pipeline(self):
        try:
            logging.info("Initiating data ingestion pipeline")
            print("Initiating data ingestion pipeline")

            data_ingestion_obj = DataIngestion()
            data_ingestion_obj.initiate_data_ingestion()  

            data_validation_obj = DataValidation()
            data_validation_obj.validate_all_file_exist()

            print("data ingestion pipeline has been successfully executed")
            print("*"*20)        

        except Exception as e:
            logging.info("Error in main method")
            raise CustomException(e,sys)

if __name__ == "__main__":
    pipeline_obj = DataIngestionPipeline()
    pipeline_obj.initiate_pipeline()