from Crypto.Cipher import ChaCha20, AES
from pwn import *

CHACHA_KEY = b"ABCDEFGHIJKLMNOPABCDEFGHIJKLMNOP"
NONCE = b"QRSTUVWXYZ12"
chacha_cipher = ChaCha20.new(key=CHACHA_KEY, nonce=NONCE)

def sendline(p, line):
    print(f"sending {line}")
    cipher = chacha_cipher.encrypt(line)
    p.send(cipher)

def recvline(p):
    return chacha_cipher.encrypt(p.recvline())

def recvn(p, n):
    return chacha_cipher.encrypt(p.recv(n))

p = remote("localhost", "8080")

sendline(p, b"HELLO")

aes_key_combo = recvn(p, (32 + 12 + 4) * 2)
print(f"AES:\n{aes_key_combo}")
aes_key_combo = aes_key_combo.split(b"++++")
aes_key = bytearray.fromhex(aes_key_combo[0].decode())
aes_nonce = bytearray.fromhex(aes_key_combo[1].decode())
assert len(aes_key) == 32
assert len(aes_nonce) == 12

print(f"aes key = {aes_key}")
print(f"aes nonce = {aes_nonce}")
sendline(p, b"ESTABLISHED")

flag_cipher = bytearray.fromhex(p.recv().decode())
print(f"flag cipher {flag_cipher}")
aes_cipher = AES.new(aes_key, AES.MODE_GCM, nonce=aes_nonce)
flag = aes_cipher.decrypt_and_verify(flag_cipher[:-16], flag_cipher[-16:])
print(flag)