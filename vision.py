from dotenv import load_dotenv
load_dotenv()

import streamlit as st  
import os
import google.generativeai as genai
from PIL import Image
import base64

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(input, image):
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stHeader {{
            padding: 0;
            margin: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="Image Recognition App" , page_icon=":camera:", layout="centered", initial_sidebar_state="expanded")

st.header("Image Recognition ChatBot", anchor=None)
input = st.text_input("Input Prompt: ", key="input")

set_background("d:/project/background_image.jpg") 

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
