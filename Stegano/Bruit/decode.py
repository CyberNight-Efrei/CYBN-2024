import argparse
from PIL import Image
from math import sqrt
from random import randint

parser = argparse.ArgumentParser(prog='Bruit generator')

parser.add_argument('file', type=str, help="Text to embedd")
parser.add_argument('-o', '--output', type=str, default='out.png', help="File to be extracted to")

args = parser.parse_args()

img = Image.open(args.file)
text = ""
data = b""
for i in range(img.size[0]):
	for j in range(img.size[1]):
		if text.endswith("Now, look at this "):
			data += img.getpixel((j,i))[0].to_bytes(1, 'little')
		else:
			text += chr(img.getpixel((j,i))[0])
print(text)
print(len(data), "bytes")

with open(args.output, 'wb') as f:
	f.write(data)