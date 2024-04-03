## PicoCTF 2024 Binary Exploitation heap 2 200 Points

When you open this challenge, you get two files -- the binary and a copy of the source code -- called [chall](chall) and [chall.c](chall.c), with this description:

> #### Description
> Can you handle function pointers?
> Additional details will be available after launching your challenge instance.

If you want to see the hints:

<details close>
<summary> <b>Hints</b> </summary>

> (1) Are you doing the right endianness?
</details>

The first thing I do, is open the c file to understand the code, which is pretty self explanitary: you are just using a simple menu to edit heap data. Lets talk about the functions one by one.

`win()` \
Well I think I found what we are meant to do. But really, looking at the file, it simply gives us the answer - Great!

`check_win` \
This is what gets called when we to print the flag (choice 4). In the function, it just calls `x`. Seeing this makes me think that we have to overwrite `x` to point to `win()`

`print_menu()` \
Pretty simple, just prints the menu for the user. Nothing of interest.

`init()` \
We see that the input data is allocated to be 5 long, though we will be using Ghidra for offsets, as I think it makes things easier.

`write_buffer()` \
Alright, now to the actual functions. First thing we should see is that there is no limit on how much we can write to the buffer. \
This should be a huge red flag to you that this is something you could potentially use for an exploit.

`print_heap()` \
Nice function that will show us where the input_data and x live. Nice for calculating offsets (maybe we won't need Ghidra after all)

Finally `main()` \
Prints the menu, gets our choice, and calls the correct function.

Lets get hacking.

First thing I do is just play with the input. See if I can get an overflow that will modify `x`

And lo and behold, it was very simple:

```
I have a function, I sometimes like to call it, maybe you should change it

1. Print Heap
2. Write to buffer
3. Print x
4. Print Flag
5. Exit

Enter your choice: 2
Data for buffer: oiwehfouhewofuhewofuhewofuhwefouhewoufhewofuhwoehufwoeufh

1. Print Heap
2. Write to buffer
3. Print x
4. Print Flag
5. Exit

Enter your choice: 1
[*]   Address   ->   Value
+-------------+-----------+
[*]   0x559927d336b0  ->   oiwehfouhewofuhewofuhewofuhwefouhewoufhewofuhwoehufwoeufh
+-------------+-----------+
[*]   0x559927d336d0  ->   hewoufhewofuhwoehufwoeufh
```

If you do the math or just play around, you find that you need to have 32 garbage values before you overwrite `x`

Now what to overwright `x` to be? Why not the `win` function! \
We don't even need to look at Ghidra, we can just run gdb and run `p win`. This will print the address of the `win` function.

Now that we have that, all we have to do is make a python script to write the output to the file and bam boom pow!

#### OH YEAH!
I almost forgot, sometimes running the solve on the chall binary on webshell or locally won't actually tell you you won, if you are seeing signs that you won, but aren't try it on the nc they give you! 

```
I have a function, I sometimes like to call it, maybe you should change it

1. Print Heap
2. Write to buffer
3. Print x
4. Print Flag
5. Exit

Enter your choice: Data for buffer: 
1. Print Heap
2. Write to buffer
3. Print x
4. Print Flag
5. Exit

Enter your choice: [*]   Address   ->   Value   
+-------------+-----------+
[*]   0x171b2b0  ->   AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA@
+-------------+-----------+
[*]   0x171b2d0  ->   @

1. Print Heap
2. Write to buffer
3. Print x
4. Print Flag
5. Exit

Enter your choice: 

x = @


1. Print Heap
2. Write to buffer
3. Print x
4. Print Flag
5. Exit

Enter your choice: picoCTF{and_down_the_road_we_go_--------}
```

