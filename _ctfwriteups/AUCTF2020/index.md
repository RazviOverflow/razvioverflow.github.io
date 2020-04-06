---
title: "AUCTF 2020"
categories: [ctf]
tags: [ctf, writeup, auctf]
hasComments: true
date: 2020-03-21
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

The buffer into the stuck must look like the image below in order to pass all the checks: 

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
