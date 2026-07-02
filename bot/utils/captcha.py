import random
import string
from io import BytesIO
from captcha.image import ImageCaptcha

def generate_captcha():
    """Generates a random captcha and returns (text, image_bytes)"""
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    image = ImageCaptcha(width=280, height=90)
    data = image.generate(captcha_text)
    return captcha_text, data.getvalue()
