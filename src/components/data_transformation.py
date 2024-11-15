import sys
import os
import pandas as pd
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException


@dataclass
class DataTranformationConfig:
    data_path = os.path.join("artifacts", "data_ingestion", "wechatbot.csv")
    transformation_path = os.path.join("artifacts","data_transformation")

class DataTransformation:
    def __init__(self):
        self.data_transformation = DataTranformationConfig()
    
    def load_dataframe(self):
        try:
            self.df = pd.read_csv(self.data_transformation.data_path)
            self.transformed_df = pd.DataFrame(columns=["input","output"])            

        except Exception as e:
            logging.info("Error in load_dataframe")
            raise CustomException(e,sys)
        
    def save_csv(self, dataframe, location, filename):
        try:
            if not os.path.exists(location):
                os.makedirs(location, exist_ok=True)

            dataframe.to_csv(os.path.join(location, (filename + ".csv")), index=False)

        except Exception as e:
            logging.info("Error in save_csv")
            raise CustomException(e,sys)

    def direct_question(self):
        try:
            for index, row in self.df.iterrows():
                input_output_dict = {}
                list_of_topics = ["description", "session price", "lessons", "duration", "price"]
                
                for topic_index, topic in enumerate(list_of_topics):
                    question = "what is the {flag1} of the course {flag2}".format(flag1 = topic, flag2 = row[0])        
                    answer = "the {flag1} is: {flag2}".format(flag1 = topic, flag2 = row[topic_index + 1])
                    input_output_dict["input"] = question
                    input_output_dict["output"] = answer
                    new_row = pd.DataFrame([input_output_dict])  # Create DataFrame from dict
                    self.transformed_df = pd.concat([self.transformed_df, new_row], ignore_index=True)
                    
            self.save_csv(dataframe=self.transformed_df, location=self.data_transformation.transformation_path, filename="transformed")
        
        except Exception as e:
            logging.info("Error in direct_question")
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self):
        try:
            self.load_dataframe()
            self.direct_question()
        
        except Exception as e:
            logging.info("Error in initiate_data_transformation")
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    data_transformation_obj = DataTransformation()
    data_transformation_obj.initiate_data_transformation()