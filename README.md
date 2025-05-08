# Image Watermarking Desktop Application & Web App

This project provides both a Python desktop application (Tkinter) and a web application (Flask) for adding watermark logos or text to images.

## Features
- Upload an image (PNG, JPG, JPEG, BMP, GIF)
- Add a logo watermark (bottom right corner)
- Add a text watermark (bottom right corner, with background for visibility)
- Adjustable text size and transparency (web app)
- Save/download the watermarked image

## Setup
1. **Clone the repository or download the files.**
2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install pillow flask tk
   ```
4. **(Web App Only) Download the font file:**
   - Download [DejaVuSans-Bold.ttf](https://github.com/dejavu-fonts/dejavu-fonts/blob/master/ttf/DejaVuSans-Bold.ttf)
   - Place it in your project directory: `DejaVuSans-Bold.ttf`

## Usage
### Desktop App
1. **Run the application:**
   ```bash
   python watermark_app.py
   ```
2. **Instructions:**
   - Click "Upload Image" to select an image file.
   - (Optional) Click "Upload Logo" to add a logo watermark.
   - (Optional) Enter text in the entry box and click "Add Text Watermark" to add a text watermark.
   - Click "Save Image" to save the watermarked image.

### Web App
1. **Run the application:**
   ```bash
   python web_watermark_app.py
   ```
2. **Open your browser and go to:**
   [http://127.0.0.1:5001/](http://127.0.0.1:5001/)
3. **Instructions:**
   - Upload an image (required)
   - (Optional) Upload a logo (bottom right watermark)
   - (Optional) Enter text for a watermark (bottom right, with background)
   - Click "Add Watermark & Download" to get your watermarked image
   - Use the "Clear" buttons to remove selected files before submitting

## Notes
- The web app uses the `DejaVuSans-Bold.ttf` font from your project directory for consistent, scalable text rendering.
- The text watermark is always visible, with a semi-transparent background and adjustable transparency.
- The font size and padding are dynamically adjusted to ensure the watermark always fits within the image.

## Requirements
- Python 3.x
- Pillow
- Flask (for web app)
- Tkinter (for desktop app) 