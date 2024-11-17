import sys
import os
from dataclasses import dataclass
from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline

from src.logger import logging
from src.exception import CustomException


@dataclass
class PredictionConfig:
    model_path = os.path.join("artifacts","model_trainer", "fine_tuned_flan_t5_base_model")
    tokenizer_path = os.path.join("artifacts","model_trainer","fine_tuned_flan_t5_base_tokenizer")
    length_penalty = 0.8
    num_beams = 8
    max_length = 128

class Prediction:
    def __init__(self):
        self.prediction = PredictionConfig()
    
    def generate_text(self, text):
        try:
            model = T5ForConditionalGeneration.from_pretrained(self.prediction.model_path)
            tokenizer = T5Tokenizer.from_pretrained(self.prediction.tokenizer_path)

            gen_kwargs = {
                "length_penalty": self.prediction.length_penalty,
                "num_beams": self.prediction.num_beams,
                "max_length": self.prediction.max_length
            }

            pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
            output = pipe(text, **gen_kwargs)[0]["generated_text"]
            return output

        except Exception as e:
            logging.info("Error in generate_text")
            raise CustomException(e,sys)