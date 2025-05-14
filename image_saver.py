# Image Filter and Format Converter Web Application
# CST 205
# This file has the function that enables users to save images in different formats. 
# It takes in a pillow image object, and a string for the desired format and saves in in that format
# Ciaran
# 5/14/2025

import os
import io
from PIL import Image


def get_image_download(image: Image.Image, file_type: str, filename: str) -> tuple[io.BytesIO, str, str]:
    
    img_io = io.BytesIO()

    pil_format = file_type.upper()
    if pil_format == 'JPG':
        pil_format = 'JPEG'

    image.save(img_io, format=pil_format)
    img_io.seek(0)
    mimetype = f"image/{file_type.lower()}"
    download_name = f"{filename}.{file_type.lower()}"
    return img_io, mimetype, download_name
    
