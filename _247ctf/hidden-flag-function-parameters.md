---
title: "247CTF - Confused Environment Read"
date: 2021-02-28
categories: [247ctf, ctf]
image: /images/247ctf/logo_0.png
tags: [247ctf, assembly, ctf, tutorial, walkthrough, debug, reverse engineering, exploiting, pwn, binary exploitation, hidden flag function parameters, buffer overflow]
description: 247CTF Hidden Flag Function Parameters (PWN) challenge explained in detail. We will see how to solve the challenge and understand the underlying concepts.
hasComments: true
---

![247ctf0](/images/247ctf/pwnable/hidden_flag_function_parameters/description.png)

This binary exploitation challenge is, by the time I'm writing this tutorial, rated as *EASY* with a difficulty score of 2.25 out of 5.0. The description states the following:

> Can you control this applications flow to gain access to the hidden flag function with the correct parameters?

There is a binary to download and exploit. Upon downloading it, I used [file](https://en.wikipedia.org/wiki/File_(command)) command to identify, at least based on its header bytes, what kind of binary it is. You could, of course, use any other tool you find appropriate. 

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/file_command_and_first_execution.png">
</p>

As you can see in the image above, the binary is a <red>32-bit</red> [ELF](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format) executable and it's not stripped. That's nice since debugging and reversing it will be easier. Additionally, I executed the binary and checked whether the binary is vulnerable to buffer overflows. And <yellow>it is</yellow>. Notice how there is a **segmentation fault** when the input is long enough. That is, with the adequate input we can overwrite the **<gold>EIP</gold>** register thus hijacking the binary's execution flow. *(We will later see what the input is)*

The next step is to find out what protections has been the binary compiled with. In the following image I'm using [Cutter](https://cutter.re/).

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/protections.png">
</p>

The binary has no [stack canaries](https://en.wikipedia.org/wiki/Stack_buffer_overflow#Stack_canaries) and it's not [PIC](https://en.wikipedia.org/wiki/Position-independent_code). That is, we can overwrite the stack without worrying about canaries and the addresses of [.text](https://en.wikipedia.org/wiki/Code_segment) section (and other sections as well) will not change between executions. However, the binary was compiled with [NX](https://en.wikipedia.org/wiki/NX_bit) bit, i.e. we cannot execute code from the stack (like inputting a shellcode and jumping to it).

Let us reverse the binary and discover its inner workings :). This time I'll be using [IDA](https://www.hex-rays.com/products/ida/support/download_freeware/).

Inspecting the declared functions, there are two of them that quickly stand out. These two functions are `flag` and `chall`.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/functions.png">
</p>

Before inspecting them, let us take a look at `main`. It prints the strings and then calls `chall`. Pretty simple, nothing relevant here.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/main.png">
</p>


<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/chall_function.png">
</p>

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/flag_function.png">
</p>


I hope you enjoyed my write-up. I'd be delighted to know whether it helped you progress and learn new things. Do not hesitate to reach me out via [Twitter](https://twitter.com/Razvieu). I'm always eager to learn new things and help others out :)

## More challenges
* Click [here](/247ctf) to see 247CTF index.