---
title: "NeverLAN CTF 2020"
categories: [ctf]
tags: [ctf, writeup, neverlan, never, lan]
hasComments: true
date: 2020-01-19
image: /images/CTF/neverlan_ctf_2020/0.png
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

We solved all challenges but two of them and finished the CTF in 59th place. It's not that bad if we consider that the first 32 teams are all #1, with the maximum possible score. Shout-outs to my teammates n0rus (Alhuerthor), [@DavidHunter98](https://twitter.com/DavidHunter98) and urzu, and also to [Kashmir54](https://twitter.com/ManuSanchez54), who helped me with some challenges. Also thanks to [Xh4h](https://twitter.com/riftwhitehat) who couldn't participate this time due to personal reasons.

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
# Reverse Engineering
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
>It looks like a script kiddie was trying to build a crypto locker. See if you can get the database back?

The challenge is attached with a file called "encrypted_db". Inspecting its contents with `cat` you will see the file is pretty huge and its contets are of the likes of:  
*(I’ll be using `| head` for the sake of screenshots)*

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_4.png"/>
</p>

If you look closely you can realize it looks like hexadecimal text. In order to translate the text file contents from hexadecimal to ASCII text you can use `xxd` with `-r` (reverse) and `-p` (print) options.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_5.png"/>
</p>

That pretty much looks like Base64.
Decode it using `base64 -d` and you’ll get quite a huge one-line JSON content

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_6.png"/>
</p>

You can copy the whole JSON file and parse it with a JSON beautifier tool and search for “flag”

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_7.png"/>
</p>

The flag is: flag{ENC0D1NG_D4TA_1S_N0T_ENCRY7I0N} *(Yes, looks like they misspelled encryp**t**ion)*

# Forensics
## Listen to this
>You hear that?
*Your flag will be in the normal flag{flagGoesHere] syntax*
-ps This guy might be important

The challenge includes an mp3 file called HiddenAudio.mp3. If you reproduce the audio, you’ll hear a guy talking and some beeps in the background. Inspecting the spectrogram with audactiy you can actually see (in the right track) that the beeps correspond to Morse code. Now the challenge is to isolate it.

That’s how the spectrogram looks like the first time you open the audio:

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_8.png"/>
</p>

The first filter I applied was Vocal Reduction and Isolation

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_9.png"/>
</p>

If you select the period mode of view (right click in the frequencies indicator) you will be able to detect the frequencies where the Morse is (between 500 and 700 approx)

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_10.png"/>
</p>

The second filter I applied was “Equalization” using the following graph:  
*(I’m applying decibels only to the frequencies related to morse code).*

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_11.png"/>
</p>

After applying the filters, you should be able to easily identify the longs, shorts and spaces. Zooming properly will reveal you the data.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_12.png"/>
</p>


The morse is:   
`.._./._../._/__./_../../_/.../._/_./_../_../._/..../.../.._./___/._./._../../.._././`

I translated it with cyberchef

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/ctf_13.png"/>
</p>

Flag is: DITSANDDAHSFORLIFE

# Chicken Little
## Chicken Little 1

>Start here
ssh neverlan@44.233.149.141 -p 3333 password: neverlan
Flags might not be in the normal flag{} format
Save the flag, as you will need it to start the next challenge

This one is pretty straightforward:
<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_1_0.png"/>
</p>


The flag is: eat-chicken-not-cows

## Chicken Little 2

>Start here
level1@44.233.149.141 -p 3333
The password is the flag from the previous challenge
Flags might not be in the normal flag{} format
Save the flag, as you will need it to start the next challenge

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_2_0.png"/>
</p>

Chickens like to **hide**. Inspect hidden files.
The flag is: chrispy-or-breaded

## Chicken Little 3

>Start here
level2@44.233.149.141 -p 3333
The password is the flag from the previous challenge
Flags might not be in the normal flag{} format
Save the flag, as you will need it to start the next challenge

In this level you are told to follow the "BAWKs". There was a file called "BAWKBAKW.txt" with thousands and thousands of lines with the word BAWK. *The file was somewhere around 18MB of size*.

The flag was inside that file and in order to find it a simple search was needed. If you take a look at all the previous flags, all of them are preceded by the level. That is, `level1:flag`, `level2:flag`... So using `grep` or `egrep` and looking for `level3` the flag can be found. 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_3_0.png"/>
</p>

