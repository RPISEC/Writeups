# WinAntiDbg0x300
PicoCTF 2024 -- 400 points

## Writeup
We're provided a windows executable. You must have administrative privileges to interact with the program.

![image](https://github.com/RPISEC/Writeups/assets/29514104/1f8f181b-9964-4710-96e6-7c4239e6b8dd)

Similar to WinantiDbg0x100 and 0x200, you must keep the program running while attaching a debugger.

Upon opening the executable with IDA Free, I notice a lone UPX segment.

![image](https://github.com/RPISEC/Writeups/assets/29514104/1876c6dc-f01b-4f13-9cd6-c37a6ce1dd41)

Unpacking the executable will be extremely helpful for further reversing. Download UPX: upx.github.io

Unpack the executable: `$ upx -d WinAntiDbg0x300.exe`

![image](https://github.com/RPISEC/Writeups/assets/29514104/65af96a1-4054-44ad-89ce-752fc7f64afc)

Now, opening the executable in IDA Free will give comprehendable results.

First, analyze the main function: _WinMain@16_0. Looking through the assembly, I notice a branch between a "Debugger detected" message and continued execution.

![image](https://github.com/RPISEC/Writeups/assets/29514104/d1f952a0-cecc-41d2-bb3c-f98018500e3a)

Set a breakpoint at `jz short loc_92802`. Edit the breakpoint and set the condition to `ZF=1`. This will guarantee we continue execution instead of detecting the debugger.

![image](https://github.com/RPISEC/Writeups/assets/29514104/8371f6f1-2f09-4e9f-b789-094c4ae8f067)

The program will crash if you continue past the breakpoint. At this point, I decide to figure out where our final destination is.

The previous challenges (0x100 and 0x200) both had the string "flag" within them. So I tried my luck with searching for the text "flag".

![image](https://github.com/RPISEC/Writeups/assets/29514104/2aa9d216-44fb-4e46-b93d-1269606c2b65)

Sure enough, we found a function that looks like it prints the flag. This is where we want to get.

![image](https://github.com/RPISEC/Writeups/assets/29514104/ed9c2ab6-1c7c-48d3-9593-2e0f2c6b8608)

![image](https://github.com/RPISEC/Writeups/assets/29514104/5d613ceb-a6a7-4e3d-b442-e51dc16b7c10)

This function has lot of branches and loops that prevent us from getting to the flag. We must evade them.

At this point, simply set a breakpoint at every important branch in the function.

That is, set breakpoints so that you are getting closer to the desired label. Essentially, follow the green lines.

![image](https://github.com/RPISEC/Writeups/assets/29514104/c02e80df-ebdd-45cf-9924-be9d90d06cf5)

Edit the first breakpoint. Set the condition to `ZF=1`.

Edit the second breakpoint. Set the condition to `ZF=0`.

Now, you should be able to run the program in IDA and continue through the breakpoints. The flag will pop up on screen and in the IDA console after you close the executable.

![image](https://github.com/RPISEC/Writeups/assets/29514104/20f3cd11-e872-485f-80ee-565b4b75c3fa)

![image](https://github.com/RPISEC/Writeups/assets/29514104/fc494397-6c2a-4f9c-8d2f-3e875e69fc4c)



