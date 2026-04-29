import streamlit as st
import numpy as np
import cv2
import io
from PIL import Image


# --Processing Functions--

def render_pencil_sketch(img_arr, boldness, intensity):
    """Applies the pencil sketch transformation logic."""
    # Convert to grayscale
    gray = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
    # Invert the gray image (negative)
    inverted = 255 - gray

    height, width = img_arr.shape[:2]


    thickness = int(width * (boldness / 100))

    if thickness % 2 == 0:
        thickness += 1

    thickness = max(3, thickness)
    # Blur the negative image
    # Note: (21, 21) is the kernel size (brush width)
    blurred = cv2.GaussianBlur(inverted, (thickness, thickness), intensity)
    # Divide original gray by the blurred negative to find edges
    sketch_arr = cv2.divide(gray, 255 - blurred, scale=255)
    return sketch_arr


st.title("🎨 Image Artist")
st.write("Upload a photo and transform it into masterpeice!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)

    # Sidebar options
    st.sidebar.header("Filter Settings")
    option = st.sidebar.selectbox(
        "Choose a style:",
        ["Original", "Grayscale", "Black & White", "Pencil Sketch"]
    )
    final_img = None

    if option == "Original":
        st.image(img, caption="Your Original Photo", width="stretch")

    else:
        # Create columns for Before and After
        col1, col2 = st.columns(2)

        with col1:
            st.header("Before")
            st.image(img, width="stretch")

        with col2:
            st.header("After")

            if option == "Grayscale":
                final_img = img.convert('L')

            elif option == "Black & White":
                threshold = st.sidebar.slider("B&W Threshold", 0, 255, 128)
                final_img = img.convert('L').point(lambda x: 0 if x < threshold else 255)

            elif option == "Pencil Sketch":
                intensity = st.sidebar.slider("Sketch Intensity", 1, 25, 5)
                img_arr = np.array(img)
                boldness = st.sidebar.slider("Thickness of pencil(%)", 0.1, 5.0, 1.0)
                sketch_arr = render_pencil_sketch(img_arr, boldness, intensity)
                final_img = Image.fromarray(sketch_arr)

            if final_img:
                st.image(final_img, width="stretch")

                buf = io.BytesIO()
                final_img.save(buf, format="PNG")
                st.download_button(
                    label="Download Result", 
                    data=buf.getvalue(), 
                    file_name=f"{option.lower()}_image.png", 
                    mime="image/png"
                )
