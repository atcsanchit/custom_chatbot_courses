from requests_html import HTMLSession
import sys
import io
import pandas as pd
import os
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException
# from src.utils.general import save_csv


@dataclass
class DataIngestionConfig:
    url="https://brainlox.com/courses/category/technical"
    name = []
    course_desc = []
    session_price = []
    lesson = []
    duration = []
    price = []
    directory = "artifacts/data_ingestion"
    filename = "wechatbot"

class DataIngestion:
    def __init__(self):
        self.data_ingestion = DataIngestionConfig()

    def configuration(self):
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            self.session = HTMLSession()
            self.render = self.session.get(self.data_ingestion.url)

            self.render.html.render(sleep=1)

            self.courses = self.render.html.xpath('//*[@class="row"]',first=True)

        except Exception as e:
            logging.info("Error in configuration")
            raise CustomException(e,sys)        

    
    def initiate_parsing(self):
        try:
            for links in self.courses.absolute_links:
                self.render = self.session.get(links)
                try:
                    self.data_ingestion.name.append(self.render.html.find("div.page-title-content h2")[0].text)
                except:
                    self.data_ingestion.name.append(None)
                
                try:
                    self.data_ingestion.course_desc.append(self.render.html.find("div.courses-overview p")[0].text)
                    # course_desc = ''.join(char for char in course_desc.text if unicodedata.category(char) != 'So')
                    # print(filtered_text)
                except:
                    self.data_ingestion.course_desc.append(None)
                try:
                    ul = self.render.html.find("ul.info",first=True)
                    # print(lesson)
                    if ul:
                        li_items=ul.find("li")
                        if li_items[0]:
                            self.data_ingestion.session_price.append(int(li_items[0].text[12:14]))
                        else:
                            self.data_ingestion.session_price.append(None)

                        if li_items[1]:
                            self.data_ingestion.lesson.append(int(li_items[1].text[7:9]))
                        else:
                            self.data_ingestion.lesson.append(None)
                        
                        if li_items[2]:
                            self.data_ingestion.duration.append(li_items[2].text[8:])
                        else:
                            self.data_ingestion.duration.append(None)
                        
                        if li_items[3]:
                            self.data_ingestion.price.append(int(li_items[3].text[6:]))
                        else:
                            self.data_ingestion.price.append(None)
                        
                except:
                    self.data_ingestion.session_price.append(None)
                    self.data_ingestion.lesson.append(None)
                    self.data_ingestion.duration.append(None)
                    self.data_ingestion.price.append(None)

        except Exception as e:
            logging.info("Error in initiate_parsing")
            raise CustomException(e,sys)      

    def save_csv(self, dataframe, location, filename):
        try:
            if not os.path.exists(location):
                os.makedirs(location, exist_ok=True)

            dataframe.to_csv(os.path.join(location, (filename + ".csv")), index=False)

        except Exception as e:
            logging.info("Error in save_csv")
            raise CustomException(e,sys)      
    
    def create_dataframe(self):
        try:
            self.dataframe = pd.DataFrame({
                "Name":self.data_ingestion.name,
                "Description":self.data_ingestion.course_desc,
                "Session_Price":self.data_ingestion.session_price,
                "Lessons":self.data_ingestion.lesson,
                "Duration":self.data_ingestion.duration,
                "Price":self.data_ingestion.price
            })

            self.save_csv(dataframe=self.dataframe, location=self.data_ingestion.directory, filename=self.data_ingestion.filename)

        except Exception as e:
            logging.info("Error in create_dataframe")
            raise CustomException(e,sys)        
    
    def initiate_data_ingestion(self):
        try:
            self.configuration()
            self.initiate_parsing()
            self.create_dataframe()


        except Exception as e:
            logging.info("Error in initiate_data_ingestion")
            raise CustomException(e,sys)        


if __name__ == "__main__":
    data_ingestion_obj = DataIngestion()
    data_ingestion_obj.initiate_data_ingestion()