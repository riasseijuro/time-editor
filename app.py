import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Clock Editor", layout="wide")

st.title("🕒 Custom Time Editor")
st.write("Type your time, then move the sliders to place it.")

uploaded_file = st.file_uploader("Upload photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    
    # --- SIDEBAR CONTROLS ---
    st.sidebar.header("1. Change Text")
    custom_time = st.sidebar.text_input("Enter Time:", value="08:33 AM")
    
    st.sidebar.header("2. Adjust Position")
    # Sliders now cover the full width/height of your specific image
    x_pos = st.sidebar.slider("Horizontal (Left/Right)", 0, img.width, int(img.width * 0.25))
    y_pos = st.sidebar.slider("Vertical (Up/Down)", 0, img.height, int(img.height * 0.82))
    
    st.sidebar.header("3. Appearance")
    font_size = st.sidebar.slider("Text Size", 10, 500, 150) # Increased max size to 500
    text_color = st.sidebar.color_picker("Pick Text Color", "#0A2850") # Default dark blue

    # --- PROCESSING ---
    if st.button("Apply Changes"):
        draw = ImageDraw.Draw(img)
        
        # Pick background color from the photo automatically
        try:
            bg_color = img.getpixel((x_pos, y_pos))
        except:
            bg_color = (255, 255, 255)

        # Use a built-in font but make it MUCH bigger
        try:
            # We use a very large default font
            font = ImageFont.load_default()
            # If the server supports scaling, we scale it
            font = font.font_variant(size=font_size)
        except:
            font = ImageFont.load_default()

        # Hide the old time with a matching colored box
        box_width = font_size * 5
        box_height = font_size * 1.5
        draw.rectangle([x_pos - 10, y_pos - 10, x_pos + box_width, y_pos + box_height], fill=bg_color)
        
        # Draw your custom time
        draw.text((x_pos, y_pos), custom_time, fill=text_color, font=font)

        # Show Result
        st.image(img, caption="New Preview", use_container_width=True)
        
        # Download Button
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.download_button("Download Edited Image", buf.getvalue(), "edited_clock.png", "image/png")
    else:
        # Show original if button not clicked
        st.image(img, caption="Original", use_container_width=True)
