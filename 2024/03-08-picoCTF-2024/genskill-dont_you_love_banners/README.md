# Commitment Issues

### General Skills - 300 points

>**Description:** Can you abuse the banner? <br>
> The server has been leaking some crucial information on `<domain1 <port-1>`. Use the leaked information to get to the server. <br>
> To connect to the running application use `nc <domain> <port-2>`. From the above information abuse the machine and find the flag in the /root directory.
>
>**Hint 1:** Do you know about symlinks? <br>
>**Hint 2:** Maybe some small password cracking or guessing.<br>

To begin this challenge you start an instance which gives you a domains and two ports. According to the description one port is leaking some information so intuitively we want to see what this is. We can run `nc <domain> <port-1>` to see whats being leaked.Netcat or nc is a versatile networking utility used for reading from and writing to network connections, port scanning, transferring files, and debugging network protocols.

```bash
$ nc <domain> <port-1>
SSH-2.0-OpenSSH_7.6p1 My_Passw@rd_@1234
```

This tells us that the domain is likely being run on an SSH server (specifically version 2.0) with OpenSSH version 7.6p1. This isn't too useful yet but we also get some sort of password. For now we can keep this in mind and checkout the other port by running the command given in the description

```text
$ nc <domain> <port-2>
*************************************
**************WELCOME****************
*************************************

what is the password? 
```

At this point we are prompted to enter a password by remote server we are likely SSHing into. We can use the password that is being leaked here.

```text
$ My_Passw@rd_@1234
What is the top cyber security conference in the world?
```

Now we get another prompt that is what is the top security conference in the world. Because I had to manually figure this one out here are 5 possible answers: Black Hat USA, BSides, RSA Conference, DEF CON, and ShmooCon. After you get it we are prompted with another question.

```text
$ <your answer goes here>
the first hacker ever was known for phreaking(making free phone calls), who was it?
```

This questions just a quick google search away. After you solve this question you are given access the server via SSH. We can list directories at this point and see what we're working with.

```
/home/player/
├── banner
└── text
```

There are two files in our current directory. A banner and text. This is what we get when we `cat` bot files.

```text
$ cat banner
*************************************
**************WELCOME****************
*************************************

$ cat text
keep digging
```

Insanely useful information... Anyways if we refer back to the description we know there is some information in /root.

Here is the directory structure to root (I really just want to make more trees)

```text
./
├── home/
│   └── player/
│       ├── banner
│       └── text
├── root/
│   ├── flag.txt
│   └── script.py
└── A bunch of random folders/
```

Once in the root directory we see there are two files: *flag.txt* and *script.py*. Obviously just run `$ cat flag.txt` and bam you got the flag, but no instead you get a permission denied error. Instead we can run `cat script.py`. This gives us the contents, its over 30 lines so you can read it [here](script.py).

After a few seconds of looking at this script you realize it it what is called when we netcat onto this port. It has the answers to all the questions we answered at the start. More importantly there is one specific line we want to attach on this server that is `with open("/home/player/banner", "r") as f:`

This line is what displays the banner when we first log into the server. This is where the first hint comes in. We want to create a symlink with some existing file and set that symlink as our home/player/banner file.

First, what is a [symlink](https://en.wikipedia.org/wiki/Symbolic_link) aka Symbolic Link. A symlink is a file whose purpose is to point to a file or directory (called the "target") by specifying a path thereto. Essentially if some sort of data exists in a file we can create another file that points to this data. This is sort of how file shortcuts work. When you run the shortcut it's running the file it's pointing to. Same goes for deleting as when you delete the shortcut it doesn't delete the program as it was calling.

Now that we know what symlinks are and the general idea behind them we can think about how to apply them in this problem. Right now we have a *flag.txt* we cannot view and a *banner* file that we view on entry of the SSH. So intuitively the best approach would be to just link *banner* to *flag.txt* so we will do just that.

Lets go back into the `/home/player` directory. To create a symlink from one file to another the general structure is `ln -s <target_path> <link_path>`. `ln` means link, `-s` is a flag that makes the link symbolic, then `<target_path>` is the absolute or relative path to the file you want to link, and finally `<link_path>` is the file you want to hold the link (think shortcut). Okay no we can create our symlink between *flag.txt* and *banner*.

```bash
$ rm banner # banner cannot exist when we make the  symlink
$ ln -s /root/flag.txt banner
```

Now we have linked banner to the flag. We can assert this by running `cat banner`. You should get a permission denied error if done correctly. Now we just exit the shell and netcat back into it and the original banner should be the flag.

```bash
$ nc <domain> <port-2>
picoCTF{b4nn3r------------------------------}

what is the password? 
```

<!-- Why are you reading this? -->