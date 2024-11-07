from base64 import b64encode
from io import BytesIO
from random import choices, randint
from PIL import Image, ImageFont, ImageDraw, ImageChops

FONT = ImageFont.truetype(r'assets/Roboto.ttf', 70)
CHARSET = '23456789ACDFGHJKMNPRUWYacdfghjkmnpruwy'
BACKGROUND = Image.open('./assets/captcha_bg.png')
WIDTH = BACKGROUND.width
HEIGHT = BACKGROUND.height
PADDING = 10

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)

def generate() -> tuple[str, Image.Image]:
    captcha = BACKGROUND.copy()
    text = Image.new('RGB', BACKGROUND.size, 'black')
    text_draw = ImageDraw.Draw(text)
    while True:
        passphrase = ''.join(choices(CHARSET, k=8))
        width, height = get_text_dimensions(passphrase, FONT)
        if width < WIDTH:
            break
    x = randint(PADDING, (WIDTH - PADDING * 2) - width)
    y = randint(PADDING, (HEIGHT - PADDING * 2) - height)
    text_draw.text((x, y), passphrase, font=FONT, fill='white')
    captcha.paste(im=ImageChops.invert(BACKGROUND), box=(0, 0), mask=text.convert('L'))

    buffered = BytesIO()
    captcha.save(buffered, format="PNG")

    return passphrase, b64encode(buffered.getvalue())