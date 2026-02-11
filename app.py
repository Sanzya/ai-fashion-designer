import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from PIL import Image
from io import BytesIO

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Fashion Designer", layout="centered")

st.title("👗 AI Fashion Designer")
st.write("Describe your outfit and AI will design it!")

prompt = st.text_input("Describe your clothing idea:")

if st.button("Generate Design"):
    if prompt:
        with st.spinner("Creating design..."):
            response = client.images.generate(
                model="gpt-image-1",
                prompt=f"Fashion design sketch, studio lighting, white background, {prompt}",
                size="1024x1024"
            )

            image_base64 = response.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_bytes))

            st.image(image, caption="AI Generated Design")
    else:
        st.warning("Please enter a description.")
