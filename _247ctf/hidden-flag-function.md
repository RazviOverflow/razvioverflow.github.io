---
title: "247CTF - Hidden Flag Function"
date: 2021-02-11
cateies: [247ctf, ctf]
image: /images/247ctf/logo_0.png
tags: [247ctf, assembly, ctf, tutorial, walkthrough, debug, reverse engineering, exploiting, pwn, binary exploitation, hidden flag function, buffer overflow]
description: 247CTF Hidden Flag Function (PWN) challenge explained in detail. We will see how to solve the challenge and understand the underlying concepts.
hasComments: true
---

![247ctf1](/images/247ctf/pwnable/hidden_flag_function/description.png)

This binary exploitation challenge is, at the moment of writing this write-up, rated as *EASY* with a difficulty score of 2.16 out of 5.0. Its description states the following:

> Can you control this applications flow to gain access to the hidden flag function?

As per usual with PWN challenges, we are given a binary to reverse and analyze. You can use whatever reversing tool or framework better suits your needs. There are fantastic tools like [Radare2](https://rada.re/n/), [Cutter](https://cutter.re/), [Ghidra](https://ghidra-sre.org/), [Rizin](https://rizin.re/), [GDB](https://www.gnu.org/software/gdb/) (with its many flavors like gdp-peda or pwngdb) or the all-mighty [IDA](https://www.hex-rays.com/products/ida/), each and every one with their own advantages and drawbacks. 

Upon downloading the binary, it's time to analyze it and find out what it really is. Using the `file` command, we find out it's a <yellow>32-bit</yellow> binary and it is <yellow>not stripped</yellow>. 

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/file_command.png">
</p>

That's cool! Being a not stripped binary actually makes our lives as reverse engineers easier since the binary will have some debug information. If you wonder what a stripped or not stripped binary is you can find more information [here](https://stackoverflow.com/questions/22682151/difference-between-a-stripped-binary-and-a-non-stripped-binary-in-linux#:~:text=1%20Answer&text=Although%20you%20have%20found%20your,debugging%20information%20built%20into%20it.&text=Whereas%20Strip%20binaries%20generally%20remove,the%20size%20of%20the%20exe.) (Google it, there are plenty of results). Now that we know what architecture we're dealing with (32-bit) we can start thinking about our exploit and its main [differences](https://security.stackexchange.com/questions/169291/x32-vs-x64-reverse-engineering-and-exploit-development) with 64-bit (4-bytes addresses, arguments are passed via stack, etc).

After executing `strings` and `rabin2 -zzzq` commands, we can clearly see there are references to flag. As we will later find out, there is a function called `flag`, a flag message and a flag.txt file that somebody will try to open. It is always recommended to use these commands to get a first impressions of what the binary's behavior will be.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/strings_rabin2_command.png">
</p>

Before starting the actual reverse engineering process, it's always recommended to execute the binary.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/1st_execution.png">
</p>

It requests for input and if it's long enough we can actually break the program. It means we can actually overwrite some stack addresses. Let's find out!

The next step was finding out what protection was the binary compiled with. In order to do so, you can use what tool you find most convenient. One widespread tool for such purpose is [checksec](https://github.com/slimm609/checksec.sh).

I will be using Cutter to reverse engineer the binary. Using Cutter we can inspect its protections:

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/protections.png">
</p>

We find out it's indeed a 32 bit [ELF](https://es.wikipedia.org/wiki/Executable_and_Linkable_Format) binary and it has no canaries, it's not a PIC/PIE binary but NX bit is enabled. [NX](https://en.wikipedia.org/wiki/NX_bit) bit (from **n**o-e**x**ecute bit) basically doesn't allow the execution of code on certain regions of memory like the stack. That is, we cannot execute our shellcode if there is a buffer overflow. In case someone is wondering about ASLR: when dealing with PWN challenged you must **ALWAYS** assume ASLR is enabled on the remote side. 

Continuing with the binary, it's time to explore its declared functions:

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/functions.png">
</p>

There are two functions that easily draw the attention: `chall` and `flag`. Now let's start from the beginning: exploring the `main` function.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/main.png">
</p>

There is nothing special about it, just a message being printed with `puts` and a call to `chall`. *Notice how `flag` function isn't called.* 

Inspecting `chall` function:

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/chall_function.png">
</p>

The input is read with `scanf`. In this context, it is mandatory for us to know that scanf is a [vulnerable](https://stackoverflow.com/questions/1621394/how-to-prevent-scanf-causing-a-buffer-overflow-in-c) function. Another scanf [vulnerability](https://dhavalkapil.com/blogs/Buffer-Overflow-Exploit/) example.

In case you are not familiar with scanf, I recommend you to read its [man page](https://man7.org/linux/man-pages/man3/scanf.3.html). It basically reads input, tries to parse it according to a given format specified and stores the result in the specified address. In fact, these are the two arguments the function takes. *Remember that we are working with a 32-bit architectures. Arguments are passed vya the stack and they are pushed in reverse order. That is, **last argument is pushed first.***

In the images below you can see the instructions within the <blue>teal</blue> lines correspond to the buffer and those within <red>red</red> lines correspond to the format specifier. 

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/variables_0.png">
</p>

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/variables_1.png">
</p>

Since `scanf` is vulnerable to buffer overflow, we must take note where does the function store the data (or the user input). In other words, where in memory (what address) does the function start writing. It starts at `ebp-0x48`. We don't need to know what specific address that is, it is enough for us to know it's 0x48 bytes below `ebp` because we also know that right above `ebp` (that is `ebp+x04` <yellow>in 32-bit</yellow>) is stored the return address of the function. Overflowing the buffer and overwriting `ebp+0x48`  we can **<gold>hijack</gold>** the program's execution flow and control where `chall` returns. 

Let's inspect `flag` function before assuming it's the right place to jump to.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/flag_function.png">
</p>

It definitely is. It opens a file (we can assume it's named flag.txt at this point, but the correct move would be to actually check it), gets its contents and prints them.

Our objective is to make it return to `flag` (hijacked flow) instead of `main` (legitimate execution). Now, how do we do that? **REMEMBER** that <yellow>writing</yellow> in memory happens from <red>lower addresses towards higher ones</red>. That is, our vulnerable `scanf` function will start writing at address `ebp-0x48` and we will have to input <orange>0x48</orange> (72 in decimal) bytes to reach `ebp`, <orange>4 more</orange> to overwrite it and reach the return address and, finally, the address (4 bytes) to hijack the execution flow and thus jumping wherever we want. In case you are not familiar with how stack behaves, I recommend you reading some beginner 32-bit exploiting tutorials like the legendary Aleph One's *[Smashing The Stack For Fun and Profit](http://phrack.org/issues/49/14.html)* published in Phrack, and many others like [1](https://www.exploit-db.com/docs/english/28475-linux-stack-based-buffer-overflows.pdf), [2](https://www.corelan.be/index.php/2009/07/19/exploit-writing-tutorial-part-1-stack-based-overflows/), [3](https://dhavalkapil.com/blogs/Buffer-Overflow-Exploit/). I also recommend [LiveOverflow](https://www.youtube.com/watch?v=iyAyN3GFM7A&list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN&ab_channel=LiveOverflow)'s exploiting videos. 

To sum it up, this is the scenario we're dealing with:

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/stack_behavior.png">
</p>

One important thing is getting the address of `flag` function. Since the binary is not PIC/PIE (position independent), the .text section addresses won't change between executions. That is, we can hardcode the address `0x08048576`. 

In order to exploit the binary I will be using [pwntools](https://github.com/Gallopsled/pwntools). **<red>PLEASE BEAR IN MIND</red>** that the data you want to overwrite and place on the stack must be [LITTLE ENDIAN](https://stackoverflow.com/questions/25938669/is-little-endian-a-byte-or-bit-order-in-x86-architecture#:~:text=IA%2D32%20processors%20are%20%E2%80%9Clittle,from%20the%20least%20significant%20byte.&text=In%20computing%2C%20memory%20commonly%20stores,8%2Dbit%20units%20called%20bytes.). Pwntools' [packing](https://docs.pwntools.com/en/stable/util/packing.html) (p32() or p64()) functions already convert the numbers for us.

```python
# RazviOverflow
# Python3

from pwn import *

# Getting flag address
static = ELF("./hidden_flag_function")
flag_address = p32(static.symbols['flag'])
payload = b"A" * 0x48 + b"B" * 4 + flag_address

# Exploiting the binary
binary = process("./hidden_flag_function")
#binary = remote("xxx", 0000)
print(binary.recv())
binary.sendline(payload)
print(binary.recvall())
```
When you try to execute the exploit for the first time you may find it appear not to be working:
<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/execution_0.png">
</p>

That's because you may find yourself (as I was) executing the exploit locally and you don't have a file called `flag.txt`. Remember that's what the function `flag` was looking for. Create the file using a fake flag and you'll see the exploit actually works :)

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/execution_1.png">
</p>

Now it's just a matter of executing it remotely, replacing `process` with `remote(address, port)` in the python exploit.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function/exploited.png">
</p>

I hope you enjoyed my write-up. I'd be delighted to know whether it helped you progress and learn new things. Do not hesitate to reach me out via [Twitter](https://twitter.com/Razvieu). I'm always eager to learn new things and help others out :)

## More challenges
* Click [here](/247ctf) to see 247CTF index.