The flag is which-came-first-the-chicken-or-the-bawk

## Chicken Little 4

>Start here
level3@44.233.149.141 -p 3333
The password is the flag from the previous challenge
Flags might not be in the normal flag{} format
Save the flag, as you will need it to start the next challenge

In this challenge there was a binary that contained the flag within it. In order to find the flag `strings` must be used *(luckily the flag was written in default single-7-bit-byte characters. More info about strings encoding [here](http://man7.org/linux/man-pages/man1/strings.1.html))*

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_4_0.png"/>
</p>

The flag is: wut-those-werent-chickens

## Chicken Little 5

>Start here
level4@44.233.149.141 -p 3333
The password is the flag from the previous challenge
Flags might not be in the normal flag{} format
Save the flag, as you will need it to start the next challenge

This challenge had a gzip embedded within another file. Using `binwalk` it can be extracted. 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_5_0.png"/>
</p>
<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_5_1.png"/>
</p>

The flag is: is-the-sky-falling?

## Chicken Little 6

>Start here
level5@44.233.149.141 -p 3333
The password is the flag from the previous challenge
Flags might not be in the normal flag{} format
Save the flag, as you will need it to start the next challeng

This challenged had a .JPG file containing the flag. Since you cannot inspect the image remotely because you had no graphical environment, using `scp` you could copy the image to your machine and visualize it. 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_6_0.png"/>
</p>

`scp -P 3333 level@IP:/image/path /local/location/to/copy/image`

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_6_1.png"/>
</p>

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_6_2.png"/>
</p>

The flag is: i-was-right-all-along-it-was-falling

## Chicken Little 7

>Start here
level6@44.233.149.141 -p 3333
The password is the flag from the previous challenge
Flags might not be in the normal flag{} format
Save the flag, as you will need it to start the next challenge

When you connect the server tells you the password is less than 5 characters

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_7_0.png"/>
</p>

Since the level is talking about "cracking the password", it is obviously a task for **John the Ripper** or **Haschat**.

The hash from `/etc/shadow` is: *(you had permission to inspect it)*

```
level7:$6$Avlq2aF8$dHQkjNT0H/YH9EeL0N/uyGaizeW83stNbvD8/P0jbetBzhI5hQYbLwe/FpXYju11qQHKVxOPtwZQ3ZGdRAvo0.:18303:0:99999:7:::
```

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_7_1.png"/>
</p>

Copy the hash to a new file. Only the hash.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_7_2.png"/>
</p>

Now we need a valid wordlist. Since we already know the password is less than 5 characters long, we can use `crunch` to generate a valid dictionary. More info about [crunch](https://tools.kali.org/password-attacks/crunch). *Please notice how I generated a wordlist from 1 to 5 characters long, but it'd have been enough from 1 to 4 since the server tells you the password is strictly less than 5 characters long.*

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_7_3.png"/>
</p>

Now it's time to use `hashcat`. Hashcat has a lot of options and algorithms, in order to know which one to use you can use hashcat help page. `hashcat --help`. Within the man page you can find all modes of operation and specifically the one we're looking for. It is `$6 sha512crypt`.

More info about hashcat [here](https://hashcat.net/hashcat/). You can find examples of every single hashing algortihm [here](https://hashcat.net/wiki/doku.php?id=example_hashes).

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_7_4.png"/>
</p>

Run `hashcat` with `-m 1800` (hashing algorithm to break) and `-a 0` (attack type) to break the password. The bruteforcing was meant to be done locally, not remotely. I suspect a lot of people tried to break the password remotely thus saturating the AWS Instances. 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/chicken_little_7_5.png"/>
</p>

The flag is: bawk

# Trivia
## Milk Please!

>Trivia Question: a reliable mechanism for websites to remember stateful information. Yummy!

The flag is: cookie

## Professional guessing

>The process of attempting to gain Unauthorized access to restricted systems using common passwords or algorithms that guess passwords

The flag is: password cracking

## Base 2^6

>A group of binary-to-text encoding schemes that represent binary data in an ASCII string format by translating it into a radix-64 representation

The flag is: base64

## AAAAAAAAAAAA! I have CVE's

>This CVE reminds me of some old school exploits. If is enabled in sudoers

This question was not so simple. Since the title is a bunch of A's it's clearly a reference to buffer overflow exploitation. 

You have to use cve.mitre.org search engine for the term “buffer overflow” [https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=buffer+overflow](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=buffer+overflow). Once you get the results, look for “sudoers”. The first occurrence is [https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-18634](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-18634). Within the text you can read `...if pwfeedback is enabled…`.

The flag is: pwfeedback

## Rick Rolled by the NSA??

This CVE Proof of concept Shows NSA.gov playing "Never Gonna Give You Up," by 1980s heart-throb Rick Astley.

The flag is: CVE-2020-0601

# Programming
## BitsnBytes

>https://challenges.neverlanctf.com:1150

When you enter the site you can see the server responds with a simple SVG image. (https://challenges.neverlanctf.com:1150/svg.php) 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/bitsnbytes_0.png"/>
</p>

Since the title of the challenge is a hint, I translated the image into bits. Dark squares are translated into a 0 bit and clear squares into a 1 bit. The result is something like:

```
01110100011010010110110101100101001000000110100001100001011100110110100000111010001110000011011000111001001110010011000000110001001101010110010101100100011000110110011000110000011001000110010000110010001101100110001101100011011000110011000100110111001110010110001101100001001100100110010100111000011001100011010001100001011001100011001001100101011000100011000000110110011000010110001101100100001101010011011101100011001100010011100001100101001101010110000101100100001101100011000101100011011001010011010101100001001101100011011000110110011000100011011100110100001101110011001
```

Now the bits are translated into bytes and then into ASCII text *(you can use online Cyberchef tool. "From binary" option)*. After translation the text was something like `time hash:someRandomHashValue`. There was nothing about it. When searching about what `time hash` is and how to decode it, nothing promising was found.

**However**, we notices that the image changed every 45 seconds or so. So we decided to create a Python script to automatically and constantly download the images and translate them into text. We left the script running for like 12 minutes and the flag appeared. 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/bitsnbytes_1.png"/>
</p>

I saved the XML corresponding to the file. You can find it here: [https://pastebin.com/46NK0ffC](https://pastebin.com/46NK0ffC)

The script used to download and translate the images is the following one:

```python
#!/usr/bin/python3
# RazviOverflow

from xml.dom import minidom
import requests

if __name__ == "__main__":
    while True:
	    fname = 'svg.php.svg'
	    url = 'https://challenges.neverlanctf.com:1150/svg.php'
	    r = requests.get(url)
	    #print(r.content)
	    open(fname , 'wb').write(r.content)
	    svg_file = 'svg.php.svg'
	    doc = minidom.parse(svg_file)  # parseString also exists
	    path_strings = [path.getAttribute('style') for path
	                    in doc.getElementsByTagName('rect')]
	    doc.unlink()

	    bits_list = []
	    for fill in path_strings:
            if fill == 'fill:#00ff00':
                bits_list.append('0')
            else:
                bits_list.append('1')

	    final_bits_string = ''.join(bits_list)
	    print(bytes(int(final_bits_string[i : i + 8], 2) for i in range(0, len(final_bits_string), 8)))
```


The flag is: flag{its_all_ab0ut_timing}


# Recon
## The big stage

>One time we keynoted @SaintCon... i think I remember hiding a flag in our pres.

If you google for “Keynote saintcon” and look on images you’ll actually find the logo of neverlan ctf.  
[https://www.google.com/search?q=keynote+saintcon&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjt3rfLosPnAhUK4BoKHWG-C_sQ_AUoAXoECAwQAw&cshid=1581210259334867&biw=1920&bih=969](https://www.google.com/search?q=keynote+saintcon&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjt3rfLosPnAhUK4BoKHWG-C_sQ_AUoAXoECAwQAw&cshid=1581210259334867&biw=1920&bih=969)

If you follow it, you’ll reach one of neverlan’s twitter post.   
[https://twitter.com/neverlanctf/status/1044640438131388422](https://twitter.com/neverlanctf/status/1044640438131388422)

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/thebigstage_0.png"/>
</p>


The post links you to a Google drive doc.  
[Link to GDocs document](https://docs.google.com/presentation/d/1v_Pj4s5zVxBKXcq5ySPBwQVSXW2dhDm1jkKfU3AJx3w/edit#slide=id.g4276f19bda_0_48)

If you look for “flag” you’ll eventually find it.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/thebigstage_1.png"/>
</p>

The flag is: flag{N3v3r_g0nna_g1v3_y0u_up}

## The Link

>NeverLAN's secret Track 2.

If you visit neverlan dj’s page [https://live.neverlanctf.com/](https://live.neverlanctf.com/), you’ll notice there are actually 2 tracks. Click on "track 2" and you'll find out it's and embedded YouTube video. The track being played is:  
[https://www.youtube.com/watch?time_continue=3](https://www.youtube.com/watch?time_continue=3).

In order to get the flag you must scroll through the comments (order them by date, most recent first) and you will randomly encounter the flag.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/thelink_0.png"/>
</p>

The flag is: flag{10684524746ba936b43a82d84385dcf5}

# Web
## Stop The Bot

>https://challenges.neverlanctf.com:1140 

Visiting the page you'll find it looks like a normal page. 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/stopthebot_0.png"/>
</p>

It talks about bots, so I intuitively tested robots.txt [https://challenges.neverlanctf.com:1140/robots.txt](https://challenges.neverlanctf.com:1140/robots.txt). 

You’ll find that `/flag.txt` is disallowed.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/stopthebot_1.png"/>
</p>

Simply visit [https://challenges.neverlanctf.com:1140/flag.txt](https://challenges.neverlanctf.com:1140/flag.txt) to get the flag.

Flag is: flag{n0_b0ts_all0w3d}

Another alternative is to mirror the entire directory using, for example, wget -m https://challenges.neverlanctf.com:1140/. By doing so robots.txt will be downloaded.

## SQL Breaker

>https://challenges.neverlanctf.com:1160/ 

When you enter the site [https://challenges.neverlanctf.com:1160/](https://challenges.neverlanctf.com:1160/) you will see a login form. Since we already know it’s vulnerable to SQL Injection, it’s just a matter of tryouts in order to guess the engine behind. In this case it’s Mysql.

In order to start session insert as user: `‘ OR ‘1’=’1’#`. Password can be whatever you want. We don’t care about it since “#” will comment the rest of the query so the result will be something like `SELECT * FROM users WHERE user = ‘’ OR ‘1’=’1’# AND password=’yourpassword’`.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/sql_0.png"/>
</p>


Login and you will be admin.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/sql_1.png"/>
</p>


The flag is : flag{Sql1nj3ct10n}

## SQL Breaker 2

>https://challenges.neverlanctf.com:1165/

This time if you test the exact same input as before, you will log in but as a user without privileges.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/sql_2.png"/>
</p>

If you notice, “only \`admin\` users” can view the flag. Backticks have a special meaning in MySQL. They are called quoted identifiers and they tell the parser to handle the text between them as literal string. [https://dba.stackexchange.com/questions/23129/benefits-of-using-backtick-in-mysql-queries](https://dba.stackexchange.com/questions/23129/benefits-of-using-backtick-in-mysql-queries).

So lets try to login using the new `admin` keyword.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/sql_3.png"/>
</p>

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/sql_4.png"/>
</p>

The flag is: flag{esc4p3y0ur1nputs}

## Browser Bias

>https://challenges.neverlanctf.com:1130

When you enter the site you will see the following message: “Sorry, this site is only optimized for browsers that run on commodo 64”. In order to see the “optimized” page you must trick the server into thinking that you are actually using a commodo64 machine. To do so, you have to change the user agent.

From Google Chrome’s developer tools select “Network Conditions” and change the user agent to Contiki/1.0 (Commodore 64; http://dunkels.com/adam/contiki/) . Source: [https://gist.github.com/dstufft/2502524](https://gist.github.com/dstufft/2502524). 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/browserbias0.png"/>
  <img src="/images/CTF/neverlan_ctf_2020/browserbias1.png"/>
</p>

<p align="center">
 
</p>


Once you’ve changed it simply reload the page. The server will give you the flag.

The flag is: flag{8b1t_w3b}

# Crypto
## Pigsfly

The challenge includes a .png image. When you download the file and open it, you’ll see the following image.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/pigsfly_0.png"/>
</p>


That looks like pigpen cipher

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/pigsfly_1.png"/>
</p>

More info about pogpen cipher: [https://en.wikipedia.org/wiki/Pigpen_cipher](https://en.wikipedia.org/wiki/Pigpen_cipher).

The flag is: flag{d0wn_and_d1r7y}

## Base not 64

The original text provided by the challenge was 
```
ctp62tvvehm6jwvfdtjq6vvedhwk6ch144rj2z8====
```

The admins later updated the challenge with a new text. The curious think about this is that at the time they changed the text because it was not working, there were people that solved it. Strange. 

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/basenot64_0.png"/>
</p>

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/basenot64_1.png"/>
</p>


<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/basenot64_2.png"/>
</p>


New text: 
```
ORUGS43PNZSXG33ONR4TGMRBEEYSC===
```

As the title says, it’s not b64. It’s actually b32.

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/basenot64_3.png"/>
</p>

The flag is: flag{thisonesonly32!!1!}

## Dont Take All Knight

The challenge includes the following image:

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/templarcipher_0.png"/>
</p>

As the title says, this one is about Knight hence the Templar Cipher

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/templarcipher_1.png"/>
</p>

You can use dcode.fr to decode it [https://www.dcode.fr/templars-cipher](https://www.dcode.fr/templars-cipher)

The image translates into: `FLAGISEVENKNIGHTSNEEDCRYPTO`

The flag is: EVENKNIGHTSNEEDCRYPTO

## The invisibles

The challenge included the following image:

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/invisibles_0.png"/>
</p>

The title of the challenge is once again a hint. This time the substitution cipher is “Arthur and the Invisibles”.You can use this page to decode it [https://www.dcode.fr/arthur-invisibles-cipher](https://www.dcode.fr/arthur-invisibles-cipher)

The image translates to: `FLAGISSYOUCANSEETHEM`.

The flag is: YOUCANSEETHEM

## Baby RSA

>We've intercepted this RSA encrypted message 2193 1745 2164 970 1466 2495 1438 1412 1745 1745 2302 1163 2181 1613 1438 884 2495 2302 2164 2181 884 2302 1703 1924 2302 1801 1412 2495 53 1337 2217 we know it was encrypted with the following public key e: 569 n: 2533

The first thing to do is get a private key to decrypt it. That means, factoring the prime n. In order to do so, we can use the almighty [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool). First of all, let’s create a valid public key from the given parameters.

`./RsaCtfTool/RsaCtfTool.py --createpub -n 2533 -e 569 > publickey`

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/babyrsa_0.png"/>
</p>

Now, let’s try to crack it and obtain a valid private key. In order to do so, you can use the following command.

`./RsaCtfTool/RsaCtfTool.py --publickey publickey --private > private_key`

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/babyrsa_1.png"/>
</p>

As you can see the prime was already factored and published on [factor.db](http://factordb.com/).

Now let’s dump information about the private key using the command:

`./RsaCtfTool/RsaCtfTool.py --dumpkey --key private_key`

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/babyrsa_2.png"/>
</p>


Now that we have the parameters d and n, we can decrypt each individual character of the original input. In order to do so, a simple python script will be enough.
```python
a = [2193,1745,2164,970,1466,2495,1438,1412,1745,1745,2302,1163,2181,1613,1438,884,2495,2302,2164,2181,884,2302,1703,1924,2302,1801,1412,2495,53,1337,2217]
b = []
d = 1673
n = 2533

for number in a:
    b.append(chr(pow(number, d, n)))

print(''.join(b)
```

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/babyrsa_3.png"/>
</p>

The flag is: flag{sm4ll_pr1m3s_ar3_t0_e4sy}

## My own encoding

>Here's an encoding challenge. This doesnt really test your technical skills, but focuses on your critical thinking.
I wrote my own encoding scheme. Can you decode it?"

The challenge provides the following image:

<p align="center">
  <img src="/images/CTF/neverlan_ctf_2020/myownencoding_0.png"/>
</p>


After some research we found out it is actually a modification of the [Bifid Cipher](http://bestcodes.weebly.com/bifid-cipher.html). If you read about it you’ll notice there is always at least one cell that represents more than one letter. In order to solve this challenge, think that the english alphabet has 26 chars and the grids are 5x5=25 cells. So there must be some overlapping.

You must place the letters of the alphabet within the cells on a letter-per-cell basis and wherever there is a black cell you must place the current letter and the next one. Applying this method and taking into account only black cells, you have:

`m/n h/i b/c d/e i/j n/o a/b x/y n/o t/u g/h ?? b/c j/k d/e q/r` where question mark represents the grid that has no black cell.

Looking closely at the cells that represent two letters, you can realize that taking always the right-position letter gives you the following message: nicejobyouh???cker. By context we can replace question marks with “a”.

The flag is: nicejobyouhacker
