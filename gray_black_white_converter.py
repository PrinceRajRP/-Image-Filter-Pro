from PIL import Image
import streamlit as st
import io

st.title("Convert Color to Black & White, Grey 📸")

# This creats a button for user to click and upload a file
uploaded_file = st.file_uploader("Choose an Image. . .", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image using PIL
    image = Image.open(uploaded_file)

    # Convert the image to grayscale ('L' mode)
    grayscale_img = image.convert('L')

    threshold = st.slider("TUne thee Black & White balance", 0, 255, 128)
    # Create the Black & White version
    bw_img = grayscale_img.point(lambda x: 0 if x < threshold else 255, '1')

    #select logic
    option = st.radio("Select Filter", ["Original", "Gray", "Black & White"])

    if option == "Original":
        final_img = image
    elif option == "Gray":
        final_img = grayscale_img
    else:
        final_img = bw_img

    st.image(final_img)

    #Download Logic
    buf = io.BytesIO()
    final_img.save(buf, format="PNG")
    st.download_button("Download Result", buf.getvalue(), "filtered_image.png")
