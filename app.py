import streamlit as st
from src.pipeline.prediction_pipeline import PredictionPipeline


@st.cache_resource
def get_response(user_input):

    prediction_obj = PredictionPipeline()
    response = prediction_obj.initiate_pipeline(text=user_input)
    return response



st.title("Chatbot Application")
st.markdown("This is a simple chatbot using a pre-trained model.")

user_input = st.text_input("You:", "")

if user_input:
    with st.spinner("Generating response..."):
        response = get_response(user_input)
        st.write(f"Bot: {response}")
