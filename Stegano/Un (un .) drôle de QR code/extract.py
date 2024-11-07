from PIL import Image, ImageDraw
import re
import sys
from pyzbar.pyzbar import decode as qr_decode
from io import BytesIO
import base64

def getimage(content):
	im = Image.open(BytesIO(base64.b64decode(content)))
	return im

BLOCK = '▓'
EMPTY = ' '
NB_BLOCKS = 85
LINES = 27

if len(sys.argv) < 2:
	print(f"Usage: {sys.argv[0]} <embedded file> [output file]")
	exit(1)

img 		= Image.open(sys.argv[1])
block_size	= img.size[0]//LINES
embed_pos 	= [(3*block_size, 3*block_size), (21*block_size, 3*block_size), (3*block_size, 21*block_size)]
size 		= block_size * 3
gap			= size//NB_BLOCKS

QR = []
for p in range(len(embed_pos)):
	QR.append('')
	for i in range(embed_pos[p][0], embed_pos[p][0] + size, gap):
		for j in range(embed_pos[p][1], embed_pos[p][1] + size, gap):
			QR[p] += BLOCK if img.getpixel((i, j))[p] == 1 else EMPTY
			print(QR[p][-1], end='')
		QR[p] += '\n'
		print()
	print('----------------------')

data = ''

for a in range(len(QR)):

	lines = QR[a].split('\n')
	new = Image.new(mode="RGB", size=(block_size*(len(lines)-1), block_size*(len(lines)-1)), color=(255,255,255))
	draw = ImageDraw.Draw(new)

	for i in range(0, len(lines)):
		for j in range(0, len(lines[i])):
			color = (0, 0 ,0) if lines[i][j] == BLOCK else (255, 255, 255)
			draw.rectangle([(i*block_size, j*block_size), (i*block_size+block_size, j*block_size+block_size)], fill=color)

	new.save(f'outfile_{a}.png')
	data += qr_decode(new)[0].data.decode('ascii')
print(data)

getimage(data).save('chall_second.png')

BLOCK = '▓'
EMPTY = ' '
NB_BLOCKS = 25

img = Image.open('chall_second.png')
block_size = img.size[0]//NB_BLOCKS
print(block_size)

QR = ''
for i in range(img.size[0]//block_size):
	for j in range(img.size[1]//block_size):
		QR += BLOCK if img.getpixel((i*block_size, j*block_size))[3] == 254 else EMPTY
		print(QR[-1], end="")
	QR+='\n'
	print()

lines = QR.split('\n')
new = Image.new(mode="RGB", size=(block_size*(len(lines)-1), block_size*(len(lines)-1)), color=(255,255,255))
draw = ImageDraw.Draw(new)

for i in range(0, len(lines)):
	for j in range(0, len(lines[i])):
		color = (0, 0 ,0) if lines[i][j] == BLOCK else (255, 255, 255)
		draw.rectangle([(i*block_size, j*block_size), (i*block_size+block_size, j*block_size+block_size)], fill=color)

output = 'outfile.png'
if len(sys.argv) == 3:
	output = sys.argv[2]

new.save(output)
print("[+] Extracted to", output)
print()
print('[+] Data :', qr_decode(new)[0].data.decode())