# Mob Psycho
### Foren, 200 points

> Can you handle APKs?
> 
> **Hint 1:** Did you know you can `unzip` APK files? <br>
> **Hint 2:** Now you have the whole host of shell tools for searching these files.

To be honest, I don't know what an APK is, but I didn't need to.

As the hint says, we can run `unzip` on our given `mobpsycho.apk` file, which inflates into a *huge* amount of directories and files.

So naturally, let's search through every file here for "pico" with:

```
grep -Ria "pico" .
```
Note that `-R` is recursive, `-i` ignores case, `-a` gives us text output for binary files, and `.` is our current directory.

This gives us a decently large output, but no flag.

We can try and search for filenames too, with:
```
find | grep "flag"
```
as suggested by [StackOverflow](https://stackoverflow.com/questions/10212192/how-can-i-grep-for-a-filename-instead-of-the-contents-of-a-file). This gives us a much more promising result, returning only a single matching file, `./res/color/flag.txt`.

The contents of `flag.txt` is: `7069636f4354467b6178386d433052553676655f4e5838356c346178386d436c5f37303364643965667d`, which looks like hex, and sure enough, plugging into a hex decoder gives us our flag:

`picoCTF{ax8mC0RU6ve_NX85l4ax8mCl_703dd9ef}`

As a side note, luckily I didn't have to know anything about Mob Psycho to solve this either.
