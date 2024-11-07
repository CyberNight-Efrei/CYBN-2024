import argparse
from PIL import Image
from math import sqrt
from random import randint

parser = argparse.ArgumentParser(prog='Bruit generator')

parser.add_argument('-f', '--file', type=str, help="file to embedd")
parser.add_argument('data', type=str, help="Text to embedd")

args = parser.parse_args()
data = args.data + " Now, look at this :"
shit = b"let's add some more noise hereeeeeeeeeeeee because why this is SOOOOOOO muuuuuch fun to be noiiiiisyyyyyyyyyyyyyyyyyyy. Did you manage to find the noise ? because sometimes noise is not that easy to hear"
file_data = b""
with open(args.file, 'rb') as f:
	temp_data = f.read()
	file_data = temp_data[:len(temp_data)//2] + shit + temp_data[len(temp_data)//2:]
size = int(sqrt(len(data) + len(file_data))) + 1

img = Image.new(size=(size,size), mode="RGB")
k,s = 0,0
for i in range(size):
	for j in range(size):
		if (i*size + j + 2) <= len(data):
			color = (ord(data[i*size + j]), randint(0,255), randint(0,255))
		elif (i*size + j + 2) <= len(data) + len(file_data):
			color = (file_data[k], randint(0,255), randint(0,255))
			k += 1
		else:
			color = (randint(0,255), randint(0,255), randint(0,255))
		img.putpixel((j,i), color)
img.save('noise.png')
