from hashlib import md5
from random import randint
result = []

with open('message.txt', 'r') as f:
	data = f.read()

size, i = 0, 0

while size <= len(data):
	i = randint(1, 3) % len(data)
	hashed = md5(data[size:size+i].encode()).hexdigest()
	result.append(hashed)
	print(data[size:size+i].encode(), hashed)
	size += i

with open('secret_message.txt', 'w') as f:
	f.write('\n'.join(result))