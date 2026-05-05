# 🎨 Image Artist

A A.I-powered photo editing web app that lets you apply artistic filters to your images — with an AI chat assistant that recommends the best filter settings based on your creative goal.

<img width="1909" height="913" alt="image" src="https://github.com/user-attachments/assets/73591411-ba87-4e56-8c66-0b09b75ffaee" />

<img width="1910" height="914" alt="image" src="https://github.com/user-attachments/assets/01085d4f-a50a-46c2-88a5-eb37e8ab2621" />

<img width="1906" height="895" alt="image" src="https://github.com/user-attachments/assets/8e75649f-e233-4fb0-bc49-3c343384d215" />

<img width="1915" height="848" alt="image" src="https://github.com/user-attachments/assets/7da40d61-01aa-481d-a222-106eb90aabc7" />

<img width="1913" height="846" alt="image" src="https://github.com/user-attachments/assets/3cfe04a7-d050-4478-9fb6-c461f584a44a" />

<img width="1904" height="911" alt="image" src="https://github.com/user-attachments/assets/9018b665-e6ec-4b63-a433-7062f784e81c" />

---

## ✨ Features

- **6 Artistic Filters** — Transform your photos with a single click
- **Adjustable Sliders** — Fine-tune each filter to your liking
- **AI Chat Assistant** — Powered by LLaMA 3.2 90B Vision via NVIDIA API; describes your image and recommends filter settings
- **Before / After View** — Side-by-side comparison of original vs. filtered image
- **One-Click Download** — Save your edited image as a PNG instantly

---

## 🖼️ Available Filters

| Filter | Controls |
|---|---|
| **Original** | — |
| **Grayscale** | — |
| **Black & White** | Threshold (0–255) |
| **Pencil Sketch** | Intensity (1–25), Thickness (0.1–5.0%) |
| **Inverted** | — |
| **Vintage Sepia** | Grain Spreadness (0–100) |
| **Pop-Art** | Posterization Level (2–128) |

---

## 🤖 AI Assistant

The **AI Chat** tab uses **LLaMA 3.2 90B Vision** (via NVIDIA's API) to analyze your uploaded image and suggest the ideal filter along with specific slider values. It maintains full conversation history so you can have a back-and-forth dialogue about your image.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/PrinceRajRP/image-artist.git
cd image-artist
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of the project:

```env
NVIDIA_API_KEY_90B=your_nvidia_api_key_here
```

> Get your free API key at [build.nvidia.com](https://build.nvidia.com)

### 5. Run the App

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
image-artist/
├── app.py               # Main Streamlit application
├── .env                 # API keys (do NOT commit this)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📦 Requirements

```
streamlit
Pillow
numpy
opencv-python
requests
python-dotenv
```

> Generate with: `pip freeze > requirements.txt`

---

## 🔒 Environment Variables

| Variable | Description |
|---|---|
| `NVIDIA_API_KEY_90B` | Your NVIDIA API key for LLaMA 3.2 90B Vision |

**Never commit your `.env` file.** Make sure it is listed in `.gitignore`:

```
.env
```

---

## 📸 Usage

1. Upload a `.jpg`, `.jpeg`, or `.png` image
2. Go to the **🎨 Filter** tab → choose a filter from the sidebar → adjust sliders
3. View the **Before / After** comparison and download your result
4. Go to the **🤖 AI Chat** tab → describe your goal (e.g. *"make it look like an old photo"*) and get a personalized filter recommendation

---

## 🛠️ How It Works

- **Image processing** is handled by `OpenCV` and `Pillow` — no cloud calls needed for filters
- **AI recommendations** send a resized (256×256) version of your image along with your message to the NVIDIA API
- **Session state** in Streamlit preserves the full chat history across interactions within a session

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the web framework
- [NVIDIA NIM](https://build.nvidia.com/) for hosted LLaMA 3.2 90B Vision inference
- [OpenCV](https://opencv.org/) for image processing primitives
