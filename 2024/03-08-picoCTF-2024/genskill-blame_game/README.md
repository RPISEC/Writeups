# Blame Game

### General Skills - 75 points

>**Description:** Someone's commits seems to be preventing the program from working. Who is it? <br>
> The challenge file can be found [here](challenge.zip).
>
>**Hint 1:** In collaborative projects, many users can make many changes. How can you see the changes within one file? <br>
>**Hint 2:** Read the chapter on Git from the picoPrimer [here](https://primer.picoctf.org/#_git_version_control).<br>
>**Hint 3:** You can use `$ python3 <file>.py` to try running the code, though you won't need to for this challenge.

To begin we are given a zip file called challenge.zip. We unzip it to reveal a file called *drop-in*. When we cd into this directory we find a single file called *message.py*. The contents of this file: `print("Hello, World!"`. Just a python file that fails to print "Hello, World!" because there is no closing bracket.

From the description and the title of the challenge we know this challenge has something to do with [git](https://git-scm.com/) and more specifically the [git blame](https://git-scm.com/docs/git-blame) command. Git blame allows you to see who wrote what lines in a file. We can use this to figure out who forgot to close the parenthesis on the python code in *message.py*.

To do this we run the command `$ git blame message.py`. This will tell us what commit the line was changed on, who changed it, what time they changed it, and what they changed it to. This is formatted as `<commit hash> (<git user> <time-stamp>) <changes>`. After we run the git blame command on *message.py* we get this output.

```bash
9ae3e1bc (picoCTF{@sk_th3----------------} 2024-03-09 21:09:01 +0000 1) print("Hello, World!"
```

Here we can see the commit hash was 9a3e1bc, the user is the flag for the challenge, the commit was made on march 9th 2024, and the change is the code is what we see in *message.py*. Now we have the flag!
