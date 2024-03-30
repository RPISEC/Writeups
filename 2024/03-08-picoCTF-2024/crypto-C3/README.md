PicoCTF 2024 Crypto
C3 
200 Points

Description refers to this as The Custom Cyclical Cipher, provides downloads to the ciphertext and convert.py files.
Hint: Modern crypto schemes don't depend on the encoder to be secret, but this one does.

I began by looking at convert.py.
```python
import sys
chars = ""
from fileinput import input
for line in input():
  chars += line

lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

out = ""

prev = 0
for char in chars:
  cur = lookup1.index(char)
  out += lookup2[(cur - prev) % 40]
  prev = cur

sys.stdout.write(out)
```

This seemed simple enough to reverse - so I wrote the following script.
```python
lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

enc = "DLSeGAGDgBNJDQJDCFSFnRBIDjgHoDFCFtHDgJpiHtGDmMAQFnRBJKkBAsTMrsPSDDnEFCFtIbEDtDCIbFCFtHTJDKerFldbFObFCFtLBFkBAAAPFnRBJGEkerFlcPgKkImHnIlATJDKbTbFOkdNnsgbnJRMFnRBNAFkBAAAbrcbTKAkOgFpOgFpOpkBAAAAAAAiClFGIPFnRBaKliCgClFGtIBAAAAAAAOgGEkImHnIl"
message = ""
prev = 0
for char in enc:
  cur = lookup2.index(char)
  message += lookup1[(cur + prev) % 40]
  prev = (cur + prev) % 40
print(message)
```

The decrypted message itself is python code.
```python
#asciiorder
#fortychars
#selfinput
#pythontwo

chars = ""
from fileinput import input
for line in input():
    chars += line
b = 1 / 1

for i in range(len(chars)):
    if i == b * b * b:
        print chars[i] #prints
        b += 1 / 1
```

This references selfinput and seems to open the same file that the convert.py encrypts, so I modified my script above to do the same in python3
```python
flag = ""
b = 1
for i in range(len(message)):
    if i == b * b * b:
        flag += message[i]
        b += 1
print("picoCTF{" + flag + "}")
```
which yielded picoCTF{adlibs}
