import sys
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DataTransformation


@dataclass
class DataTransformationPipeline:
    def __init__(self):
        pass

    def initiate_pipeline(self):
        try:
            logging.info("Initiating data transformation pipeline")
            print("Initiating data transformation pipeline")

            data_transformation_obj = DataTransformation()
            data_transformation_obj.initiate_data_transformation()

            print("data transformation pipeline has been successfully executed")
            print("*"*20)        

        except Exception as e:
            logging.info("Error in main method")
            raise CustomException(e,sys)

if __name__ == "__main__":
    pipeline_obj = DataTransformationPipeline()
    pipeline_obj.initiate_pipeline()