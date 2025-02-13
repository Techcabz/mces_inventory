import os
from flask import request, current_app, url_for
from PIL import Image


def get_inventory_image(image_filename):
    """Returns the correct image URL based on file existence"""
    if not image_filename:  
        return url_for("static", filename="images/not_available.jpg")
    
    image_path = os.path.join(current_app.static_folder, "storage/app", image_filename)
    
    if os.path.exists(image_path):  
        return url_for("static", filename=f"storage/app/{image_filename}")
    
    return url_for("static", filename="images/not_available.jpg")

def compress_image(image_path, max_width=800, quality=85):
    """Compress and convert the image to WebP format."""
    with Image.open(image_path) as img:
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Convert to WebP and save
        webp_path = image_path.rsplit(".", 1)[0] + ".webp"
        img.save(webp_path, "webp", optimize=True, quality=quality)
        return os.path.basename(webp_path) 
