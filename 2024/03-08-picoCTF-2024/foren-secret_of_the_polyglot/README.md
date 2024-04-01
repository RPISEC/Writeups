# Secret of the Polyglot
### Foren, 100 points

> The Network Operations Center (NOC) of your local institution picked up a suspicious file, they're getting conflicting information on what type of file it is. They've brought you in as an external expert to examine the file. Can you extract all the information from this strange file? <br>
> 
> **Hint:** This problem can be solved by just opening the file in different ways

We're given a file, `flag2of2-final.pdf`. If we open the file, we can see:

![2nd Part of Flag](flag2.png)

`1n_pn9_&_pdf_2a6a1ea8}`, the back half of the flag, so we're already half way there!

Let's further inspect this file. Running `file`, we find:

![Output](output.png)

So this file is *really* a .png in disguise.

I ran `cp flag2of2-final.pdf flag.png` to copy our given file to a png file with the name "flag", and opened it, receiving:

![1st Part of Flag](flag.png)

`picoCTF{f1u3n7_`, the first part of the flag.

`picoCTF{f1u3n7_1n_pn9_&_pdf_2a6a1ea8}`
