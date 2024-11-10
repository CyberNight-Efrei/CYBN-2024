from pwn import *
from hashlib import md5

context.log_level = 'error'

def generate_key(id: int) -> str:
  key = str(id).encode()
  for _ in range(30):
    key = md5(key).digest()
  return key.hex()

client = remote('localhost', 3001)
client.recvuntil(b'> ')

client.sendline(b'credits')
data = client.recvuntil(b'> ').decode()
admin_id = int(data.split('admin : n°')[1].split('\n', 1)[0])
admin_key = generate_key(admin_id)

client.sendline(str(admin_id).encode())
client.recvuntil(b'> ')
client.sendline(admin_key.encode())
print(client.recvall(timeout=1).decode())
