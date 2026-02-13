import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from PIL import Image
from io import BytesIO
from streamlit_drawable_canvas import st_canvas
import urllib.parse

# --- Setup ---
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

# --- Sketch Section ---
st.markdown("### ✏️ Sketch your idea (optional)")
st.caption("Draw a rough outfit idea. The AI will use this sketch as inspiration.")

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.0)",
    stroke_width=3,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=320,
    width=240,
    drawing_mode="freedraw",
    key="canvas",
)

# --- Sketch Toolbar ---
col_a, col_b = st.columns([3, 1])
with col_a:
    st.caption("Tip: Draw silhouette first, then add details.")
with col_b:
    if st.button("🧹 Clear sketch"):
        st.session_state["canvas"] = None

st.divider()
st.caption("Design custom outfits with AI")

# --- Style Gallery (Presets) ---
st.markdown("### 🖼️ Explore styles")
st.caption("Click a style to prefill your design. You can tweak it after.")

STYLE_PRESETS = {
    "Casual": {
        "emoji": "👕",
        "prompt": "Relaxed everyday outfit with comfortable fit and minimal details"
    },
    "Formal": {
        "emoji": "🕴️",
        "prompt": "Elegant formal wear suitable for evening events and ceremonies"
    },
    "Streetwear": {
        "emoji": "🧢",
        "prompt": "Modern streetwear with bold accents and urban aesthetic"
    },
    "Bridal": {
        "emoji": "👰",
        "prompt": "Bridal outfit with intricate embroidery and luxurious fabrics"
    },
}

# Session state for prefill
if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = ""
if "preset_style" not in st.session_state:
    st.session_state.preset_style = "Casual"

cols = st.columns(4)
for i, (style_name, data) in enumerate(STYLE_PRESETS.items()):
    with cols[i]:
        if st.button(f"{data['emoji']} {style_name}"):
            st.session_state.preset_prompt = data["prompt"]
            st.session_state.preset_style = style_name





# --- UI Controls ---
prompt = st.text_input(
    "Describe your outfit idea ✍️",
    value=st.session_state.get("preset_prompt", ""),
    key="prompt_input"
)

style = st.selectbox(
    "Style",
    ["Casual", "Formal", "Streetwear", "Bridal"],
    index=["Casual", "Formal", "Streetwear", "Bridal"].index(
        st.session_state.get("preset_style", "Casual")
    ),
    key="style_select"
)

fabric = st.selectbox("Fabric", ["Silk", "Denim", "Cotton", "Velvet"], key="fabric_select")
color = st.color_picker("Pick a main color", "#1f77b4", key="color_picker")
occasion = st.selectbox(
    "Occasion",
    ["Everyday", "Party", "Wedding", "Runway", "Office"],
    key="occasion_select"
)


# --- Generate ---
if st.button("✨ Generate Design"):
    if prompt:
        with st.spinner("Creating design..."):
            sketch_note = ""
            if canvas_result.image_data is not None:
                sketch_note = "Use the user's rough sketch as inspiration for the garment silhouette and details. "

            full_prompt = (
                f"{sketch_note}"
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

            st.markdown("### 📝 Design Description")
            st.write(text_response.output_text)
    else:
        st.warning("Please enter a description.")





