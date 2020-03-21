---
title: "RIFTCTF 2020"
categories: [ctf]
tags: [ctf, writeup, riftctf]
hasComments: true
date: 2020-03-21
image: /images/CTF/RIFTCTF2020/CTF_Logo.png
description: RIFT CTF 2020 challenge writeups. 
---

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/CTF.jpg" width="500"/>
</p>

Main event page: [https://technovate.iiitnr.ac.in/](https://technovate.iiitnr.ac.in/)
Main CTF page: [http://riftctf.iiitnr.ac.in:8000/](http://riftctf.iiitnr.ac.in:8000/)

RIFTCTF 2020 was the first CTF organized by the IIIT Naya Raipur as part of their [Technovate 2020](https://technovate.iiitnr.ac.in/) event. There were some problems with the infrastucture and some challenges were not working as intended. In addition, the flag format was unclear in most of the challenges what led us to a lot of guessing. *Guessing is not nice :P*. However, it's not all bad news, the challenges we managed to solve were pretty enjoyable (we also enjoyed those we didn't solve) and we learned throughout the process which, as always, is main objective. 

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/scoreboard.png" width="500"/>
</p>

I'd like to thank [Kashmir54](https://twitter.com/ManuSanchez54) and [liti0s](https://twitter.com/DavidHunter98) for participating along with me.

The CTF had several categories. In this page you will find the following writeups:
  - Reverse Engineering:
    - Chall 1 and Chall 2.
  - Forensics:
    - Chall 2.
  - Crypto:
    - Crypto 0x0001, 0x0004, 0x0005 and 0x0007.
  - OSINT:
    - Osint 0x004 and 0x0005.

# Reverse Engineering
## Chall 1

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/rev1_0.png"/>
</p>

This challenge was pretty easy since the password was hardcoded, that is, it was stored as plain ASCII in the .rodata section of the EFL. Using `strings` or any other null-terminated strings finder gives you the flag. 

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/rev1_1.png"/>
</p>

Or you could inspect full contents of the ELF section with `objdump`.

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/rev1_2.png"/>
</p>

The flag is: riftCTF{tr4c1ng-mAkes-17-SUPeR-345Y}

## Chall 2

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/rev2_0.png"/>
</p>

I used `Cutter` to reverse the binary. The `main` calls `fcn.00001165` with some parameters and prints *Correct password* if the return value of the call is 0. 

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/rev2_1.png"/>
</p>

In case you're wondering why there are no function names: it's because the binary is [stripped](https://en.wikipedia.org/wiki/Stripped_binary).

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/rev2_3.png"/>
</p>

Looking at the code of `fcn.00001165` we can see it performs a bitwise XOR with 0x55 and every character of the user input. *Notices that I renamed some variables so it is easier to understand.*. Then it XORs again with every each character of the original expected password. Then it performs a bitwise OR with the first 32 bits of i, that is, it performs OR with itself. That's the way the compiler checks if the result of each iteration of XORs is equal to 0. 

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/rev2_2.png"/>
</p>

Maybe looking at the disassembly code and not the decompiled one is easier to understand what's happening here. 

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/rev2_5.png"/>
</p>
<p align="center">
  <img src="/images/CTF/RIFTCTF2020/rev2_4.png"/>
</p>

Basically the program is checking whether the result of XORing each character from the user input with 0x55 equals to the second parameter received by the function. That is, the expected password. Looking at how the main calls `fcn.00001165`, we can see the second passed parameter is "\'<3!\x16\x01\x13.!\'a6<;2\n1ef&;!\n\"e\'>\n4;,\x18e\'ff(". So, given the properties of XOR, in order to get the correct password we must XOR each character from the previous string with 0x55.

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/rev2_6.png"/>
</p>

The flag is: riftCTF{tr4cing_d03snt_w0rk_anyM0r33}

# Forensics
## Forensics 2

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/forensics2_0.png"/>
</p>

This challenge was as simple as analyzing the .zip file and extracting its contents.

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/forensics2_1.png"/>
</p>

The flag is: riftCTF{Y0u-M4st33r3-THE_ZIP_FILE-\x50\x4B\x01\x02}

# Crypto
## Crypto 1

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/crypto1_0.png"/>
</p>

The flag was just a message encoded multiple times as base64.

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/crypto1_1.png"/>
</p>

The flag is: riftCTF{Its_4LL_ab0ut_BaS3}

## Crypto 4

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/crypto4_0.png"/>
</p>

The challenge included the following image:

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/crypto4_1.png"/>
</p>

The flags correspond to the [International Maritime Signal Flags](https://en.wikipedia.org/wiki/International_maritime_signal_flags ).

The flag translated to riftctf{justa7r1but3t0armedforces} but it was incorrect. After asking some CTF organizers, turns out the flag was riftCTF{just_a_7r1but3_t0_armedforces}.

## Crypto 5

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/crypto5_0.png"/>
</p>

The challenge included the following image:

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/crypto5_1.png"/>
</p>

It is dagger alphabet. You must just translate the message. 

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/crypto5_2.png"/>
</p>

The flag is: riftctfbonjourelliot

# Crypto 7

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/crypto7_0.png"/>
</p>

The challenge included the following image:

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/crypto7_1.png"/>
</p>

It's a strange alphabet (yet another substitution algorithm). You can use [https://www.dcode.fr/hylian-language-twilight-princess](https://www.dcode.fr/hylian-language-twilight-princess) to decode it. 

The flag is: riftctf{survival_of_the_fittest} (separate words with "_")


# OINT
## Osint 4

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/osint4_0.png"/>
</p>

The challenge included the following image:

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/osint4_1.png" width="400"/>
</p>

After researching for some time I found out it is a Ford Ka 2nd generation.

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/osint4_2.png" width="600"/>
</p>

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/osint4_3.png" width="400"/>
</p>

The flag is: Fordka 2008 *I know, it makes no sense. According to the challenge description it should've been Ford 2008.*

## Osint 5

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/osint5_0.png"/>
</p>

In this challenge you had to find the country where the IP is hosted in. 

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/osint5_1.png"/>
</p>

The IP is indeed a network camera. You can find the country simply by asking `whois` about the ip.

<p align="center">
  <img src="/images/CTF/RIFTCTF2020/osint5_2.png"/>
</p>

The flag is: The flag is: riftctf{Belgium}