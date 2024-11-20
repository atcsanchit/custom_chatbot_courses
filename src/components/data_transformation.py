import sys
import os
import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import T5Tokenizer, T5ForConditionalGeneration
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException


@dataclass
class DataTranformationConfig:
    data_path = os.path.join("artifacts", "data_ingestion", "wechatbot.csv")
    transformation_path = os.path.join("artifacts","data_transformation")
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")

class DataTransformation:
    def __init__(self):
        self.data_transformation = DataTranformationConfig()
        self.list_of_topics = ["description", "session price", "lessons", "duration", "price"]
    
    def load_dataframe(self):
        try:
            self.df = pd.read_csv(self.data_transformation.data_path)
            self.transformed_df = pd.DataFrame(columns=["input","output"])       
            self.rag_transformed_df = pd.DataFrame(columns=["input"])

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
                # list_of_topics = ["description", "session price", "lessons", "duration", "price"]
                
                for topic_index, topic in enumerate(self.list_of_topics):
                    question = "what is the {flag1} of the course {flag2}".format(flag1 = topic, flag2 = row[0])        
                    answer = "the {flag1} is: {flag2}".format(flag1 = topic, flag2 = row[topic_index + 1])
                    input_output_dict["input"] = question
                    input_output_dict["output"] = answer
                    new_row = pd.DataFrame([input_output_dict])  
                    self.transformed_df = pd.concat([self.transformed_df, new_row], ignore_index=True)
                    
            self.save_csv(dataframe=self.transformed_df, location=self.data_transformation.transformation_path, filename="transformed")
        
        except Exception as e:
            logging.info("Error in direct_question")
            raise CustomException(e,sys)
    
    def rag_preprocessing(self):
        try:
            for index, row in self.df.iterrows():
                input_output_dict = {}
                for topic_index, topic in enumerate(self.list_of_topics):
                    input = "{name} - {topic} - {flag}".format(name = row[0], topic = topic, flag = row[topic_index + 1])
                    input_output_dict["input"] = input
                    new_row = pd.DataFrame([input_output_dict])  
                    self.rag_transformed_df = pd.concat([self.rag_transformed_df, new_row], ignore_index=True)
            
            self.save_csv(dataframe=self.rag_transformed_df, location=self.data_transformation.transformation_path, filename="rag_input")

        except Exception as e:
            logging.info("Error in rag_preprocessing")
            raise CustomException(e,sys)

    def preprocessing(self, examples):
        try:
            model_inputs = self.data_transformation.tokenizer(
                examples['input_text'], 
                max_length=512, 
                truncation=True, 
                padding='max_length'  
            )
            with self.data_transformation.tokenizer.as_target_tokenizer():
                labels = self.data_transformation.tokenizer(
                    examples['target_text'], 
                    max_length=512, 
                    truncation=True, 
                    padding='max_length'  
                )
        
            model_inputs['labels'] = labels['input_ids']
            return model_inputs

        except Exception as e:
            logging.info("Error in preprocessing")
            raise CustomException(e,sys)

    def convert_to_features(self):
        try:
            train_data = self.transformed_df[['input', 'output']].to_dict(orient='records')
            dataset = Dataset.from_dict({'input_text': [item['input'] for item in train_data],
                                'target_text': [item['output'] for item in train_data]})
            
            train_test = dataset.train_test_split(test_size=0.1)  # 10% for evaluation
            train_dataset = train_test['train']
            eval_dataset = train_test['test']

            tokenized_dataset_train = train_dataset.map(self.preprocessing, batched=True)
            tokenized_dataset_eval = eval_dataset.map(self.preprocessing, batched=True)

            tokenized_dataset_train.save_to_disk(os.path.join(self.data_transformation.transformation_path, "train"))
            tokenized_dataset_eval.save_to_disk(os.path.join(self.data_transformation.transformation_path, "evaluate"))

        except Exception as e:
            logging.info("Error in convert_to_features")
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self):
        try:
            self.load_dataframe()
            self.direct_question()
            self.rag_preprocessing()
            self.convert_to_features()
        
        except Exception as e:
            logging.info("Error in initiate_data_transformation")
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    data_transformation_obj = DataTransformation()
    data_transformation_obj.initiate_data_transformation()