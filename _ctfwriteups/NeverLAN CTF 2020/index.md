---
title: "NeverLAN CTF 2020"
categories: [ctf]
tags: [ctf, writeup, neverlan, never, lan]
hasComments: true
date: 2020-01-19
image: /images/CTF/h-c0n/2020/hc0n2019logo.png
description: NeverLAN CTF 2020 challenges writeups. 
---

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/0.png"/>
</p>

Main event page: [https://neverlanctf.com/](https://neverlanctf.com/)  
Main CTF page: [https://ctf.neverlanctf.com/](https://ctf.neverlanctf.com/)

Some friends and I participated in NeverLAN CTF 2020, an online CTF with entry-level challenges. The CTF overall was pretty nice, even though there were some technical difficulties and we were somewhat penalized because of the time zone. I enjoyed the experience and learned a lot. That's the most important part and where the fun really is, learning in the process. The prize or actual number one of the competition is secondary. 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/scoreboard.png"/>
</p>

We solved all challenges but two of them and finished the CTF in 59th place. It's not that bad if we consider that the first 32 teams are all #1, with the maximum possible score. 

The CTF had several categories including reverse engineering, crypto, pcacp, forensics, programming, recon, web, *chicken little* and trivia. We solved a lot of challenges but, unfortunately, couldn't document them all. The writeups you can find in this page are:

- Pre-CTF challenges: [https://prectf.neverlanctf.com/](https://prectf.neverlanctf.com/)
	- Web: Cookie monster, Javascript password & What the header
	- Crpyto: Base64, Morse Madness & Crypto Box
- CTF challenges:
	- Reverse Engineering: Adobe Payroll & Script Kiddie
	- Forensics: Listen to this
	- chicken Little: 1, 2, 3, 4, 5, 6 & 7
	- Trivia: Milk Please!, Professional guessing, Base 2^6, I hate CVEs, Rick Rolled by NASA??
	- Programming: BitsnBytes
	- Recon: The big stage, The Link
	- Web: Stop the Bot, SQL Breaker, SQL Breaker 2, Browser Bias
	- Crypto: Pigsfly, Base not 64, Dont Take All Knight, The Invisibles, Baby RSA, My own encoding

# Pre-CTF challenges
## Cookie Monster

When you enter the challenge, you are redirected to https://prectf.neverlanctf.com/challenges/CookieMonster/. The page contains the following message: “He's my favorite Red guy”.

You can use your browser’s development tools in order to inspect the cookies, given the name of the challenge. You’ll find a cookie named “Red_Guy’s_Name” whose value, by default, is “NameGoesHere”

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/prectf_1.png"/>
</p>

You will have to use a bit of intuition. Since the name of the challenge is “Cookie Monster” and they are talking about “Red” guy, with capital R… there is only one possibility: Sesame Street. 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/prectf_2.png" width="300"/>
</p>


Change cookie’s value from “NameHoesHere” to “Elmo” and reload the page. The server will respond you with the flag.

The flag is: flag{C00kies_4r3_the_b3st}


## Javascript password

When you enter the challenge, you are redirected to https://prectf.neverlanctf.com/challenges/JavascriptPassword/. The page asks you about some password unguessable.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/prectf_4.png"/>
</p>

You can inspect the source code with your browser’s development tools or simply pressing CTRL+U (Google Chrome). You’ll notice there is an embedded JavaScript code.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/prectf_5.png"/>
</p>

The flag is hardcoded after the sequence of if(true)s. You can also test it, submitting the text “Zesty Rules”. The page will give you the flag. 

The flag is: flag{server>browser}

## What the header

You are redirected to https://prectf.neverlanctf.com/challenges/WhatTheHeader/. The page says “You Already have what you need.”
Given the name of the chall, one must inspect whatever headers there might be. 
When inspecting the HTML body, a comment tells you that’s not the header you’re looking for.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/prectf_6.png"/>
</p>

You can also inspect HTTP headers using development tools. If you do so, you’ll notice there is a response header called “neverlanheader” that contains the flag.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/prectf_7.png"/>
</p>

The flag is: flag{much_cust0m_v3ry_h34der}

## Base64

This challenge is pretty self explanatory. You are given the following string: `ZmxhZ3tiYXNlNjRfaXNfZWFzeX0=`. 

Use whatever tool you consider to base64 decode the message.
The flag is: flag{base64_is_easy}

## Morse Madness

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/prectf_8.png"/>
</p>

This challenge is also pretty self explanatory. Morse decode the text in order to get the flag. "hen you decode it, you will get something similar to “flag beep-b00p”. Please bear in mind the format of previous flags: flag{lowercase}

The flag is: flag{beep-b00p}

## Crypto Box

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/prectf_9.png"/>
</p>

In this chall you will have to find out what cipher algorithm was used to encrpyt the flag. You are already provided with the key. 
I recommend you to always start with the easiest, classic ciphers. Since you’re provided with a key, there are not so many ciphers to test. 

Vigènere is the one you’re looking for. 
The flag is: flag{can_you_crypto}

# CTF Challenges
## Adobe Payroll
>We've forgotten the password to our payroll machine. Can you extract it?
Your flag will be in the flag{flagGoesHere} syntax.

The challenge is attached with a couple of files. One of them is a Windows PE (Portable Executable) binary and the other is a markdown file called “description” that tells you to take a look at “dotPeek” (a .NET disassembler). Since this is a .NET PE you can use dotPeek or any other disassembly tool you like. I used IDA. 

Looking at the imported funcionts you can easily realize there are interesting functions like `checkUsername` and `checkPassword`.
<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_0.png"/>
</p>

You can inspect their code individually. `checkUsername`:
<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_1.png"/>
</p>
It checkes whether the username is "admin".

`checkPassword`:
<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_2.png"/>
</p>
It checks whether the password is "bmV2ZXJfZ29ubmFfZ2l2ZV95b3VfdXAh".

Using these credentials you can obtain the flag. 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_3.png"/>
</p>

The flag is: flag{.net_is_pretty_easy_to_decompile}

## Script Kiddie
