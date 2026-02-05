import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Time Editor", layout="centered")

st.title("🕒 Clock-In Time Editor")
st.write("If the time doesn't appear in the right spot, we will adjust the coordinates below.")

uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    
    # We create sliders so YOU can move the text to the right spot
    st.sidebar.header("Adjust Position")
    x_pos = st.sidebar.slider("Horizontal (X)", 0, img.width, int(img.width * 0.23))
    y_pos = st.sidebar.slider("Vertical (Y)", 0, img.height, int(img.height * 0.81))
    font_size = st.sidebar.slider("Font Size", 10, 200, 40)

    if st.button("Apply Edit (08:33 AM)"):
        draw = ImageDraw.Draw(img)
        
        # 1. Pick a background color from the image to hide the old time
        # We pick the color exactly where you are placing the text
        try:
            bg_color = img.getpixel((x_pos, y_pos))
        except:
            bg_color = (255, 255, 255) # Default white if it fails

        # 2. Draw a rectangle to hide the old numbers
        # We make it slightly larger than the text
        draw.rectangle([x_pos - 5, y_pos - 5, x_pos + 200, y_pos + 60], fill=bg_color)
        
        # 3. Draw the new time
        text = "08:33 AM"
        # Using a basic font that is guaranteed to be on the server
        font = ImageFont.load_default()
        
        # Draw the text in dark blue/black to match typical clock-in apps
        draw.text((x_pos, y_pos), text, fill=(10, 40, 80), font=font)

        st.success("Applied! Use the sliders on the left if it's in the wrong spot.")
        
        # Save and provide Download
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.image(img, caption="Edited Photo", use_container_width=True)
        st.download_button(label="Download Edited Image", data=byte_im, file_name="edited_0833.png")
    else:
        st.image(img, caption="Original Photo", use_container_width=True)
