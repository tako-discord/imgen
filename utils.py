import requests
from io import BytesIO
from typing import Tuple
from PIL import Image, ImageOps

def get_image(url: str, size: Tuple[int, int]=(512, 512)):
    buffer = BytesIO(requests.get(url).content)
    return Image.open(buffer).convert("RGBA").resize(size)

def mask(img: Image, mask: str):
    mask = Image.open('assets/masks/' + mask + ".png").convert('L')
    output = ImageOps.fit(img, mask.size)
    output.putalpha(mask)
    return output.convert("RGBA")
