## PicoCTF 2024 Binary Exploitation heap 0 50 Points

When you open this challenge, you get two files -- the binary and a copy of the source code -- called [chall](chall) and [chall.c](chall.c), with this description:

> #### Description
> Are overflows just a stack concern?
> Additional details will be available after launching your challenge instance.

If you want to see the hints:

<details close>
<summary> <b>Hints</b> </summary>

> (1) What part of the heap do you have control over and how far is it from the safe_var?
</details>


The first thing I do, is open the c file to understand the code, which is pretty self explanitary: you are just using a simple menu to edit heap data. Lets talk about the functions one by one.

`check_win()` \
This function will check if the `safe_var` is correct, and if not, we win!

`print_menu()` \
Pretty simple, just prints the menu for the user. Nothing of interest.

`init()` \
Prints the menues, and sets the `input_data` and `safe_var`. Nothing really of interest either.

`write_buffer()` \
Alright, now to the actual functions. First thing we should see is that there is no limit on how much we can write to the buffer. \
This should be a huge red flag to you that this is something you could potentially use for an exploit.

`print_heap()` \
Nice function that will show us where the input_data and x live. Nice for calculating offsets (maybe we won't need Ghidra after all)

Finally `main()` \
Prints the menu, gets our choice, and calls the correct function.

Lets get hacking.

The first thing we saw - `check_win()` - is, I think, going to be our golden goose. We just need to change `x`

Looking for a way to do that we have to understand what the [heap](https://www.techtarget.com/whatis/definition/heap) is, and what an [overflow](https://en.wikipedia.org/wiki/Buffer_overflow) is. \
Simply put: the heap is a collection of memory that is not on the stack, but we can ask to use for our program. An overflow is when a buffer we make (or an array of data, be it a string or otherwise) tries to hold too much data, thus overflowing the length of the buffer.

With that being said, we can see from the initial print statement:
```
Heap State:
+-------------+----------------+
[*] Address   ->   Heap Data   
+-------------+----------------+
[*]   0x6502389482b0  ->   pico
+-------------+----------------+
[*]   0x6502389482d0  ->   bico
+-------------+----------------+
```
that the two points of interest are very close to eachother. This combined with what we know about `write_buffer()` - that we can put an arbitrary amount of data into the buffer - means that we have the perfect situation for an overflow.

Once we do this, we can do whatever we want with the `"safe_var"` and get the flag!

#### OH YEAH!
I almost forgot, sometimes running the solve on the chall binary on webshell or locally won't actually tell you you won, if you are seeing signs that you won, but aren't try it on the nc they give you! 


```
Welcome to heap0!
I put my data on the heap so it should be safe from any tampering.
Since my data isn't on the stack I'll even let you write whatever info you want to the heap, I already took care of using malloc for you.

Heap State:
+-------------+----------------+
[*] Address   ->   Heap Data   
+-------------+----------------+
[*]   0x6502389482b0  ->   pico
+-------------+----------------+
[*]   0x6502389482d0  ->   bico
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
[*]   0x6502389482b0  ->   AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAY
+-------------+----------------+
[*]   0x6502389482d0  ->   YAY
+-------------+----------------+

1. Print Heap:          (print the current state of the heap)
2. Write to buffer:     (write to your own personal block of data on the heap)
3. Print safe_var:      (I'll even let you look at my variable on the heap, I'm confident it can't be modified)
4. Print Flag:          (Try to print the flag, good luck)
5. Exit

Enter your choice: 

Take a look at my variable: safe_var = YAY


1. Print Heap:          (print the current state of the heap)
2. Write to buffer:     (write to your own personal block of data on the heap)
3. Print safe_var:      (I'll even let you look at my variable on the heap, I'm confident it can't be modified)
4. Print Flag:          (Try to print the flag, good luck)
5. Exit

Enter your choice: 
YOU WIN
picoCTF{my_first_heap_overflow_--------}
```

