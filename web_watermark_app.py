from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get files and text
        image_file = request.files.get('image')
        logo_file = request.files.get('logo')
        watermark_text = request.form.get('watermark_text', '')

        if not image_file:
            return render_template('index.html', error='Please upload an image.')

        # Open main image
        image = Image.open(image_file).convert('RGBA')

        # Add logo if provided
        if logo_file and logo_file.filename:
            logo = Image.open(logo_file).convert('RGBA')
            logo_width = int(image.width * 0.2)
            logo_ratio = logo_width / logo.width
            logo_height = int(logo.height * logo_ratio)
            logo_resized = logo.resize((logo_width, logo_height), Image.LANCZOS)
            position = (image.width - logo_width - 10, image.height - logo_height - 10)
            image.paste(logo_resized, position, logo_resized)

        # Add text watermark if provided
        if watermark_text.strip():
            # Try to fit the text image within the main image
            max_font_size = int(min(int(image.height * 0.12), 300) * 0.5)  # 50% of previous max
            min_font_size = 10
            padding = 40
            font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans-Bold.ttf')
            font_size = max_font_size
            while font_size >= min_font_size:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                except Exception as e:
                    print("Font load error:", e)
                    font = ImageFont.load_default()
                # Calculate text size
                dummy_img = Image.new('RGBA', (1, 1))
                dummy_draw = ImageDraw.Draw(dummy_img)
                bbox = dummy_draw.textbbox((0, 0), watermark_text, font=font)
                textwidth = bbox[2] - bbox[0]
                textheight = bbox[3] - bbox[1]
                total_width = textwidth + 2 * padding
                total_height = textheight + 2 * padding
                if total_width <= image.width and total_height <= image.height:
                    break
                font_size -= 4  # Decrease font size and try again
            print(f"Loaded font from: {font_path}, font size: {font_size}")
            # Create image for text
            text_img = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_img)
            # Draw a more transparent rectangle for contrast
            text_draw.rectangle([0, 0, total_width, total_height], fill=(0,0,0,100))
            # Draw the text with more transparency
            text_draw.text((padding, padding), watermark_text, font=font, fill=(255,255,255,160))
            # Position: bottom right with larger margin
            margin = 40
            x = max(margin, image.width - text_img.width - margin)
            y = max(margin, image.height - text_img.height - margin)
            # Paste text image onto main image
            image.alpha_composite(text_img, (x, y))

        # Save to BytesIO
        img_io = io.BytesIO()
        image = image.convert('RGB')
        image.save(img_io, 'JPEG', quality=95)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg', as_attachment=True, download_name='watermarked.jpg')

    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 