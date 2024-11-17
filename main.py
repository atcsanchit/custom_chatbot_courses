#script to execute all the pipelines at once from scratch
import sys
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException

from src.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.pipeline.model_trainer_pipeline import ModelTrainerPipeline


@dataclass
class Pipeline:
    def __init__(self):
        pass

    def execute_pipeline(self):
        try:
            data_ingestion_obj = DataIngestionPipeline()
            data_ingestion_obj.initiate_pipeline()

            data_transformation_obj = DataTransformationPipeline()
            data_transformation_obj.initiate_pipeline()

            training_obj = ModelTrainerPipeline()
            training_obj.initiate_pipeline()

            print("all pipelines are successfully executed")
            logging.info("all pipelines are successfully executed")

        except Exception as e:
            logging.info("Error in execute_pipeline method in main strategy")
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    pipeline_obj = Pipeline()
    pipeline_obj.execute_pipeline()