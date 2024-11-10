from pwn import *

context.log_level = 'error'

def encrypt(client: remote, hexa: str) -> bytes:
  client.sendline(hexa.encode())
  data = client.recvuntil(b'> ').decode()
  encrypted = bytes.fromhex(data.splitlines()[0])
  return encrypted

client = remote('localhost', 3000)
client.recvuntil(b'> ')

FLAG_CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#$-?!@_{}'
flag = ''
while not flag.endswith('}') and len(flag) < 32:
  base = '00' * (32 - len(flag) - 1)
  expected = encrypt(client, base)
  found = False
  for c in FLAG_CHARSET:
    encrypted = encrypt(client, f'{base}{flag.encode().hex()}{ord(c):0>2X}')
    if encrypted[:32] == expected[:32]:
      flag += c
      found = True
      print(flag)
      break
  if not found:
    print('Not found')
    break