## PicoCTF 2024 RE FactCheck 200 Points

When you open this challenge, you get a file called [bin](bin), and this description:

> #### Description
>This binary is putting together some important piece of information... Can you uncover that information? Examine this file. Do you understand its inner workings?

But of course, like the connoisseur of reverse engineering you are, you look at hints as the first thing you do. Well do I have good news for you!

> #### Hints
>(None)

Let's get to work.

It looks like garbage if you just open it, and you can run this file... you know what that means! Open it up in IDA or Ghidra; for this specfic challenge, IDA finds refrences to the important information much better, so I'd recommend it over Ghidra (though I like how Ghidra does the conditional statements better, so I actually went back and forth using the strengths of both). Each have their nuances and finding which you like better will be good for more RE challenges.

The first thing I do when I open the file in IDA is press *FN-F5*, this will open up the Pseudocode of the main function.\
Now that I am looking at the code more readably, I see when opening bin up in IDA is the part of the flag:

```
std::allocator<char>::allocator
(&v21, "picoCTF{wELF_d0N3_mate_", v3);
```

This is just the start of the flag... this challenge can't be that easy.

Looking through more of the code, we see a lot of random looking functions with weird inputs, but looking at the most common ones can give us a better understanding of what the function is doing.\
The most common functions I'm seeing right now are:

```
This:
std::__cxx11::basic_string<char,std::char_traits<char>,
std::allocator<char>>::basic_string(v38, "8", &v21);
And This:
std::allocator<char>::~allocator(&v21);
```

These don't really make a lot of sense, but looking at what actually matters, you can see the `allocator` keyword. \
The first one is just the construction of a string, specifically the allocation of it\
The second one is the destructor\
In both cases, we don't have to worry about them :P

What we do need to worry about are what comes after all of the allocations: the if statements that will append specific values to the flag.

Here is the whole of what we need to consider (from IDA's Pseudocode):

```
if ( *(cr_traits<char>,std::allocator<char>>::operator[](v24, 0LL) <= 65 )
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, v34);
if ( *(_BYTE *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator[](v35, 0LL) != 65 )
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, v37);
if ( "Hello" == "World" )
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, v25);
v19 = *(char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator[](v26, 0LL);
if ( v19 - *(char *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator[](v30, 0LL) == 3 )
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, v26);
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, v25);
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, v28);
if ( *(_BYTE *)std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator[](v29, 0LL) == 71 )
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, v29);
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, v27);
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, v36);
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, v23);
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, v31);har *)std::__cxx11::basic_string<char,std::cha
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator+=(v22, 125LL);
```

You can just read this with all of the garbage, but the first thing I would do is just clean this up a bit:

```c#
if (operator[](v24, 0LL) <= 65 )
  operator+=(v22, v34);

if (operator[](v35, 0LL) != 65 )
  operator+=(v22, v37);

if ( "Hello" == "World" )
  operator+=(v22, v25);

v19 = operator[](v26, 0LL);
if ( v19 - operator[](v30, 0LL) == 3 )
  operator+=(v22, v26);

operator+=(v22, v25);
operator+=(v22, v28);

if (operator[](v29, 0LL) == 71 )
  operator+=(v22, v29);

operator+=(v22, v27);
operator+=(v22, v36);
operator+=(v22, v23);
operator+=(v22, v31);
operator+=(v22, 125LL);
```

This looks much better, but all of the `v__`'s don't look very nice, so we can refrence what we see in the code just above this to fill in these values:\
 (also if you don't know what to do with the decimal values that are compared to strings, it is almost always the ascii equivelant, check this [image](ASCII-Table.png) for these values)

```c#
v23 = "9"
v24 = "5"
v25 = "a"
v26 = "3"
v27 = "c"
v28 = "9"
v29 = "a"
v30 = "e"
v31 = "5"
v32 = "d"
v33 = "b"
v34 = "9"
v35 = "6"
v36 = "b"
v37 = "3"
v38 = "8"
```

I have simplified this a bit but all I did was look at the assignments of the values we care about.
\
Replaing the refrences to these values and interpreting the `operator[](_, 0)` as just the value itself, and the `operation+=` as refrencing the flag and adding to it we get:
<!-- erl delphi -->
``` c#
if ('a') <= 'A' ) //true
  FLAG += '9';

if ("6") != 'A' ) //true
  FLAG += '3';

if ( "Hello" == "World" ) //false
  FLAG += 'a';

v19 = '3';
if ('3' - 'e' == 3 ) //'3' - 'e' = 51 - 101 != 3 false
  FLAG += '3';

FLAG += 'a';
FLAG += '9';

if ('a') == 'G' ) //false
  FLAG += 'a';

FLAG += 'c';
FLAG += 'b';
FLAG += '9';
FLAG += '5';
FLAG += '}';
```

From this you should be able to get the flag

<!-- picoCTF{wELF_d0N3_mate_93a9cb95} -->