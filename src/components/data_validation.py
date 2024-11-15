import sys
import os
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException


@dataclass
class DataValidationConfig:
    all_required_files = ["wechatbot.csv"]
    status_file = "artifacts/data_validation"
    data_path = os.path.join("artifacts","data_ingestion")

class DataValidation:
    def __init__(self):
        self.data_validation = DataValidationConfig()
    
    def save_txt(self, file, location, filename):
        try:
            if not os.path.exists(location):
                os.makedirs(location, exist_ok=True)
        
            with open(os.path.join(location, filename + ".txt"), "w") as f:
                f.write(file)

        except Exception as e:
            logging.info("Error in save_txt")
            raise CustomException(e,sys)
        
    def validate_all_file_exist(self):
        try:
            validation_status = None
            all_files = os.listdir(self.data_validation.data_path)
            # print(all_files)
            for file in all_files:
                if file not in self.data_validation.all_required_files:
                    validation_status = False
                    break
                else:
                    validation_status = True

            file = f"validation_status:{validation_status}"
            self.save_txt(file=file, location=self.data_validation.status_file, filename="status")

        except Exception as e:
            logging.info("Error in validate_all_file_exist")
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    data_validation_obj = DataValidation()
    data_validation_obj.validate_all_file_exist()