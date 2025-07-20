
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io

st.title("🕒 Image Timestamp App")
st.write("Upload an image and add a visible timestamp to it.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
timestamp_text = st.text_input("Enter timestamp text", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
position = st.selectbox("Select timestamp position", ["Bottom Right", "Top Left", "Bottom Left", "Top Right"])
font_size_ratio = st.slider("Font Size (relative to image height)", 1, 10, 3)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    draw = ImageDraw.Draw(image)
    font_size = int(image.size[1] * (font_size_ratio / 100))

    # Use default font or system font if available
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    text_width, text_height = draw.textsize(timestamp_text, font=font)
    margin = 10

    if position == "Bottom Right":
        x = image.width - text_width - margin
        y = image.height - text_height - margin
    elif position == "Top Left":
        x, y = margin, margin
    elif position == "Bottom Left":
        x, y = margin, image.height - text_height - margin
    elif position == "Top Right":
        x = image.width - text_width - margin
        y = margin

    draw.text((x, y), timestamp_text, font=font, fill="white")

    st.image(image, caption="Stamped Image", use_column_width=True)

    # Download button
    buf = io.BytesIO()
    image_format = uploaded_file.type.split("/")[1].upper()
    image.save(buf, format=image_format)
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Download Stamped Image",
        data=byte_im,
        file_name=f"timestamped_{uploaded_file.name}",
        mime=uploaded_file.type
    )
