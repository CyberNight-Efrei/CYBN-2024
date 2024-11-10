from requests import Session
from PIL import Image, ImageChops
from io import BytesIO
from base64 import b64decode
import pytesseract

HOST = 'localhost'
PORT = 4001
URL = f'http://{HOST}:{PORT}'
CHARSET = '23456789ACDFGHJKMNPRUWYacdfghjkmnpruwy'

def get_captcha(session: Session) -> Image.Image:
  response = session.get(f'{URL}/api/captcha')
  return Image.open(BytesIO(b64decode(response.content)))

def solve_captcha(session: Session, captcha: Image):
  diff = ImageChops.difference(background, captcha).convert('L')
  diff = diff.point(lambda x: 0 if x < 20 else 0xff)
  code = pytesseract.image_to_string(diff, config=f'-c tessedit_char_whitelist={CHARSET}').strip()
  return session.post(f'{URL}/api/captcha', json={'code': code}).json()

background = Image.open('captcha_bg.png')
session = Session()
session.get(URL)
while True:
  captcha = get_captcha(session)
  response = solve_captcha(session, captcha)
  if 'flag' in response and response['flag']:
    break
print(session.get(URL).text)
print(f'Cookie à mettre dans son navigateur : {session.cookies.get("session")}')
