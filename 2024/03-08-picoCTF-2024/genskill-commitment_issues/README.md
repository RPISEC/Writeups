# Commitment Issues

### General Skills - 50 points

>**Description:** I accidentally wrote the flag down. Good thing I deleted it! <br>
> The challenge files can be found [here](challenge.zip).
>
>**Hint 1:** Version control can help you recover files if you change or lose them! <br>
>**Hint 2:** Read the chapter on Git from the picoPrimer [here](https://primer.picoctf.org/#_git_version_control).<br>
>**Hint 3:** You can 'checkout' commits to see the files inside them.

To begin we are given a zip file called challenge.zip. We unzip it to reveal a file called *drop-in*. When we cd into this directory we find a single file called *message.txt*. The contents of message.txt: `TOP SECRET`. Not much info here...

At this point many would give up unless they knew what [git](https://git-scm.com/) was. Intuitively if you have heard of git you would know from the challenge name that it has something to do with [committing](https://git-scm.com/docs/git-commit). You can see the [commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History) of a git repository using the command `$ git log`. The commit history is how git keeps track of the changes made to the repository over time. This is what it output after we run this command.

```bash
commit 3899edb7f3110d613c72ad40083fd8feeef703d0 (HEAD -> master)
Author: picoCTF <ops@picoctf.com>
Date:   Sat Mar 9 21:09:58 2024 +0000

    remove sensitive info

commit 6603cb4ff0c4ea293798c03a32e0d78d5ab12ca2
Author: picoCTF <ops@picoctf.com>
Date:   Sat Mar 9 21:09:58 2024 +0000

    create flag
```

Here we can see all the past commits of this git repository. The current commit we are at is 3899eb. We can see the commit message for this is "remove sensitive info" which tells us that the previous commit probably has something.

To go back in the commit history there are a few commands we can do, both use the [checkout](https://git-scm.com/docs/git-checkout) function. The simplest to use when you know the commit hash code is `$ git checkout <hash>` which is 6603c in this case. Another we can use in this situation is `$ git checkout HEAD~1` which will bring us one commit back from the current commit.

After we run either of these commands we will be at the 6630c commit. So if we run git log we will see this

```bash
commit 6603cb4ff0c4ea293798c03a32e0d78d5ab12ca2 (HEAD)
Author: picoCTF <ops@picoctf.com>
Date:   Sat Mar 9 21:09:58 2024 +0000

    create flag
```

Now when we list files we will see our *message.txt* file which we can then read to see the flag: `picoCTF{s@n1--------------}`.
