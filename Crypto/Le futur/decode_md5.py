from string import printable
from itertools import product
from hashlib import md5
import json

hashes = {}

for i in range(1,4):
	permutation = list(product(printable, repeat=i))
	for perm in permutation:
		current = ''.join(perm)
		current_md5 = md5(current.encode()).hexdigest()
		hashes.update({current_md5: current})

with open('hashes.txt', 'w') as f:
	f.write(json.dumps(hashes))

with open('secret_message.txt', 'r') as f:
	tbd = f.read().split('\n')

decoded_message = ''

for code in tbd:
	try:
		decoded_message += hashes[code]
	except:
		print('Error:', code)
print(decoded_message)