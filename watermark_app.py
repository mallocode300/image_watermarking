import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarking App")
        self.root.geometry("800x600")
        self.image = None
        self.logo = None
        self.display_image = None
        self.image_path = None

        # UI Elements
        self.canvas = tk.Canvas(root, width=600, height=400, bg='gray')
        self.canvas.pack(pady=20)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Upload Image", command=self.upload_image).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Upload Logo", command=self.upload_logo).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Add Text Watermark", command=self.add_text_watermark).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Save Image", command=self.save_image).grid(row=0, column=3, padx=5)

        self.text_entry = tk.Entry(root, width=40)
        self.text_entry.pack(pady=5)
        self.text_entry.insert(0, "Enter watermark text here...")

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.image = Image.open(file_path).convert("RGBA")
            self.image_path = file_path
            self.show_image(self.image)

    def upload_logo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path and self.image:
            self.logo = Image.open(file_path).convert("RGBA")
            self.add_logo_watermark()
        elif not self.image:
            messagebox.showwarning("No Image", "Please upload an image first.")

    def add_logo_watermark(self):
        if self.image and self.logo:
            base = self.image.copy()
            # Resize logo to 20% of base image width
            logo_width = int(base.width * 0.2)
            logo_ratio = logo_width / self.logo.width
            logo_height = int(self.logo.height * logo_ratio)
            logo_resized = self.logo.resize((logo_width, logo_height), Image.LANCZOS)
            # Position: bottom right
            position = (base.width - logo_width - 10, base.height - logo_height - 10)
            base.paste(logo_resized, position, logo_resized)
            self.image = base
            self.show_image(self.image)

    def add_text_watermark(self):
        if self.image:
            text = self.text_entry.get()
            if not text.strip():
                messagebox.showwarning("No Text", "Please enter watermark text.")
                return
            base = self.image.copy()
            draw = ImageDraw.Draw(base)
            # Use a truetype font if available
            try:
                font = ImageFont.truetype("arial.ttf", int(base.height * 0.05))
            except:
                font = ImageFont.load_default()
            textwidth, textheight = draw.textsize(text, font=font)
            # Position: bottom left
            x = 10
            y = base.height - textheight - 10
            draw.text((x, y), text, font=font, fill=(255,255,255,128))
            self.image = base
            self.show_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please upload an image first.")

    def show_image(self, img):
        # Resize for display
        display_img = img.copy()
        display_img.thumbnail((600, 400))
        self.display_image = ImageTk.PhotoImage(display_img)
        self.canvas.delete("all")
        self.canvas.create_image(300, 200, image=self.display_image)

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
            if file_path:
                # Convert to RGB if saving as JPEG
                if file_path.lower().endswith(('.jpg', '.jpeg')):
                    self.image.convert("RGB").save(file_path)
                else:
                    self.image.save(file_path)
                messagebox.showinfo("Saved", f"Image saved to {file_path}")
        else:
            messagebox.showwarning("No Image", "Please upload and watermark an image first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop() 