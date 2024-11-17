import sys
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException
from src.components.prediction import Prediction

@dataclass
class PredictionPipeline:
    def __init__(self):
        pass

    def initiate_pipeline(self,text):
        try:
            # logging.info("Initiating model trainer pipeline")
            # print("Initiating model trainer pipeline")

            prediction_obj = Prediction()
            return prediction_obj.generate_text(text)

            # print("model trainer pipeline has been successfully executed")
            # print("*"*20)        

        except Exception as e:
            logging.info("Error in main method")
            raise CustomException(e,sys)

if __name__ == "__main__":
    pipeline_obj = PredictionPipeline()
    result = pipeline_obj.initiate_pipeline()