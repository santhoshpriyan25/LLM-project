from dotenv import load_dotenv
load_dotenv()

import streamlit as st  
import os
import google.generativeai as genai
from PIL import Image


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(input, image):
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

st.set_page_config(page_title="Image Recognition App" , page_icon=":camera:", layout="centered", initial_sidebar_state="expanded")

st.header("Image Recognition Bot")
input = st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader("Choose an image... ", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_container_width=True)

submit=st.button("Generate Response")

if submit:
    if image is None:
        st.warning("Please upload an image first.", icon="⚠️")
    else:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input, image)
        st.success("Response generated!", icon="✅")
        st.write(response)
