import os
import io
from PIL import Image

def save_image_to_folder(image: Image.Image, file_type: str, filename: str, folder: str = "saved_images") -> str:

    os.makedirs(folder, exist_ok=True)

    output_path = os.path.join(folder, f"{filename}.{file_type.lower()}")

    pil_format = file_type.upper()
    if pil_format == 'JPG':
        pil_format = 'JPEG'

    image.save(output_path, format=pil_format)
    print(f"Image saved to {output_path}")
    return output_path


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
    
