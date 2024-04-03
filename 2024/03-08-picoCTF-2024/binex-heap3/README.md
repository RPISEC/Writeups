## PicoCTF 2024 Binary Exploitation heap 3 200 Points

When you open this challenge, you get two files -- the binary and a copy of the source code -- called [chall](chall) and [chall.c](chall.c), with this description:

> #### Description
> This program mishandles memory. Can you exploit it to get the flag?
> Additional details will be available after launching your challenge instance.

If you want to see the hints:

<details close>
<summary> <b>Hints</b> </summary>

> (1) Check out "[use after free](https://encyclopedia.kaspersky.com/glossary/use-after-free/)"
</details>


At this point I'm going to assume that you have at least read on of [heap0](../binex-heap0/README.md) [heap1](../binex-heap1/README.md) or [heap2](../binex-heap2/README.md) (sorry)


Lets look at the new functions of interest:

`alloc_object()` \
Alright, this function will allocate a specified amount of space for the user, and then will fill that space with... well actually the scan for input doesn't stop you from overflowing your own buffer. So that is a good thing to know. \
Overall this function seems simple, and it is, but it allows us to put any data anywhere we want in heap memory, as long as it fits - which we will get back to later.

`free_memory()` \
Very simple, it free's `x`............................... well hold on a second here. There are some VERY important concepts to take away form this, and is very important for concepts such as heap poisoning, double free's, and (what we care about) use after frees \
Let's think about some of the consequences of freeing x. \
Well, what is x? It is an object of size 35 sure. It has three segments of 10 and one of 5, also yes. But it is also a global variable that is refrenced in many different functions. So, I ask you even though I know you will just read the answer, what is going to happen when we free x? \
I'll tell you what! We are going to be accessing this freed memory even though we shouldn't be, soooo if something gets allocated where x should be, what will we be reading when we check `x-->flag`? \
Oh yeah baby, we got our exploit


`check_win()` \
An inportant function, with one difference: `if(!strcmp(x-->flag, "pico))` \
We need to set the flag part of `x` to pico, and with what we know about use after free's, we got this.

Well actually hold up there. A concept that is weird, seemingly inconsistent, and just annoying, is how the allocator decides where to put what memory. Currently, we have `num_allocs`, `object *x`, and `choice`. What is going to matter? Honestly, there isn't a lot I can tell you for sure because it just isn't always consistent with what I would tell you. My best advise for finding where something is going to be allocated is two part: \
- If Struct A was size 64, and after we free A, we allocate B of size 64, it will most likly take the place of A
- If values will align nicely (64, 32, 16, 8), they may be placed inside of each other (if they are free of course)

If you actually want to know hw the C allocator works, I highly recommend looking up papers on google scholar or trying to find an actual explaination of the C allocation in specific. It is a topic you will be able to find info about.

But for our purposes, we just need to know the size of the allocation of x, and match that. As that will land in the same place 100% of the time _90% of the time_.

I recommend actually playing around with different sizes and seeing where they end up. Just input random amounts of A's and look for 0x41 in your memory with gdb. These are the commands and inputs I put to do this:
```
$ gdb chall
(gdb) r
Starting program: /heap/3/chall 

freed but still in use
now memory untracked
do you smell the bug?

1. Print Heap
2. Allocate object
3. Print x->flag
4. Check for win
5. Free x
6. Exit

Enter your choice: 2
Size of object allocation: 16
Data for flag: AAAABBBB

1. Print Heap
2. Allocate object
3. Print x->flag
4. Check for win
5. Free x
6. Exit

Enter your choice: ^C
Program received signal SIGINT, Interrupt.
(gdb) x/15x x
0x20b66b0:      0x00000000      0x00000000      0x00000000      0x00000000
0x20b66c0:      0x00000000      0x00000000      0x00000000      0x69620000
0x20b66d0:      0x00006f63      0x00000000      0x00000411      0x00000000
0x20b66e0:      0x41414141      0x42424242      0x0000000a
```

Now that you have played around with memory on the heap, lets get the flag. This is going to be just the ordering of what we have talked about:\
1. Free `x`
    - Know why you are doing this! What is the goal of freeing it, what steps do we take after?
2. Allocate something the same size as `x`
    - Why the same size? Why not less, we can overflow the buffer after all? Knowing this will help in the future
3. Write into that something
    - To find what to write, follow the same process as you did you heap2: play around with inputs, count how big the offset is from the beginning of x is to the end, use gdb to examine memory. You have the tools!
4. Profit
    - Get those flags!

Here is what my run of getting the flag looked like

#### OH YEAH!
I almost forgot, sometimes running the solve on the chall binary on webshell or locally won't actually tell you you won, if you are seeing signs that you won, but aren't try it on the nc they give you! 

```
freed but still in use
now memory untracked
do you smell the bug?

1. Print Heap
2. Allocate object
3. Print x->flag
4. Check for win
5. Free x
6. Exit

Enter your choice: 5
1. Print Heap
2. Allocate object
3. Print x->flag
4. Check for win
5. Free x
6. Exit

Enter your choice: 2
Size of object allocation: 35
Data for flag: * b'A'*30 + b"pico\n" * 
1. Print Heap
2. Allocate object
3. Print x->flag
4. Check for win
5. Free x
6. Exit

Enter your choice: 4
YOU WIN!!11!!
picoCTF{now_thats_free_real_estate_--------}
```
