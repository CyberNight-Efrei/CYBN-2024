from pwn import *
from hashlib import sha256
from itertools import product

context.log_level = 'error'

expected = 0x3d923435fe5b07e4.to_bytes(8, 'little')
indexes = 0xd070c0a0e040919.to_bytes(8, 'little')
mask = b'shadow'
DA_WAY = None
for comb in product('DGHB', repeat=10):
  way = ''.join(comb).encode()
  masked_way = bytes([way[i] ^ mask[i % len(mask)] for i in range(len(way))])
  hash = sha256(masked_way).digest()
  result = bytes([hash[i] for i in indexes])
  if result == expected:
    DA_WAY = way # HHBBGDGDHB
if DA_WAY is None:
  print('DA_WAY not found')
  exit(1)

client = remote('localhost', 8006)
client.recvuntil(b'> ')
client.sendline(b'Knuckles > Sonic')
client.recvuntil(b'> ')
client.sendline(DA_WAY)
print(client.recvall(1).decode())


    