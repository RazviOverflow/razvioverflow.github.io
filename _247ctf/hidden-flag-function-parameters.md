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

Now, when taking a look at `chall` we can easily spot the vulnerability. The function performs a `scanf` read at address <yellow>ebp-0x88</yellow>. Scanf is a well-known [vulnerable](https://www.google.com/search?q=scanf+vulnerability&oq=scanf+vulnerability&aqs=chrome..69i57.2484j0j1&sourceid=chrome&ie=UTF-8) function since it performs no bounds checking. That is, we can input vast amounts of bytes.

The attack is now clear, we can overwrite `chall`'s thus **<red>hijacking the execution flow</red>**.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/chall_function.png">
</p>

Now the question is: where do we want to redirect the execution flow? The answer is: to `flag` function. Inspecting `flag` one can see there are several consecutive conditional jumps. If the correct conditions are met, there is a final block that actually opens a file called *<red>flag.txt</red>* and prints its content. If successfully exploited on the remote server, that would print the flag.

In order to reach (execute) the code block that prints the flag, we must meet the following requirements from `flag`'s perspective:
```
ebp + 0x8 = 0x1337
ebp + 0xc = 0x247
ebp + 0x10 = 0x12345678
```

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/flag_function.png">
</p>

In other words, when we manage to hijack the execution flow and reach `flag` function, its parameters/arguments must be the aforementioned ones. Please bear in mind we are exploiting a binary compiled for a <yellow>32-bit architecture</yellow>, hence the use of the stack to pass parameters to functions. Remember the [calling convention](https://en.wikipedia.org/wiki/X86_calling_conventions#List_of_x86_calling_conventions) is different for 32-bit and 64-bit. In 32-bit, arguments are always referenced as relative addresses to `ebp` register, since `ebp` is the [base pointer](https://stackoverflow.com/questions/21718397/what-are-the-esp-and-the-ebp-registers) (also known as frame pointer) of that particular stack frame. 

In other words, from `flag`'s point of view, it expects the stack to be aligned like the following image where 1st argument corresponds to 0x1337, 2nd argument to 0x247 and 3rd argument to 0x12345678. Notice how the return address of the function is stored at ebp+0x4 and right above it, at ebp+0x8, lives the very first parameter.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/arguments_position.png">
</p>



I hope you enjoyed my write-up. I'd be delighted to know whether it helped you progress and learn new things. Do not hesitate to reach me out via [Twitter](https://twitter.com/Razvieu). I'm always eager to learn new things and help others out :)

## More challenges
* Click [here](/247ctf) to see 247CTF index.