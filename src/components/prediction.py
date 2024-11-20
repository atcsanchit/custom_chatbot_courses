import sys
import os
from dataclasses import dataclass
from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.logger import logging
from src.exception import CustomException


@dataclass
class PredictionConfig:
    model_path = os.path.join("artifacts","model_trainer", "fine_tuned_flan_t5_base_model")
    tokenizer_path = os.path.join("artifacts","model_trainer","fine_tuned_flan_t5_base_tokenizer")
    length_penalty = 0.8
    num_beams = 8
    max_length = 128
    rag_file_path = "rag_input.csv"
    message = """
                Answer this question using the provided context only. Make sure to answer the questions in more personised way and user friendly way.

                {question}

                Context:
                {context}
                """
    persist_directory = os.path.join("artifacts","chroma_db")

class Prediction:
    def __init__(self):
        self.prediction = PredictionConfig()
    
    # def load_split_data(self):
    #     try:
    #         loader = CSVLoader(file_path=self.prediction.rag_file_path, encoding='cp1252')
    #         data = loader.load()

    #         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    #         self.splits = text_splitter.split_documents(data)

    #     except Exception as e:
    #         logging.info("Error in load_split_data")
    #         raise CustomException(e,sys)


    def store_in_VD(self,query):
        try:
            embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
            vectorstore = Chroma(persist_directory=self.prediction.persist_directory,
                                  embedding_function=embeddings_model)
            
            retriever = vectorstore.as_retriever(
                            search_type="similarity",
                            search_kwargs={"k": 10},

                        )

            results = retriever.get_relevant_documents(query)
            list_of_outputs = []
            for i, result in enumerate(results, 1):
                list_of_outputs.append(result.page_content)


            return (" ".join(list(set(list_of_outputs))))



        except Exception as e:
            logging.info("Error in store_in_VD")
            raise CustomException(e,sys)

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

            # self.load_split_data()
            context = self.store_in_VD(query = text)
            self.prediction.message = self.prediction.message.format(question = text, context = context)
            print("*"*500)
            print(self.prediction.message)
            output = pipe(self.prediction.message, **gen_kwargs)[0]["generated_text"]
            return output

        except Exception as e:
            logging.info("Error in generate_text")
            raise CustomException(e,sys)