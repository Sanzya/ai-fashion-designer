import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from PIL import Image
from io import BytesIO



load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="FashAI – AI Fashion Studio",
    page_icon="👗",
    layout="centered"
)

# --- Hero Header ---
col1, col2 = st.columns([4, 1])

with col1:
    st.markdown("## ✨ **FashAI**")
    st.markdown("### AI Fashion Studio")
    st.caption("From idea to runway in seconds.")


# --- Social Share Buttons ---
import urllib.parse

PUBLIC_URL = "https://ai-fashion-designer-fenqebmvjvtbwgdja8vgiu.streamlit.app/"
SHARE_TEXT = "Check out FashAI – an AI Fashion Designer that creates outfit designs in seconds 👗✨"
ENC_TEXT = urllib.parse.quote(f"{SHARE_TEXT} {PUBLIC_URL}")

st.markdown(
    f"""
<style>
.share-pill:hover {{
  filter: brightness(0.95);
  transform: translateY(-1px);
}}
</style>


<div style="position:fixed; top:64px; right:16px; display:flex; gap:8px; z-index:9999;">
  <a class="share-pill" href="https://wa.me/?text={ENC_TEXT}" target="_blank"
     style="text-decoration:none; border:1px solid #ddd; border-radius:999px; padding:8px 12px; background:#25D366; color:white; font-size:14px;">
     🟢 WhatsApp
  </a>
  <a class="share-pill" href="https://www.linkedin.com/sharing/share-offsite/?url={PUBLIC_URL}" target="_blank"
     style="text-decoration:none; border:1px solid #ddd; border-radius:999px; padding:8px 12px; background:#0A66C2; color:white; font-size:14px;">
     🔵 LinkedIn
  </a>
</div>
""",
    unsafe_allow_html=True,
)


st.divider()

st.caption("Design custom outfits with AI")




# --- UI Controls ---
prompt = st.text_input("Describe your outfit idea✍️")

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

if st.button("✨ Generate Design"):

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
