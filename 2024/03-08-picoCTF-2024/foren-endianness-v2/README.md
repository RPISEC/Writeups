# endianness-v2

## Foren, 300 points

> Here's a file that was recovered from a 32-bits system that organized the bytes a weird way. We're not even sure what type of file it is.
>
> Download it [here](https://artifacts.picoctf.net/c_titan/37/challengefile) and see what you can get out of it
>
> No hints

We're given a challenge file, and told that it was recovered from a 32-bit
system with strange byte organization. Based on the name of the file, our first
guess for the byte organization is that it will be big-endian.

The first thing I do is run `file` on `challengefile`, but it can't determine
the file type. The next thing I do is inspect the bits to see if I can find any magic bytes. The first 32 bits of the file are `E0FFD8FF`. Searching for these bytes on a [list of file signatures](https://en.wikipedia.org/wiki/List_of_file_signatures) didn't return anything either, so its time to start modifying the bits.

Since we know that the file is 32-bit, and is probably reverse-endian, we reverse the first 4 bytes that we extracted: `FFD8FFE0`. Cross referencing the list of file signatures gets us a match with jpg files! So, we need to reverse each four byte segment of the file.

Here's a python script to do that:

```python
with open('challengefile', 'rb') as read_file, open('outputfile', 'wb') # Read from challengefile, write to output file
    data = read_file.read()
    # Make an array with 4 bytes of data per entry from data
    array = [data[i:i+4] for i in range(0, len(data), 4)]
    # Reverse each entry in the array
    array = [entry[::-1] for entry in array]
    # Write the reversed array to outputfile
    for entry in array:
        write_file.write(entry)
```

Running this gives us an image file with the flag!

`picoCTF{cert!f1Ed_iNd!4n_s0rrY_3nDian_f72c4bf7}`
