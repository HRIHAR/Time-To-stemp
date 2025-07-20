
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io

st.set_page_config(page_title="Batch Image Timestamp App", layout="wide")
st.title("🕒 Batch Image Timestamp App")
st.write("Upload one or more images and preview timestamp placement before processing.")

uploaded_files = st.file_uploader(
    "Upload image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)
timestamp_text = st.text_input("Enter timestamp text", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
position = st.selectbox("Select timestamp position", ["Bottom Right", "Top Left", "Bottom Left", "Top Right"])
font_size_ratio = st.slider("Font Size (relative to image height)", 1, 10, 3)

if uploaded_files:
    st.subheader("Preview Before Processing")

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file).convert("RGB")
        preview_img = image.copy()
        draw = ImageDraw.Draw(preview_img)
        font_size = int(preview_img.size[1] * (font_size_ratio / 100))

        # Try to load system font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Calculate text size
        bbox = draw.textbbox((0, 0), timestamp_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        margin = 10

        # Position logic
        if position == "Bottom Right":
            x = preview_img.width - text_width - margin
            y = preview_img.height - text_height - margin
        elif position == "Top Left":
            x, y = margin, margin
        elif position == "Bottom Left":
            x, y = margin, preview_img.height - text_height - margin
        elif position == "Top Right":
            x = preview_img.width - text_width - margin
            y = margin

        # Draw timestamp on preview
        draw.text((x, y), timestamp_text, font=font, fill="white")

        # Display preview
        st.image(preview_img, caption=f"Preview: {uploaded_file.name}", use_column_width=True)

    st.subheader("Download Processed Images")

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file).convert("RGB")
        draw = ImageDraw.Draw(image)
        font_size = int(image.size[1] * (font_size_ratio / 100))

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), timestamp_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if position == "Bottom Right":
            x = image.width - text_width - 10
            y = image.height - text_height - 10
        elif position == "Top Left":
            x, y = 10, 10
        elif position == "Bottom Left":
            x, y = 10, image.height - text_height - 10
        elif position == "Top Right":
            x = image.width - text_width - 10
            y = 10

        draw.text((x, y), timestamp_text, font=font, fill="white")

        # Save to buffer
        buf = io.BytesIO()
        image_format = uploaded_file.type.split("/")[1].upper()
        image.save(buf, format=image_format)
        byte_im = buf.getvalue()

        st.download_button(
            label=f"📥 Download: {uploaded_file.name}",
            data=byte_im,
            file_name=f"timestamped_{uploaded_file.name}",
            mime=uploaded_file.type
        )
