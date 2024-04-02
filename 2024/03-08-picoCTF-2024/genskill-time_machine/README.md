# Time Machine

### General Skills - 50 points

>**Description:** What was I last working on? I remember writing a note to help me remember... <br>
> The challenge files can be found [here](challenge.zip).
>
>**Hint 1:** The cat command will let you read a file, but that won't help you here! <br>
>**Hint 2:** Read the chapter on Git from the picoPrimer [here](https://primer.picoctf.org/#_git_version_control).<br>
>**Hint 3:** When committing a file with git, a message can (and should) be included.

To begin we are given a zip file called challenge.zip. We unzip it to reveal a file called *drop-in*. When we cd into this directory we find a single file called *message.txt*. The contents of message.txt: `This is what I was working on, but I'd need to look at my commit history to know why...`. 

We know this problem has something to do with [git](https://git-scm.com/) as the *message.txt* refers to [commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History). Commit history is how git allows you to see the changes in the repository over time. The way we can see commit history is using the command `$ git log`. After running this command we get this output.

```bash
commit 3339c144a0c78dc2fbd3403d2fb37d3830be5d94 (HEAD -> master)
Author: picoCTF <ops@picoctf.com>
Date:   Sat Mar 9 21:10:22 2024 +0000

    picoCTF{t1m3----------------}
```

Just like that we get the flag!
