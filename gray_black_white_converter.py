from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import numpy as np
import requests
import base64
import cv2
import io
import os

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY_90B")


def get_ai_recommendation(img, goal, chat_history):

    img_resize = img.resize((512, 512))
    buf = io.BytesIO()
    if img_resize.mode != "RGB":
        img_resize = img_resize.convert("RGB")
    img_resize.save(buf, format="JPEG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    messages = []
    for exchange in chat_history:
        messages.append({"role": "user", "content": exchange["user"]})
        messages.append({"role": "assistant", "content": exchange["ai"]})

    
    content = [
                    {
                        "type": "text",
                        "text": f"""The user says: "{goal}". 
                        If this is a greeting or small talk, respond warmly and ask what they want to do with their image.
                        If this relates to the image or filters, analyze the image and give a helpful recommendation with slider values.
                        If this is off-topic, politely redirect them to image filters."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
                    }
                ]

    messages.append({"role": "user", "content": content})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    payload = {
        "model": "meta/llama-3.2-90b-vision-instruct",
        "messages": [
            {
                "role": "system",
                "content": """You are a helpful image filter assistant for a photo editing app. Help users pick the best filter for their image.

                You ONLY recommend filters from these 6 options:
                1. Grayscale
                2. Black & White (threshold: 0-255)
                3. Pencil Sketch (intensity: 1-25, boldness: 0.1-5.0)
                4. Inverted
                5. Vintage Sepia (spreadness: 0-100)
                6. Pop-Art (posterization level: 2-128)

                Behavior rules:
                - If the user greets you, greet them back and ask what effect they want on their image.
                - If the user asks about the image, describe it briefly, then suggest one relevant filter with slider values.
                - If the user asks something unrelated to image editing, politely say you can only assist with image filters and ask about their image goal.
                - Never recommend any filter outside the 6 listed above.
                - Always suggest specific slider values when recommending a filter.
                - Reply in plain text only. No markdown, no bullet points, no headers. Keep it concise.
                - You have access to the full conversation history above. Always use it to maintain context and refer back to previous messages when relevant."""
            },
            *messages
        ],
        "max_tokens": 200,
        "temperature": 1,
        
    }

    response = requests.post("https://integrate.api.nvidia.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    result = response.json()["choices"][0]["message"]["content"]
    return result


# --Processing Functions--

def render_pencil_sketch(img_arr, boldness, intensity):
    """Applies the pencil sketch transformation logic."""

    shape = img_arr.shape
    has_alpha = len(shape) == 3 and shape[2] == 4

    if has_alpha:
        color_part = img_arr[:, :, :3]
        alpha_part = img_arr[:, :, 3:]
    else:
        color_part = img_arr
        alpha_part = None

    # Convert to grayscale
    gray = cv2.cvtColor(color_part, cv2.COLOR_RGB2GRAY)
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
    
    if has_alpha:
        return np.dstack((sketch_arr, alpha_part.reshape(sketch_arr.shape[0], sketch_arr.shape[1])))
    else:
        return sketch_arr


def inverted(img_arr):

    # 1. Safely get the dimensions of the image
    shape = img_arr.shape
    
    if len(shape) == 3:
        # Image has channels (height, width, channels)
        height, width, channels = shape
    else:
        # Image is grayscale (height, width)
        height, width = shape
        channels = 1

    if channels == 4:
        color_channels = img_arr[:, :, :3]
        inverted_colors = 255 - color_channels

        alpha_channel = img_arr[:, :, 3:]

        inverted_arr = np.dstack((inverted_colors, alpha_channel))

    else:
        inverted_arr = 255 - img_arr

    return inverted_arr

def apply_sepia(img_arr, spreadness):
    """Applies the Vintage Sepia transformation logic"""

    shape = img_arr.shape
    has_alpha = len(shape) == 3 and shape[2] == 4

    if has_alpha:
        color_part = img_arr[:, :, :3]
        alpha_part = img_arr[:, :, 3:]

    else:
        color_part = img_arr
        alpha_part = None

    # Convert Streamlit's RGB image to BGR for our matrix
    bgr_img = cv2.cvtColor(color_part, cv2.COLOR_RGB2BGR)

    # Our custom BGR Sepia Matrix
    kernel = np.array([[0.131, 0.534, 0.272],
                       [0.168, 0.686, 0.349],
                       [0.189, 0.769, 0.393]])
    
    # Apply color transformation
    sepia_img = cv2.transform(bgr_img, kernel)

    # Add the vintage grain (mu=0, sigma=15)
    noise = np.random.normal(0, spreadness, sepia_img.shape)
    noisy_sepia = sepia_img + noise

    # Clamp values and convert to uint8
    final_bgr = np.clip(noisy_sepia, 0, 255).astype(np.uint8)

    # Convert back to RGB for Streamlit to display properly
    final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)

    # 7. Reconstruct the image if it had transparency
    if has_alpha:
        # Stack the sepia colors with the original alpha
        return np.dstack((final_rgb, alpha_part))
    else:
        return final_rgb


def pop_art(img_arr, step_size):
    """Applies the Pop-Art transformation logic"""
    shape  = img_arr.shape
    has_alpha = len(shape) == 3 and shape[2] == 4

    if has_alpha:
        color_part = img_arr[:, :, :3]
        alpha_part = img_arr[:, :, 3:]
    else:
        color_part = img_arr
        alpha_part =None

    # Divide by a number to reduce then floor(remove numbers after decimal) them
    bucket = color_part // step_size

    # multiply by that number again
    result_img = bucket * step_size

    if has_alpha:
        return np.dstack((result_img, alpha_part))
    else:
        return result_img


st.title("🎨 Image Artist")
st.write("Upload a photo and transform it into masterpeice!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    
    # Normalize: convert grayscale/palette images to RGB (or RGBA to keep transparency)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    img_arr = np.array(img)

    # Initialize one list to store conversation
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []


    tab1, tab2 = st.tabs(["🎨 Filter", "🤖 AI Chat"])

    with tab1:
        # Sidebar options
        st.sidebar.header("Filter Settings")
        option = st.sidebar.selectbox(
            "Choose a style:",
            ["Original", "Grayscale", "Black & White", "Pencil Sketch", "Inverted", "Vintage Sepia", "Pop-Art"]
        )

    with tab2:
        # Display past messages
        for exchange in st.session_state["chat_history"]:
            with st.chat_message("user"):
                st.write(exchange["user"])
            with st.chat_message("assistant"):
                st.write(exchange["ai"])


        # Input bar
        goal = st.chat_input("What's your goal for the image?")
        if goal:
            result = get_ai_recommendation(img, goal, st.session_state["chat_history"])
            st.session_state["chat_history"].append({"user": goal, "ai": result})
            st.rerun()
    

    final_img = None
    with tab1:

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
                    boldness = st.sidebar.slider("Thickness of pencil(%)", 0.1, 5.0, 1.0)
                    sketch_arr = render_pencil_sketch(img_arr, boldness, intensity)
                    final_img = Image.fromarray(sketch_arr)

                elif option == "Inverted":
                    inverted_arr = inverted(img_arr)
                    final_img = Image.fromarray(inverted_arr)

                elif option == "Vintage Sepia":
                    spreadness = st.sidebar.slider("Spreadness of grain effect", 0, 100, 15)
                    vintage_sepia_arr = apply_sepia(img_arr, spreadness)
                    final_img = Image.fromarray(vintage_sepia_arr)

                elif option == "Pop-Art":
                    step_size = st.sidebar.slider("Posterization Level", 2, 128, 64, 8)
                    pop_art_arr = pop_art(img_arr, step_size)
                    final_img = Image.fromarray(pop_art_arr)

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
