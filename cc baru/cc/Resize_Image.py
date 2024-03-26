from PIL import Image
import os

def resize_images(folder_path, new_width=216, new_height = 216):
    """Resizes all images in the specified folder to the given width."""

    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            img = Image.open(os.path.join(folder_path, filename))
            # Resize image while maintaining aspect ratio
            width, height = img.size
            img = img.resize((new_width, new_height))
            # Save resized image with "resized_" prefix
            img.save(os.path.join(folder_path, f"{filename}"))
            print(f"Resized: {filename}")

# Specify the folder path containing images
folder_path = "D:\kuliah\FC\images"  # Replace with your actual folder path

# Resize images with a new width of 400 pixels (adjust as needed)
resize_images(folder_path, new_width=400, new_height=512)
