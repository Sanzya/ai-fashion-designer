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
st.write("Design custom outfits with AI")

# --- UI Controls ---
prompt = st.text_input("Describe your clothing idea:")

style = st.selectbox(
    "Style",
    ["Casual", "Formal", "Streetwear", "Bridal"]
)

fabric = st.selectbox(
    "Fabric",
    ["Silk", "Denim", "Cotton", "Velvet"]
)

color = st.color_picker("Pick a main color", "#1f77b4")

occasion = st.selectbox(
    "Occasion",
    ["Everyday", "Party", "Wedding", "Runway", "Office"]
)

if st.button("Generate Design"):
    if prompt:
        with st.spinner("Creating design..."):
            full_prompt = (
                f"Fashion design sketch of a {style.lower()} outfit made of {fabric.lower()}, "
                f"main color {color}, for {occasion.lower()} occasion. "
                f"Studio lighting, white background. {prompt}"
            )

            response = client.images.generate(
                model="gpt-image-1",
                prompt=full_prompt,
                size="1024x1024"
            )

            image_base64 = response.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_bytes))

            st.image(image, caption="AI Generated Design")

            # --- Download Button ---
            buf = BytesIO()
            image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="⬇️ Download Design",
                data=byte_im,
                file_name="ai_fashion_design.png",
                mime="image/png",
            )

            # --- Auto Description ---
            description_prompt = (
                f"Write a short, elegant 2-sentence description of a {style.lower()} "
                f"{fabric.lower()} outfit in {color} for a {occasion.lower()} occasion."
            )

            text_response = client.responses.create(
                model="gpt-4.1-mini",
                input=description_prompt
            )

            description = text_response.output_text

            st.markdown("### 📝 Design Description")
            st.write(description)

    else:
        st.warning("Please enter a description.")
