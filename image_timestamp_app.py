import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
import tempfile

# Function to overlay timestamp
def add_timestamp(img, text, font_size=40):
    draw = ImageDraw.Draw(img)

    # Try to use Arial, fallback if not available
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)

    text_width, text_height = draw.textsize(text, font=font)
    x = img.width - text_width - 20
    y = img.height - text_height - 20

    draw.text((x, y), text, font=font, fill="white")
    return img

# Streamlit UI
st.title("🕒 Time to Photo")
st.markdown("Upload up to 500+ photos and apply a timestamp!")

uploaded_files = st.file_uploader("Upload your photos", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

timestamp_text = st.text_input("Enter the timestamp (leave blank for current time):")
font_size = st.slider("Font size", min_value=10, max_value=100, value=40)

# Show preview
if uploaded_files:
    preview_file = uploaded_files[0]  # Show only the first image
    st.markdown("### Preview (First Image Only):")

    image = Image.open(preview_file).convert("RGB")
    timestamp = timestamp_text if timestamp_text else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    preview_img = add_timestamp(image.copy(), timestamp, font_size)
    st.image(preview_img, caption="Preview")

    if st.button("Process All Images"):
        with tempfile.TemporaryDirectory() as tmpdirname:
            for i, uploaded_file in enumerate(uploaded_files):
                img = Image.open(uploaded_file).convert("RGB")
                timestamp = timestamp_text if timestamp_text else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                img_with_text = add_timestamp(img, timestamp, font_size)

                save_path = os.path.join(tmpdirname, f"timestamped_{i+1}.jpg")
                img_with_text.save(save_path)

            st.success(f"Processed {len(uploaded_files)} images with timestamps.")

