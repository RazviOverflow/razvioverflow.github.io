---
title: "AUCTF 2020"
categories: [ctf]
tags: [ctf, writeup, auctf]
hasComments: true
date: 2020-04-07
image: /images/CTF/AUCTF2020/logo.png
description: AUCTF 2020 (Auburn CTF) challenge writeups.
---

<p align="center">
  <img src="/images/CTF/AUCTF2020/logo.png" width="300"/>
</p>
  
Main CTF page: [https://ctf.auburn.edu/team](https://ctf.auburn.edu/team)  
CTFTime even page: [https://ctftime.org/event/1020](https://ctftime.org/event/1020)  
Auburn University Ethical Hacking Club's Site: [https://ehc.auburn.edu/](https://ehc.auburn.edu/)  

AUCTF 2020 was, in my opinion, one of the best online CTFs so far in 2020. Administrator were very active on their discord server and always answering our questions. There were some technical problems with the infrastructure but they took care of it immediately. So huge props to them :) AUCTF is organized by the [AU Ethical Hacking Club](https://twitter.com/AU_EHC).

The challenged were pretty nice and carefully crafted, we really enjoyed them. As always, learning by doing is the main objective and it was totally achieved with AUCTF since we learned quite a few things. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/scoreboard.png" width="500"/>
</p>

This time I participated along with [Kashmir54](https://twitter.com/ManuSanchez54) and [urzu](@daniel_uroz) and we ended up in 160th position. I'd like to thank both of them :)

The CTF had several categories. In this page you will find the following writeups:
  - Pwn / Binary Exploitation:
    - Easy as Pie! and Thanksgiving Dinner!
  - Reverse Engineering:
    - Cracker Barrel, Mr. Game and Watch, Sora, Plain Jane and Don't Break Me!
  - Trivia:
    - The answer to all questions. 


# PWN
## Easy as Pie!

<p align="center">
  <img src="/images/CTF/AUCTF2020/pwn00.png"/>
</p>

In this challenge the user connected to a bash emulator that had several commands like cat, write, etc... In order to inspect sensitive files like flag.txt or .acl.txt, there were other access control files. Turns out the user had write permission over them. So it was just a matter of adding the read permission to the access control files. The flag was in the .acl.txt file and `write .acl.txt:user:600 acl.txt` gave the read permission. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/pwn01.png" />
</p>

The flag is: auctf{h4_y0u_g0t_tr0ll3d_welC0m#_t0_pWN_l@nd}

# Thanksgiving Dinner!

<p align="center">
  <img src="/images/CTF/AUCTF2020/pwn10.png" />
</p>

This time we're given a binary. I used [Cutter](https://cutter.re/) to reverse and debug it. Looking at the protections of the binary we can see it has NX bit (no shellcode in the stack) and PIE/PIC. Since server has ASLR disabled, we don't have to worry about ASLR. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/pwn15.png" />
</p>

Inspecting the main function, we can see there is a call to `vulnerable`. *(You can also notice the function in the functions tab)*

<p align="center">
  <img src="/images/CTF/AUCTF2020/pwn11.png" />
</p>

Inspecting the `vulnerable` functions we can see it performs a fgets on the buffer `s`, and it reads 0x24 (36) bytes. It then performs several checks over the contents of that same buffer. 

Please take into account that not all the checks are the same. Whenever a jump from the checks is taken, `print_flag` is skipped so we must not take the checks. That is (ordered by check order, not by position in the buffer): writing the value 0x1337, writing a value strictly lesser than 0xffffffec (it's the representation of the signed -20 value), writing a value different to 0x14, writing the value 0x667463 and writing the value 0x2a.

<p align="center">
  <img src="/images/CTF/AUCTF2020/pwn13.png" />
</p>

<p align="center">
  <img src="/images/CTF/AUCTF2020/pwn12.png" />
</p>

The buffer into the stuck must look like the image below in order to pass all the checks: *Please bear in mind how 0xffffffeb is the representation of -21, which is strictly lesser than  0xffffffec (-21)* 

<p align="center">
  <img src="/images/CTF/AUCTF2020/pwn14.png" />
</p>

Creating the script is fairly simple with [pwntools](https://github.com/Gallopsled/pwntools). 

```python
#RazviOverflow
from pwn import *

binary = remote("challenges.auctf.com", 30011)
#binary = process("./turkey")

padding = "A" * 16
firstcheck = p32(0x2a)
secondcheck = p32(0x15)
thirdcheck = p32(0x667463)
forthcheck = p32(0xffffffeb)
fifthcheck = p32(0x1337)


print binary.recvuntil("Sorry that's all I got!")
binary.sendline(padding+firstcheck+secondcheck+thirdcheck+forthcheck+fifthcheck)
print binary.recvall()

```

<p align="center">
  <img src="/images/CTF/AUCTF2020/pwn16.png" />
</p>

The flag is: The flag is: auctf{I_s@id_1_w@s_fu11!}

# Reversing

## Cracker Barrel

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing00.png" />
</p>

We're given a binary to reverse and see how to obtain the flag. I will go straight to the inner workings of the binary since checking protections is irrelevant here, but remember it is always a MUST.

Inspecting the `main` function we detect a call to `check` function. If check returns 0 the flag `print_flag` will be called. That's what we want :)

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing02.png" />
</p>

Here is the Ghidra-decompiled version:

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing03.png" />
</p>

Within `check` there are three nested if's statements that check the result of check_1, check_2 and check_3. We can see all calls are performed with the user's input as parameter and in order to get the flag every check must return whatever value rather than 0.

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing04.png" />
</p>

Taking a look into `check_1`, we can easily identify that *starwars* is the input that makes the function return != 0. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing05.png" />
</p>

Now, `check_2` is a bit tricky. Since the while loop is performed base upon the length of the user's input, what happens if that very same length is 0? Remember [strlen()](http://man7.org/linux/man-pages/man3/strlen.3.html) count up to, but excluding, the \0 null byte. If strlen returns 0, the while loop is irrelevant and the strcmp call will return 0 hence `check_2` will return **True**. In C all values except 0 are considered as True. (0 is False) And thats exactly what we want, a value != 0. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing06.png" />
</p>

For `check_3` we can apply the exact strategy since all the checks are as well performed based on the length of the user's input. Again, what happens if that length is 0?

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing07.png" />
</p>

You can see that the execution locally works with the input sequence `starwars(enter),(enter),(enter)`.

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing09.png" />
</p>

Now it's a matter of running it remotely. You can also try the expected input, or part of it, and it will work as well. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing01.png" />
</p>

The flag is: auctf{w3lc0m3_to_R3_1021}

## Mr. Game and Watch

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing10.png" />
</p>

This time we're provided with a java .class file. I used [JD-GUI](https://java-decompiler.github.io/) to decompile it. After decompiling it, understanding the binary's behavior is quite simple. There is a crackme() call and based on its return value (it must  be True) there is a call to print_flag().

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing11.png" />
</p>

As you can see, crackme() calls crack_1, crack_2 and crack_3 passing as parameter the user's input. All functions must return True so crackme() returns True as well. Additionally, the program has the following global variables:

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing111.png" />
</p>


Let's check out the crack_* functions. `crack_1` simply computes the MD5 of the user given input and compares it with secret_1. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing12.png" />
</p>

In order to pass the first check we must crack the secret_1 hash (we know it's MD5) and provide that as input. Before trying to bruteforce it, we can check whether it has been previously cracked. In order to do so, I'll be using [Crackstation](https://crackstation.net/).

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing13.png" />
</p>

Turns out it has indeed been cracked before. The first input must be `masterchief`.

`crack_2` performs the SHA1 of the input and compares it to the result of the decrypt() call. Let's find out what decrypt() actually does.

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing14.png" />
</p>

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing15.png" />
</p>

It doesn't seem to make any sense. It could be a decompilation error. I tried decompiling the file with [java decompilers](http://www.javadecompilers.com/).

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing112.png" />
</p>

That definitely looks better. We now know that decrpyt is xoring every entry of secret_2 with key_2. I made use of a simple python script to get the hash. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing113.png" />
</p>

We can, once again, use crackstation to see whether the hash has been already cracked. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing16.png" />
</p>

And yes, it has. The second input must be `princesspeach`. 

Last but not least, `crack_3`

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing17.png" />
</p>

We can see it computes the SHA-256 of the user provided input, encrypts it using encrypt() and then compares the whole array with `secret_3`.

Now, the encrypt function is the following one:

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing18.png" />
</p>

It xors every character of the first parameter with the second parameter and stores them in an array of ints. That is, it xors the SHA-256 of the given input with `key_3` and compares the result iwth `secret_3`. In other words, we know `secret_3` is the result we're looking for. So we can xor every number with `key_3` and see what is the resulting hash. That resulting hash is the SHA-256 we're looking for. 

We can do so with a simple python script. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing115.png" />
</p>

Notice how, even though we are xoring pure integers, I converted them to char in order to get the corresponding hash. Once again, we want to find out if the hash has been already cracked.

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing19.png" />
</p>

And yes, it has been cracked. The third input must be `solidsnake`

Now it's time to execute the binary (remotely) and see if the inputs are correct.

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing110.png" />
</p>

The flag is: auctf{If_u_h8_JAVA_and_@SM_try_c_sharp_2922}

## Sora

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing20.png" />
</p>

This time we're given an ELF64. When we disassemble it and take a look at the main function, we can see there is a call to `encrypt`. In order to print the flag we want `encrypt` to return 0.

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing22.png" />
</p>

Lets find out what is `encrypt`. *I'm showing the decompiled version for simplicity* It performs several operations with a string called \_secret. That \_secret variable/constant is now oh high interest to us. We can place a breakpoint there and debug the program. Cutter allows us to place a breakpoint in the decompiled version and it will be also placed in the corresponding disassembly code. When it reaches that breakpoint we can inspect the value of rdi *(remember x64 calling convention, first parameter goes into the rdi register (in Linux))*.

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing23.png" />
</p>

We inspect the contents of rdi register, i.e, we "debug register" `dr rdi` and "print string" `ps` at that specific address and we can see the string being passed as argument to strlen is `aQLpavpKQcCVpfcg`. Now it is just a matter of replicating the `encrypt` algorithm and see its output. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing24.png" />
</p>


Please notice there are many solutions to this challenge since the modulo operation is not completely reversible. That is, the %0x3d the binary performs could be the result of many possibilities. For example, 0 mod 61 = 61 mod 61 = 122 mod 61, etc... We don't really know what the original character was. That's why I used string.printable, to take into account every printable char. Notice, however, that at the first letter I found to be the result, I break the loop. It doesn't mean there isn't any other letter to also be the result. The script that I used is:
```python
#RazviOverflow
from pwn import *
import string

secret = "aQLpavpKQcCVpfcg"

secret_decrypted = list()

for letter in secret:
  for char in string.printable:
    if ((ord(char) * 8 + 0x13) % 0x3d + 0x41) is ord(letter):
      secret_decrypted.append(char)
      break


secret_decrypted ="".join(secret_decrypted)
  
#binary = process("./sora")
binary = remote("challenges.auctf.com", 30004)
print binary.recvuntil("!")
binary.sendline(secret_decrypted)
print binary.recvall()
```

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing21.png" />
</p>

The flag is: auctf{that_w@s_2_ezy_29302}

## Plain Jane 
<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing30.png" />
</p>

This time we're given a `.s` file. That is, an assembly file. [More info here](https://stackoverflow.com/questions/10285410/what-are-s-files)

In order to run it I used [Online GDB](https://www.onlinegdb.com/). We must place a breakpoint right before main function finishes and inspect what the value of `eax` is. Remember in 32 bit return value is stored, by default, in `eax`. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing31.png" />
</p>

The flag is: 0x6fcf

## Don't Break Me!

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing40.png" />
</p>

This time we're once again given an ELF binary. Inspecting its disassembled code we can easily identify a call to a function named `debugger_check`. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing45.png" />
</p>

This function checks whether the binary is being debugged. We must NOP it in order to be able to debug the binary but first we must check where is this function called. To do so, we must inspect its cross-references.

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing46.png" />
</p>

Now we can NOP all the calls made to `debugger_check`. NOPping a funcion with Cutter is fairly simple: right click on the instruction -> Edit -> NOP Instruction.

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing47.png" />
</p>

After NOPping all the calls, the cross-references window should look like this:

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing41.png" />
</p>

Now, looking at the main algorithm we can notice that `print_flag` is called based on the result of the strcmp call. The string compare function is comparing `s2` and `s1`. `s2` is the result of calling `encrypt` over `s` (the user input) and `s1` is the result of calling `get_string`, i.e, `s1` is the expected result. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing48.png" />
</p>

So the approach we can follow here is placing a breakpoint before and after the `strcmp` call and see what strings are being compared. 

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing411.png" />
</p>

We can see the expected result of the encrypt call over the input is SASRRWSXBIEBCMPX. Now, in order to reverse it and get what input we must provide, we can simply patch the binary to call `decrypt` rather tan `encrypt` over our provided input and provide SASRRWSXBIEBCMPX as input. Then, while debugging, we can get the output of decrypt.

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing411.png" />
</p>

After doing so, we can see the input that encrypts to SASRRWSXBIEBCMPX is `IKILLWITHMYHEART`.

<p align="center">
  <img src="/images/CTF/AUCTF2020/reversing49.png" />
</p>

The flag is: auctf{static_or_dyn@mIc?_12923}

# Trivia
## Password 1
50
A more secure way to hashing a password involves appending this to the password before the hashing is done.
NOTE: The flag is NOT in the standard auctf{} format
Author: FireKing
### Response: Salt


## Password 2
50
What company fell victim to the largest known breach in history? What year was the full extent of the breach discovered?
NOTE: The flag is NOT in the standard auctf{} format
flag format - company:year
Author: FireKing
### Response: yahoo!:2017

## OSINT 1
50
What President is responsible for the agency that OSINT originated from? (First and Last name)
NOTE: The flag is NOT in the standard auctf{} format
Author: FireKing
### Response: Franklin Roosevelt

## Networking 1
50
What is Layer 7 of the OSI Model?
NOTE: The flag is NOT in the standard auctf{} format
Author: Kensocolo
### Response: application

## Networking 2
50
What protocol dynamically allocates IP Addresses?
NOTE: The flag is NOT in the standard auctf{} format
Author: Kensocolo
### Response: dhcp

## Networking 3
50
What type of packet does ping use?
NOTE: The flag is NOT in the standard auctf{} format
Author: kensocolo
### Response: icmp

## Networking 4
50
What is the range of usable IP addresses with the following: 110.24.52.32/19
NOTE: The flag is NOT in the standard auctf{} format. Enter as first IP - last IP. For example, 192.168.3.1 - 192.168.3.255
Author: Kensocolo
### Response: 110.24.32.1 - 110.24.63.254 

## Pwn
50
What is a countermeasure used to prevent return oriented programming?
NOTE: The flag is NOT in the standard auctf{} format
Author: nadrojisk
## Response: ASLR

## Pwn 2
50
What are the pieces of a rop chain called?
Author: nadrojsk
### Response: Gadget

## Reversing 2
50
What is the deliberate act of trying to make code unreadable by a human in order to prevent tampering and to help ensure security?
NOTE: The flag is NOT in the standard auctf{} format
Author: FireKing
### Response: obfuscation

## Web 1
50
These properties are important to guarantee valid transactions within a database?
NOTE: The flag is NOT in the standard auctf{} format
flag format - list all properties in comma separated list 1, 2, 3,...
Author: FireKing
### Response: atomicity, consistency, isolation, durability 
*acid properties*

## Web 2
50
This web attack takes advantage of web applications that can perform actions input by trusted users without requiring any form of authorization from the user allowing an attacker to perform actions through another user.
NOTE: The flag is NOT in the standard auctf{} format
Author: FireKing
### Respones: Cross-site request forgery

## Reversing 1
281
What person is credited with creating the first assembler and what device was it used in?
NOTE: The flag is NOT in the standard auctf{} format
flag format - person:device
Author: FireKing
### Response: David Wheeler:EDSAC
*More info here: [http://wiki.sjs.org/wiki/index.php/History_of_Computers_-_Assembly_Language](http://wiki.sjs.org/wiki/index.php/History_of_Computers_-_Assembly_Language)*

## OSINT 2
734
Although most federal agencies are involved in OSINT collection there is one federal agency that is the focal point for the exploitation of open source material. They primarily provide information to important government figures. Also what year was it founded?
NOTE: The flag is NOT in the standard auctf{} format
flag format - agency:year
Author: FireKing
### Response: Director of National Intelligence Open Source Center:2005

## Forensics 1
753
What organization developed the archival algorithm used to package Debian's initrd image?
NOTE: The flag is NOT in the standard auctf{} format
Author: FireKing, Vincent
### Response: AT&T Bell Laboratories

## Forensics 2
866
It used to be that you could decrypt a https traffic stream with just the server's private key. What technology removed that capability?
NOTE: The flag is NOT in the standard auctf{} format
Author: FireKing, Vincent
### Response: Diffie-Hellman Key Exchange
*More info here: [https://security.stackexchange.com/questions/71309/it-is-possible-to-decrypt-https-with-the-private-public-pair-if-it-uses-dhe](https://security.stackexchange.com/questions/71309/it-is-possible-to-decrypt-https-with-the-private-public-pair-if-it-uses-dhe)*
