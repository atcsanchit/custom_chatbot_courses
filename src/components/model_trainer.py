import sys
import pandas as pd
from datasets import Dataset, DatasetDict, load_from_disk
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import Trainer, TrainingArguments
import os
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException


@dataclass
class ModelTrainerConfig:
    train_path = os.path.join("artifacts","data_transformation","train")
    evaluate_path = os.path.join("artifacts","data_transformation","evaluate")
    model_name = "google/flan-t5-base"
    output_path = os.path.join("artifacts","model_trainer")
    evaluation_strategy='no'
    learning_rate=2e-5
    per_device_train_batch_size=4
    per_device_eval_batch_size=4
    num_train_epochs=3
    weight_decay=0.01    

class ModelTrainer:
    def __init__(self):
        self.model_trainer = ModelTrainerConfig()
    
    def initiate_training(self):
        try:
            tokenizer = T5Tokenizer.from_pretrained(self.model_trainer.model_name)
            model = T5ForConditionalGeneration.from_pretrained(self.model_trainer.model_name)
            
            tokenized_dataset_train = load_from_disk(self.model_trainer.train_path)
            tokenized_dataset_evaluate = load_from_disk(self.model_trainer.evaluate_path)

            if not os.path.exists(self.model_trainer.output_path):
                os.makedirs(self.model_trainer.output_path)
            
            training_args = TrainingArguments(
                output_dir=self.model_trainer.output_path,
                evaluation_strategy=self.model_trainer.evaluation_strategy,  
                learning_rate=self.model_trainer.learning_rate,
                per_device_train_batch_size=self.model_trainer.per_device_train_batch_size,
                per_device_eval_batch_size=self.model_trainer.per_device_eval_batch_size,
                num_train_epochs=self.model_trainer.num_train_epochs,
                weight_decay=self.model_trainer.weight_decay
            )

            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=tokenized_dataset_train,
                eval_dataset=tokenized_dataset_evaluate
            )

            trainer.train()
            
            model.save_pretrained(os.path.join(self.model_trainer.output_path, "fine_tuned_flan_t5_base_model"))
            tokenizer.save_pretrained(os.path.join(self.model_trainer.output_path, "fine_tuned_flan_t5_base_tokenizer"))

        except Exception as e:
            logging.info("Error in initiate_training")
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    model_trainer = ModelTrainer()
    model_trainer.initiate_training()