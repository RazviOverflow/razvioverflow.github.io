---
title: "247CTF - Hidden Flag Function Parameters"
date: 2021-03-04
categories: [247ctf, ctf]
image: /images/247ctf/pwnable/hidden_flag_function_parameters/stack_behavior_while_hijacking_exploiting.png
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

As you can see in the image above, the binary is a <red>32-bit</red> [ELF](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format) executable and it's not stripped. That's nice since debugging and reversing it will be easier. Automatically we must set our minds to think in 32-bit architecture. Additionally, I executed the binary and checked whether the binary is vulnerable to buffer overflows. And <yellow>it is</yellow>. Notice how there is a **segmentation fault** when the input is long enough. That is, with the adequate input we can overwrite the **<gold>EIP</gold>** register thus hijacking the binary's execution flow. *(We will later see what the input is)*

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

In other words, from `flag`'s point of view, it expects the stack to be aligned like the following image where:
- 1st argument corresponds to 0x1337
- 2nd argument to 0x247
- 3rd argument to 0x12345678

Notice how the return address of the function is stored at ebp+0x4 and right above it, at ebp+0x8, lives the very first parameter.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/arguments_position.png">
</p>

So, the exploit consists in overwriting the return address of `chall` function with the address of `flag` and continue writing data in the stack in such a way that the parameters of `flag` are set according to the previous image. 

**<yellow>However</yellow>**, this one is a bit tricky and we must manually configure the stack. Bear in mind that in a <green>legit</green> execution, before *calling* a function, there is a `call` instruction. [CALL](https://stackoverflow.com/questions/7060970/substitutes-for-x86-assembly-call-instruction) instructions modifies the stack pointer (`ESP` register) given it pushes the address to return to. Since we're hacking our way to call `flag`, there will be no `call` instruction. Additionally, functions are preceded by the [prologue](https://stackoverflow.com/a/14765429) and succeeded by the [epilogue](https://stackoverflow.com/a/14765429). The prologues and epilogues will still happen, but the absence of `call` slightly modifies the stack template/setting we must achieve. 

Before reasoning about the exploit and the payload, **there is one more thing to note**. The register `ebx` is crucial. It is used throughout the whole program to reference parameters that are constant (hardcoded) and passed to other functions like `fopen`. 

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/use_of_ebx.png">
</p>

Notice how, in the image above, `ebp` is assigned from the stack right before `chall` function finises (instruction at address `084862D`). Since `chall` is the function whose stack frame we will overflow, it is important to keep the correct value at `ebp-0x04` because it is later used in `flag` (right column of the image below) to reference all the parameters needed to open <red>flag.txt</red> (amongst many others).

Now, what is that value? It is fairly simple to find it out with IDA by simply resolving the offsets used in `lea` instructions (e.g., address `080485A9`). However, you can also debug it using your debugger of preference. You can do so by debugging a legit execution. Place a breakpoint when calling `chall`  and take a look at the contents of the stack. Right below `ebp` you will see the expected value of `ebx`. The value in question is `08048708`, which corresponds to the beginning of the [.rodata](https://en.wikipedia.org/wiki/Data_segment) (read-only data) section.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/rodata_section.png">
</p>

Now, with this in mind we know so far that our exploit should meet, at least, the following requirements:
1. Writing of bytes starts at `ebp-0x88` 
2. At `ebp-0x4` we must preserve the expected `ebx` value: `0x08048708`
3. The return address of `chall` must be overwritten with the return address of `flag`: `0x08048576`
4. When executing `flag`, the following must be true: `ebp+0x08 = 0x1337`, `ebp+0xc = 0x247` and `ebp+0x10 = 0x12345678`.

With all this information in mind, the scheme of our exploit is the one I drew in the next image.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/stack_behavior_while_hijacking_exploiting.png">
</p>

Notice I depicted the state of the stack and the registers when `chall` is about to finish (execute `ret`) and right after `flag` epilogue. If there is something you don't understand (like how the registers work or why do they move) do not hesitate to reach me out!

The logic behind the previous scheme is: in the left side of the image you can see the stack's composition when `chall` is about to finish (calling `ret`). In order to reach `flag` we must overwrite `chall`'s return address. We must write 0x84 padding bytes to reach `ebp-0x4`, write `ebx`'s expected value (remember we are working with 32-bit little endian), another 0x4 bytes of padding to reach the return address and, finally, the address of `flag`. We must continue writing data into memory so we accordingly set the parameters of `flag`. And here is where is most useful the drawing of the stack from `flag`'s perspective (right side of the image).

Please be aware of the cell separation that exists between `ebp` and `flag`'s first argument (even though this memory cell corresponds to what would have been `flag`'s return address, we couldn't care less about it at this point). This is how `flag` expects the stack to be set-up and we must respect it. This cell separation must be considered when overflowing `chall`'s buffer.

After all this reasoning, the script that I used and successfully exploits the binary is the following one. __BEAR IN MIND__ you can test your exploit locally by creating a spurious _flag.txt_.

```python
# RazviOverflow
# Python3

from pwn import *

flag_address = 0x08048576
ebx_original_value = 0x0804a000
arg1 = 0x1337
arg2 = 0x247
arg3 = 0x12345678
payload = b"A"*0x84 + p32(ebx_original_value) + b"B"*0x4 + p32(flag_address) + b"C"*0x4 + p32(arg1) + p32(arg2) + p32(arg3)

binary = process("./hidden_flag_function_with_args")
#binary = remote("XXX", 00000)
print(binary.recv())
binary.sendline(payload)
binary.interactive()
```

Executing the exploit successfully leaks the flag. _The execution ends with errors, but we do not care about a clean execution. We have the flag :)_

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/exploited_locally.png">
</p>

Now, executing it remotely should leak the actual flag to validate the challenge.

<p align="center">
	<img src="/images/247ctf/pwnable/hidden_flag_function_parameters/exploited_remotely.png">
</p>

I hope you enjoyed my write-up. I'd be delighted to know whether it helped you progress and learn new things. Do not hesitate to reach me out via [Twitter](https://twitter.com/Razvieu). I'm always eager to learn new things and help others out :)

## More challenges
* Click [here](/247ctf) to see 247CTF index.