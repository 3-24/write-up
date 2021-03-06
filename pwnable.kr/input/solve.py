from pwn import *
import os

context.log_level='debug'

input_path = './input'                  # For local environment
# input_path = '/home/input2/input'     # For running on provided pwnable.kr server

argvs = ["" for i in range(0,100)]
argvs[ord('A')] = '\x00'
argvs[ord('B')] = '\x20\x0a\x0d'
argvs[ord('C')] = '64123'

stderr,stderw = os.pipe()

p = process(executable = input_path, argv = argvs, stderr=stderr, env={b"\xde\xad\xbe\xef":b"\xca\xfe\xba\xbe"})

p.recvuntil("Stage 1 clear!\n")
print("Stage 1 clear!")

p.send(b"\x00\x0a\x00\xff")
os.write(stderw, b"\x00\x0a\x02\xff")

p.recvuntil("Stage 2 clear!\n")
print("Stage 2 clear!")

p.recvuntil("Stage 3 clear!\n")
print("Stage 3 clear!")

with open("\x0a","w+") as f:
    f.write(b"\x00\x00\x00\x00")

p.recvuntil("Stage 4 clear!\n")
print("Stage 4 clear!")

print(p.poll())     # wait for opening sockets. It should print None if successful.
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 64123))

sock.send(b"\xde\xad\xbe\xef")

p.recvuntil("Stage 5 clear!\n")
print("Stage 5 clear!")
print(p.recvall())