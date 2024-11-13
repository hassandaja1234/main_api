from PIL import Image
import base64
def convert_to_rgb(image):
    return image.convert("RGB")


def read_image_to_bytes(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    return str(image_bytes)
