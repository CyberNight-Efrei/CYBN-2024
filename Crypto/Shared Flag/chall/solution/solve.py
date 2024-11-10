from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import unpad
import primefac
import random
import hashlib

def decrypt_flag(shared_secret: int, encrypted: bytes) -> str:
  key = hashlib.md5(long_to_bytes(shared_secret)).digest()
  cipher = AES.new(key, AES.MODE_ECB)
  return unpad(cipher.decrypt(encrypted), AES.block_size).decode()

context.log_level = 'error'

client = remote('localhost', 3002)

# Get g
client.recvuntil(b'g : ')
g = int(client.recvline())
client.recvuntil(b'p : ')
p = int(client.recvline())
client.recvuntil(b'> ')

# Check that p is prime and factor p-1.
if not primefac.isprime(p):
  print("The provided modulus is not prime!")
  exit(1)
factors = primefac.primefac(p - 1)

# Most likely 2 is a factor and thus provides a subgroup of size 2 but this generalises it.
seen_factors = set()
for factor in factors:
  if factor in seen_factors:
    continue
  seen_factors.add(factor)

  # Test 1000 integers.
  for i in range(1000):
    generator_candidate = random.randrange(2, p - 1)
    candidate = pow(generator_candidate, (p - 1) // factor, p)
    if candidate != (p - 1) and candidate != 1:
      # Find the possible shared values.
      possible_shared = set()
      ctr = 1
      max_ctr = 100
      while len(possible_shared) != factor and ctr < max_ctr:
        possible_shared.add(pow(candidate, ctr, p))
        ctr += 1
    
      if ctr >= max_ctr:
        continue
      
      # Now that we have all we need to predict the possible shared secrets, send the candidate.
      print(f'Candidate {candidate} has {len(possible_shared)} elements in subgroup: {possible_shared}')
      client.sendline(str(candidate).encode())
      client.recvuntil(b'Ton flag : ')
      encrypted_flag = bytes.fromhex(client.recvline().decode())
      print(f'Encrypted flag: {encrypted_flag.hex()}')
      
      for shared_secret in possible_shared:
        try:
          possible_flag = decrypt_flag(shared_secret, encrypted_flag)
          if 'CYBN{' in possible_flag:
            print(f'Shared secret: {shared_secret}')
            print(f'Flag: {possible_flag}')
            exit(0)
        except Exception:
          pass
      print('No shared value found, please restart.')
      exit(2)

