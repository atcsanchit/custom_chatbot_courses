import sys
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException
from src.components.model_trainer import ModelTrainer


@dataclass
class ModelTrainerPipeline:
    def __init__(self):
        pass

    def initiate_pipeline(self):
        try:
            logging.info("Initiating model trainer pipeline")
            print("Initiating model trainer pipeline")

            model_trainer_obj = ModelTrainer()
            model_trainer_obj.initiate_training()

            print("model trainer pipeline has been successfully executed")
            print("*"*20)        

        except Exception as e:
            logging.info("Error in main method")
            raise CustomException(e,sys)

if __name__ == "__main__":
    pipeline_obj = ModelTrainerPipeline()
    pipeline_obj.initiate_pipeline()