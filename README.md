# 🎨 Image Artist

A fast, interactive web application built with Python that lets users upload images and apply various artistic filters in real-time.

✨ Features
Upload any image and instantly apply a variety of custom-built image processing filters. The app currently supports the following styles:

* Original: View the untouched base image.
* <img width="1024" height="587" alt="image" src="https://github.com/user-attachments/assets/55e6967d-27e6-4d85-9771-f4ac552e0076" />

* **Grayscale:** Convert any colorful photo into a classic, elegant monochrome image.
* <img width="1023" height="443" alt="image" src="https://github.com/user-attachments/assets/b7f948ab-73b5-4f2a-b493-c542eafd09d5" />

* **Black & White:** Create high-contrast binary art. Includes an **adjustable threshold slider** (0-255) to perfectly balance the light and dark pixels.
* <img width="1024" height="442" alt="image" src="https://github.com/user-attachments/assets/bc48917a-fd91-40c0-8b20-a18cfa36dbe0" />

* **Pro Pencil Sketch:** An advanced, math-driven sketch effect featuring:
* <img width="1024" height="438" alt="image" src="https://github.com/user-attachments/assets/776dcff1-58cb-454b-b410-305b4676a2c3" />

* **Inverted:**	Flips color values while keeping the transparency layer untouched.
* <img width="891" height="582" alt="image" src="https://github.com/user-attachments/assets/d5c44f5b-2b92-4525-9699-e28b32761012" />

* **Vintage Sepia:** Warm, nostalgic tones with simulated film grain spread.
* <img width="888" height="582" alt="image" src="https://github.com/user-attachments/assets/112fb828-a96a-4602-92c5-008e38a9c48e" />

* **Pop-Art:** A highly stylized, retro posterization effect (includes adjustable intensity/step-size controls!).
* <img width="1621" height="760" alt="image" src="https://github.com/user-attachments/assets/19256047-2235-4e0b-b57e-aafed6effd20" />



  🛡️ Smart Alpha Preservation
Unlike standard filters that often strip transparency, this app uses custom slicing logic to isolate, protect, and reintegrate the Alpha layer (RGBA). Your transparent backgrounds stay transparent.

✏️ Dynamic Pencil Sketch
Dynamic Line Boldness: The "brush size" automatically scales based on a percentage of your image's width. This ensures the sketch looks consistent whether you upload a tiny icon or a massive 4K photograph!

Adjustable Sketch Intensity: Control the underlying Gaussian Blur to make the pencil strokes look sharp and precise or soft and smudged.

🎞️ True Vintage Transformation
Experience an authentic old-school aesthetic using a specialized BGR color matrix combined with Gaussian noise to simulate realistic film grain and aged photography styles.

⚙️ Robust Input Handling
Universal Compatibility: Seamlessly processes RGB, RGBA, and 2D Grayscale images.

Auto-Correction: Features automated shape detection and array reshaping to prevent common processing crashes.

💻 User Experience
Side-by-Side Comparison: Instantly see your original photo next to the processed masterpiece to fine-tune your settings.

One-Click Download: Save your newly generated art locally as a high-quality, transparency-ready PNG.

## 🛠️ Tech Stack

* **[Streamlit](https://streamlit.io/):** For the interactive web interface and responsive layout.
* **[OpenCV](https://opencv.org/):** (`cv2`) For core image processing, matrix divisions, and Gaussian blurring.
* **[NumPy](https://numpy.org/):** For fast mathematical operations on image arrays.
* **[Pillow (PIL)](https://python-pillow.org/):** For reading, converting, and saving image files.
