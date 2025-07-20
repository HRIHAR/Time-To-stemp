import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import datetime

st.set_page_config(page_title="Image Timestamp App", layout="centered")

st.title("📸 Timestamp Your Images")
st.markdown("Upload up to **500+ photos** and apply a timestamp!")

# Upload images
uploaded_files = st.file_uploader(
    "Upload your photos", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

timestamp = st.text_input("Enter the timestamp (leave blank for current time):")

font_size = st.slider("Font size", min_value=10, max_value=100, value=31)

def add_timestamp(image, timestamp_text, font_size):
    draw = ImageDraw.Draw(image)
    
    # Try to load Arial font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Get text bounding box for accurate placement
    bbox = font.getbbox(timestamp_text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Set position bottom right with padding
    position = (image.width - text_width - 20, image.height - text_height - 20)
    
    # Draw white text with black shadow
    draw.text((position[0]+2, position[1]+2), timestamp_text, font=font, fill="black")
    draw.text(position, timestamp_text, font=font, fill="white")

    return image

if uploaded_files:
    # Use current time if none is provided
    if not timestamp:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.subheader("🔍 Preview (First Image Only):")

    try:
        # Show preview of first image only
        preview_file = uploaded_files[0]
        img = Image.open(preview_file)
        preview_img = add_timestamp(img.copy(), timestamp, font_size)

        st.image(preview_img, caption="Preview with Timestamp", use_column_width=True)
    except Exception as e:
        st.error(f"Error processing preview image: {e}")
