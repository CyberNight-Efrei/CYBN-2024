from PIL import Image
import sys
import segno
import base64
import argparse
parser = argparse.ArgumentParser()

def chunk(string, parts):
   # Determine the length of each substring
   part_length = len(string) // parts

   # Divide the string into 'parts' number of substrings
   substrings = [string[i:i + part_length] for i in range(0, len(string), part_length)]

   # If there are any leftover characters, add them to the last substring
   if len(substrings) > parts:
      substrings[-2] += substrings[-1]
      substrings.pop()

   return substrings

def generate_qr(data, outfile, **args):
	print(data, outfile)
	qrcode = segno.make_qr(data)
	qrcode.save(
	    outfile,
	    **args
	)

parser.add_argument("--embed", "-e", help="first QR - embedder", required=True)
parser.add_argument("--second", "-s", help="data of second QR", required=True)
parser.add_argument("--outfile", "-o", help="outfile", required=True)
parser.add_argument("--flag", "-f", help="flag data", required=True)
parser.add_argument("--flagfile", "-fo", help="flag file to be exported", required=True)


args = parser.parse_args()

second_file = "second.png"
generate_qr(args.flag, args.flagfile, scale=1, border=0)
generate_qr(args.second, second_file, scale=5, border=0)

img = Image.open(args.flagfile)
embed = Image.open(second_file)
embed = embed.convert("RGBA")

LINES = 25
block_size = embed.size[0]//LINES

# First embed - alpha corner
for i in range(img.size[0]):
	for j in range(img.size[1]):
		c = embed.getpixel((i*block_size, j*block_size))
		color = (c[0],c[1],c[2],255) if img.getpixel((i, j)) == 255 else (c[0],c[1],c[2],254)
		#color = (255,0,0,255) if img.getpixel((i, j)) == 255 else (0,255,0,254)

		position = (i*block_size, j*block_size)
		
		embed.putpixel(position, color)

embed.save(second_file)

with open(second_file, 'rb') as f:
	b64_second = base64.b64encode(f.read()).decode()

parts = chunk(b64_second, 3)
print(b64_second, parts)
generate_qr(parts[0], "top_left.png", scale=1, border=0)
generate_qr(parts[1], "top_right.png", scale=1, border=0)
generate_qr(parts[2], "bottom_left.png", scale=1, border=0)


# Second embed - color corners
LINES = 27

embed = Image.open(args.embed)
embed = embed.convert("RGB")
block_size = embed.size[0]//LINES

embed_pos = [(3*block_size, 3*block_size), (21*block_size, 3*block_size), (3*block_size, 21*block_size)]
size = block_size*3

# TOP LEFT
img = Image.open("top_left.png")

gap = size//img.size[0]
for i in range(img.size[0]):
	for j in range(img.size[1]):
		c = (1,0,0) if img.getpixel((i, j)) == 0 else (0, 0, 0)

		position = (embed_pos[0][0] + i*gap, embed_pos[0][1] + j*gap)
		
		embed.putpixel(position, c)


# TOP RIGHT
img = Image.open("top_right.png")

gap = size//img.size[0]
for i in range(img.size[0]):
	for j in range(img.size[1]):
		c = (0,1,0) if img.getpixel((i, j)) == 0 else (0, 0, 0)
		
		position = (embed_pos[1][0] + i*gap, embed_pos[1][1] + j*gap)
		
		embed.putpixel(position, c)


# BOTTOM LEFT
img = Image.open("bottom_left.png")

gap = size//img.size[0]
for i in range(img.size[0]):
	for j in range(img.size[1],):
		c = (0,0,1) if img.getpixel((i, j)) == 0 else (0, 0, 0)
		
		position = (embed_pos[2][0] + i*gap, embed_pos[2][1] + j*gap)
		
		embed.putpixel(position, c)

embed.save(args.outfile)
