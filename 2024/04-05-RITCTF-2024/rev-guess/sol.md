# Guess
REV - 100 points

We're given an APK. During the competition I spent the time to emulate and run the program with android studio, but it didn't turn out to be too useful:

![image](https://github.com/RPISEC/Writeups/assets/29514104/74fc471d-887b-479b-bec7-59e559c476ff)

So, I opened the apk in `jadx-gui` instead.

![image](https://github.com/RPISEC/Writeups/assets/29514104/3390203d-c678-42ad-b4c1-9e3250016e9e)

There was the `flag` class in the MainActivity. This class looked like it was decrypting the flag in some way. 

So, I converted the Java code to Python by asking ChatGPT 3.5:
```python
import base64

class Flag:
    @staticmethod
    def end():
        return Flag.what_the_function("cmpkdjNjYzE6MzUuU1R8aHY0dHR6YGd2b2R1MnBvfi46MTI0M3M6amcz")

    @staticmethod
    def what_the_function(evil_string):
        forname_n = None
        try:
            forname_n = base64.b64decode(evil_string).decode('utf-8')
        except:
            pass

        recursive_char_array = []
        undecrypted_encrypted_string = "SGF2ZSB5b3UgZXZlciB1c2VkIEZyaWRhPw=="
        final_array = list(reversed(undecrypted_encrypted_string))
        kentucky = 0
        xortrad = len(final_array) - 1
        while kentucky < xortrad:
            glaf = final_array[kentucky]
            final_array[kentucky] = final_array[xortrad]
            final_array[xortrad] = glaf
            kentucky += 1
            xortrad -= 1

        for char in forname_n:
            decrypted_char = chr(ord(char) - 1)
            recursive_char_array.append(decrypted_char)

        encrypted_string = ""
        for c in final_array:
            encrypted_string += base64.b64encode("SGF2ZSB5b3UgZXZlciB1c2VkIEZyaWRhPw==".encode()).decode() + c

        return "SGF2ZSB5b3UgZXZlciB1c2VkIEZyaWRhPw==" + ''.join(recursive_char_array) + encrypted_string

# Example usage:
print(Flag.end())
```

Then, I simply ran the python code, and the flag was part of the output.
