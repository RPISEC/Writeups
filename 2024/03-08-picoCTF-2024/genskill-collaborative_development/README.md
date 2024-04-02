# Collaborative Development

### General Skills - 75 points

>**Description:** My team has been working very hard on new features for our flag printing program! I wonder how they'll work together? <br>
> The challenge files can be found [here](challenge.zip).
>
>**Hint 1:** `git branch -a` will let you see available branches. <br>
>**Hint 2:** How can file 'diffs' be brought to the main branch? Don't forget to `git config`!<br>
>**Hint 3:** Merge conflicts can be tricky! Try a text editor like nano, emacs, or vim.

To begin we are given a zip file called challenge.zip. We unzip it to reveal a file called *drop-in*. When we cd into this directory we find a single file called *flag.py*. The contents of this file: `print("Printing the flag...")`. It does not print the flag when you run the file...

From the description and the title of the challenge we know this challenge has something to do with [git](https://git-scm.com/) and more specifically collaboration on git. Git allows multiple people to contribute to a codebase at the same time via a [remote](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes), think of this as a repository on someone elses computer that everyone makes changes to.

It gets messy when everyone makes changes to the same files so often times people will make a [branch](https://git-scm.com/docs/git-branch) which allows you to copy all the files of a commit and alter them without changing the original copy. To see all the branches this repository has we can run the command `$ git branch -a`. We get this output.

```bash
  feature/part-1
  feature/part-2
  feature/part-3
* main
```

There are 4 total branches in this repository. The '*' next to main means we are currently looking at the main branch. To look at other branches we use the [checkout](https://git-scm.com/docs/git-checkout) command. Let's look at branch feature/part-1, to do this we run `$ git checkout feature/part-1`. This then alters our directory to show the files on the feature/part-1 branch.

If we list files we find another *flag.py* files. This time the contents are different: `print("picoCTF{t3@mw0rk_", end='')`. We have the first part of the flag! This is not it as we need check out all the other branches to get the rest of the flag. At this point you can repeat the process for every other branch the flag. If you want to learn about merging and conflicts keep reading!

#### Merges and Conflicts

So another way to get all content of the *flag.py* files in one place is to [merge](https://git-scm.com/docs/git-merge) the different branches. Merging branches is a way to get the code from two different branches on a single one. Since we know branches feature/part-1:3 different parts of the flag we can merge all these branches together. To do this make sure you checkout main them run the command `$ git merge feature/part-1`. This will take the code in part-1's *flag.py* and put it in the *flag.py* file of the main branch.

After running the command this should appear on your terminal.

```bash
Updating eb4de2a..ad37f59
Fast-forward
 flag.py | 1 +
 1 file changed, 1 insertion(+)
```

If we then check the contents of *flag.py* we will see it has been updated to this

```py
print("Printing the flag...")
print("picoCTF{t3@mw0rk_", end='')
```

We can then repeat this process for feature/part-2. So we run `$ git merge feature/part-2`. This is what the terminal outputs.

```txt
Committer identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.
```

So we've run into an issue. Git does not know who we are. When contributing to a repository git wants to keep track of who is changing what and user.email and user.name is what it uses to figure out who is who. To merge these two branches we need to set out email and name. We can run the following commands to do so.

```bash
$ git config --global user.email temp@example.com
$ git config --global user.name temp
```

We have set our email to 'temp@example.com' and our name to 'temp'. When we add the `--global` flag it sets it for all git repositories on our machine. If you have multiple projects with different credentials you can use the `--local` flag to set it on a repository basis.

Now that we have set our credentials we can now re-run `$ git merge feature/part-2`. Then our terminal outputs this.

```txt
Auto-merging flag.py
CONFLICT (content): Merge conflict in flag.py
Automatic merge failed; fix conflicts and then commit the result.
```

This means we have a [merge conflict](https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging). A merge conflict means the code in both branches have conflicting information. If we open the file up we will see the following code.

```py
print("Printing the flag...")
<<<<<<< HEAD
print("picoCTF{t3@mw0rk_", end='')
=======

print("m@k3s-----------", end='')
>>>>>>> feature/part-2
```

This is showing us what lines are conflicting between our two branches. The general format of merge conflicts look like this.

```txt
<<<<<<< (Current Branch)
Code from current branch goes here.
=======
Code from other branch goes here.
>>>>>>> (Incoming Branch)
```


In our *flag.py* (on main) we have `("picoCTF{t3@mw0rk_", end='')` and on feature/part-2 we have `print("m@k3s-----------", end='')`. Since we want both of these lines we can just delete the headers for this conflict which leaves us with this.

```py
print("Printing the flag...")
print("picoCTF{t3@mw0rk_", end='')
print("m@k3s-----------", end='')
```
From here we need to commit our code to assert that we have fixed the conflict. To do this we can run these commands.

```bash
$ git add flag.py
$ git commit -m "Merging Main and feature/part-2"
```

The first command tells git to track the changes we made this *flag.txt*. The second command creates a new commit with a message. After running we get confirmation that our branches have been merged!

```bash
[main e7b1952] Merging main and feature/part-2
```

From here we can do the same process for feature/part-3. It should also give you a merge conflict. After solving we will have code that looks like this.

```py
print("Printing the flag...")
print("picoCTF{t3@mw0rk_", end='')
print("m@k3s-----------", end='')
print("-------------}")
```

Then we can just run the code and our output should be the flag!

`picoCTF{t3@mw0rk_m@k3s-------------------------}`