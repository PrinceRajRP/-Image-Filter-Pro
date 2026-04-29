# 🎨 Image Artist

A sleek, interactive web application built with Python and Streamlit that transforms your photos into stunning visual art. Upload an image and instantly apply various computer vision filters, including a highly customizable, dynamic pencil sketch effect.

## ✨ Features

* **Original View:** Inspect your raw uploaded photo in a responsive, full-width container.
* <img width="1024" height="587" alt="image" src="https://github.com/user-attachments/assets/55e6967d-27e6-4d85-9771-f4ac552e0076" />

* **Grayscale:** Convert any colorful photo into a classic, elegant monochrome image.
* <img width="1023" height="443" alt="image" src="https://github.com/user-attachments/assets/b7f948ab-73b5-4f2a-b493-c542eafd09d5" />

* **Black & White:** Create high-contrast binary art. Includes an **adjustable threshold slider** (0-255) to perfectly balance the light and dark pixels.
* <img width="1024" height="442" alt="image" src="https://github.com/user-attachments/assets/bc48917a-fd91-40c0-8b20-a18cfa36dbe0" />

* **Pro Pencil Sketch:** An advanced, math-driven sketch effect featuring:
* <img width="1024" height="438" alt="image" src="https://github.com/user-attachments/assets/776dcff1-58cb-454b-b410-305b4676a2c3" />

  * **Dynamic Line Boldness:** The "brush size" automatically scales based on a percentage of your image's width. This ensures the sketch looks consistent whether you upload a tiny icon or a massive 4K photograph!
  * **Adjustable Sketch Intensity:** Control the underlying Gaussian Blur to make the pencil strokes look sharp and precise or soft and smudged.
* **Side-by-Side Comparison:** Instantly see your original photo next to the processed masterpiece.
* **One-Click Download:** Save your newly generated art locally as a high-quality PNG.

## 🛠️ Tech Stack

* **[Streamlit](https://streamlit.io/):** For the interactive web interface and responsive layout.
* **[OpenCV](https://opencv.org/):** (`cv2`) For core image processing, matrix divisions, and Gaussian blurring.
* **[NumPy](https://numpy.org/):** For fast mathematical operations on image arrays.
* **[Pillow (PIL)](https://python-pillow.org/):** For reading, converting, and saving image files.
