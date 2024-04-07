# My Favorite Flag
REV - 100 points

We are given the source code for a password checker.

It uses a simple XOR operation with some funny array indexing to check your input. 

I reversed the XOR operation and printed the output:

![image](https://github.com/RPISEC/Writeups/assets/29514104/9e800e22-2199-4c49-8fad-6201223387d7)

I also removed the initial if-statement that checks to see if you inputted the fake flag.
I then recompiled the program and provided the fake flag as input, which revealed the real one.
