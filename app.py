import streamlit as st
from diffusers import AutoPipelineForInpainting
import torch
from PIL import Image
import io

# 1. Setup the Webpage Interface
st.title("AI Photo Editor (No Watermark)")
st.write("Upload a photo and edit the time to 08:33 AM")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the original image
    init_image = Image.open(uploaded_file).convert("RGB")
    st.image(init_image, caption="Uploaded Image", use_column_width=True)

    # 2. Load the AI Model (Stable Diffusion XL)
    # Note: This requires a GPU to run fast.
    @st.cache_resource
    def load_model():
        pipe = AutoPipelineForInpainting.from_pretrained(
            "diffusers/stable-diffusion-xl-1.0-inpainting-0.1", 
            torch_dtype=torch.float16, variant="fp16"
        ).to("cuda") # Use "cpu" if you don't have a GPU
        return pipe

    if st.button("Edit Time to 08:33 AM"):
        with st.spinner("Processing... This takes a few seconds."):
            pipe = load_model()
            
            # The 'mask' tells the AI where to change the image
            # In a full app, you'd use a 'sketch' tool to draw over the old time
            prompt = "digital clock text displaying 08:33 AM, high resolution, sharp"
            
            # Generate the new image
            # (In a real script, you'd also pass a 'mask_image' here)
            result_image = pipe(prompt=prompt, image=init_image, mask_image=mask_image).images[0]

            # 3. Show and Download the Result
            st.image(result_image, caption="Edited Image", use_column_width=True)
            
            buf = io.BytesIO()
            result_image.save(buf, format="PNG")
            st.download_button(
                label="Download Edited Image",
                data=buf.getvalue(),
                file_name="edited_clock.png",
                mime="image/png"
            )