import requests
from io import BytesIO
from typing import Tuple
from PIL import Image, ImageOps, ImageChops


def get_image(url: str, size: Tuple[int, int] = (512, 512), conversion: bool = True):
    buffer = BytesIO(requests.get(url).content)
    if conversion:
        return Image.open(buffer).convert("RGBA").resize(size)
    return Image.open(buffer)


def mask(img: Image, mask: str):
    mask = Image.open("assets/masks/" + mask + ".png").convert("L")
    output = ImageOps.fit(img, mask.size)
    mask = ImageChops.darker(mask, img.split()[-1])
    output.putalpha(mask)
    return output.convert("RGBA")


def valid_avatar_url(url: str):
    if url.startswith("https://cdn.discordapp.com/"):
        return True
