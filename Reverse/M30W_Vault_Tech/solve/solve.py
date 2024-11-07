import sys
from ctypes import CDLL

libc = CDLL("libc.so.6")
libc.srand(0x574f454d)


content = open(sys.argv[1], "rb").read()
key = content[:16]
cipher = content[16:]

state = []
for i in range(256):
    state.append(i)

j = 0
for i in range(256):
    j = ((libc.rand() % 16) + state[i] + j + key[i % 16])%256
    tmp = state[j]
    state[j] = state[i]
    state[i] = tmp

plain=[]
j = 0
i = 0
for i in range(len(cipher)):
    tmp = state[i]
    state[i] = state[j]
    state[j] = tmp
    plain.append(state[(state[j]+state[i])%256] ^ cipher[i])
    j+=1
    i+=1

print("".join(chr(c) for c in plain))
