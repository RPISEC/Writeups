# Verify
### Foren, 50 points

> People keep trying to trick my players with imitation flags. I want to make sure they get the real thing! I'm going to provide the SHA-256 hash and a decrypt script to help you know that my flags are legitimate.<br>
> 
> **Hint 1:** Checksums let you tell if a file is complete and from the original distributor. If the hash doesn't match, it's a different file. <br>
> **Hint 2:** You can create a SHA checksum of a file with `sha256sum <file>` or all files in a directory with `sha256sum <directory>/*`. <br>
> **Hint 3:** Remember you can pipe the output of one command to another with |. Try practicing with the 'First Grep' challenge if you're stuck!

Once connected to the challenge instance, we're placed in a directory with a file `checksum.txt`, the legitimate SHA-256 hash of the flag, the decrypt script `decrypt.sh`, and a directory `files/`, with the imitation flags as specified by the challenge description.

The `checksum` file only has the string: `b09c99c555e2b39a7e97849181e8996bc6a62501f0149c32447d8e65e205d6d2`.

We're tasked to find the real flag, hidden among the files in `files`, identified by having same hash as in `checksum.txt`. Then, running `./decrypt.sh <file>` will decrypt the flag.

To find the flag, we can compare the `sha256sum` of each file in `files` as the hint tells us. Rather than spending time running the command on each file or pruning through the output of `sha256sum files/*`, we can use `grep` and `cat` to help us:

```
sha256sum files/* | grep "$(cat checksum.txt)"
```
(or in English, retrieve the `sha256sum` of every file (`*`) in `files/`, and find (`grep`) the output which matches the contents (`cat`) of `checksum.txt`)

Output:
```
b09c99c555e2b39a7e97849181e8996bc6a62501f0149c32447d8e65e205d6d2  files/451fd69b
```
As we can verify, this is the same sum as in `checksum`, so the real flag must be `files/451fd69b`!

Finally, running `./decrypt.sh files/451fd69b` successfully gives us our flag.

`picoCTF{trust_but_verify_451fd69b}`
