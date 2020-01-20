---
title: "Hackplayers h-c0n CTF Qualifiers 2020"
categories: [ctf]
tags: [ctf, writeup, h-c0n, hackplayers]
hasComments: true
date: 2020-01-19
image: /images/CTF/h-c0n/2020/hc0n2019logo.png
description: H-c0n Hackplayers Conference is a nice security conference held in Spain. Here are our writeups for the solved challenges. 
---
<p align="center">
  <img src="/images/CTF/h-c0n/2020/hc0n2019logo.png" width="400"/>
</p>

Main event page: [https://www.h-c0n.com/p/home.html](https://www.h-c0n.com/p/home.html)  
Main CTF page: [https://www.h-c0n.com/p/ctf.html](https://www.h-c0n.com/p/ctf.html)

H-c0n Hackplayers Conference is a nice security conference held in Spain and this time some friends and I participated in their online CTF Qualifier (January 2020). I participated in a three-members team alongside Alhuerthor and [@DavidHunter98](https://twitter.com/DavidHunter98). There were a total of 268 players, 149 registered teams and 73 teams that solved at least one challenge. We ended up in 11th position and learnt a lot. I'm eager for the next live CTF we can get into and we are slowly building the addiction to them :)  
Congratulations to the top 6 teams that managed to qualify for the finals. Good luck!

<p align="center">
  <img src="/images/CTF/h-c0n/2020/scoreboard.png" width="700"/>
</p>

The CTF had several challenges in various categories such as reversing, binary exploiting, steganography, cryptography, radio, boot2root and forensics. The challs we managed to solve are:

 - Weird Sanity Check (Welcome challenge)
 - Kojo No Mai (Crypto)
 - Baby Malicious (Forensic)
 - Ok, I got this (Radio)
 - Samurai (Stego)
 - User flag and Machine flag (Boot2Root)
 - Modulated secret (Radio)

## Weird Sanity Check (Welcome)
>Welcome to h-c0n qualifier CTF 2020!  
Each flag will follow the format "H-c0n{" + MD5 + "}".  
Here is your weird welcome flag:

This challenge was all about inspecting the source code of its description window. Hidden as a comment there was a very large and strange text. 
```
FMVSWKZLFMVSWKZLLM7CWPRLFMVT4KZLFMVSWKZLHYVSWKZLFMVSWKZLFM6DYPB4FVOT4PR6FMVS4PBLFMVSWKZLFMVSWKZLFMVSWKZOHY7C2LR4HQVSWKZOHY7CWKZLFMVSWKZLFMVSWLRLFMVSWKZLFMVSWKZLFMVS4PB4FMVSWKZLFMVSWLRNFUWS2LJOFUXC2LRLFMVSWKZLFMXD4KZLFMVSWKZLFMVSWKZLFMVSWKZLFMVSWKZLFMVSWLRLFMXDYLJNFUWS2LRLFY7C4PBNFUWS4KZLFMVSWKZLFYWS2LJNFUXCWLR6FY6C2LJOFMVSWKZOFMXCWLRNFUWS2LJNFUXD4KZLFMXC2LR4FMVSWLR6FUWS2LRLFMXCWLR4FMVSWKZLFYWS2LJNFUWS2LJOFMVSWKZLFMVS4PROFY6C2LJNFUXD4PRLFMXA====
```
It defnitiley looks like base64 but it is not. It's actually base32. To decode it we can use whatever online tool like [this one](https://www.dcode.fr/base-32-encoding).  
The decoded result is a combination of `+`, `.`, `[`, `]`, `-`. `>` and `<`.
```
++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++.<+++++++++++++++.>>-.<<+++.>>+++++++++++.+++++++++++++.<<++++++++.-----.-.-.+++++++.>+++++++++++++++++++++++++.++.<-----.+.>.<---.+++++++.-----.+.>.<--.++++.+.+.-------.>+++.-.<+++.>---.++.+.<+++++.--------.+++++++.>..<----.>>++.���s
```

This code is easily recognizable, it is [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck). There are a lot of online brainfuck interpreters like [this one](https://copy.sh/brainfuck/).

Executing the brainfuck code prints the flag:
```
H-c0n{83218ac34c1834c26781fe4bde918ee4}
```

## Kojo No Mai (Crypto)
>Prunus Incisa "Kojo No Mai" is the Japanese name for a dwarf or bonsai cherry. Although small things can be precious it is not a good idea to use them in cryptography ... cause usually with a small key it is easier to break the encryption, right?

In this challenge we had to download a file whose content was:
```
-----BEGIN PUBLIC KEY-----
MCwwDQYJKoZIhvcNAQEBBQADGwAwGAIRAOSpZLB7VXE7iZA72YTS85UCAwEAAQ==
-----END PUBLIC KEY-----

XnZvSmNqZqz+N5LL+ec6XA==
k4TD9AHouSlxdn97PXfmOg==
FhHp7W1orCt78mlz5PNGBQ==
a5FPpzeDX29qOriH2kS64A==
XCWOYhWFC6v3wa3qM58v5g==
qlLYhsaMWbOvCXddqsQ/pA==
i1jClSfyTf8XLiT57Su6IQ==
DZbTy4vMKW0WqjrD7CspMg==
```

As we can see there is a public key and what looks like several b64 encoded ciphertexts. We know they are different messages because each b64 encrypted message ends with `==`. If we try to decode one of them the result is incomprehensible since the message is encrypted. 

Information about the public key can be retrieved using `openssl`:
```
openssl -rsa -pubin -in kojonomai.txt -text -noout
```
![](/images/CTF/h-c0n/2020/openssl_rsa_1.png)

We next placed the public key in its own file and tried to break it with the allmighty [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool). Launching the tool does indeed break/factor the public key and we can obtain a corresponding private key. Turns out the modulus was already factored and it's posted at [factordb](http://factordb.com/).
```
RsaCtfTool.py --publickey publick_key.key --verbose --private
```
![](/images/CTF/h-c0n/2020/rsactf_1.png)

We export the private key to a file so we can use it to obtain the plaintexts. In order to decipher the ciphertexts you can use either `openssl rsautl` or `RsaCtfTool`. We used `openssl rsault` wit the following command:
```
openssl rsautl -decrypt -in cipher -out plaintext -inkey private_key
```
Please note that *cipher* in the previous command is a file containing a single ciphertext from the original provided file. The command outputs an RSA operation error because the *<red>data is greater than the mod len</red>*.

![](/images/CTF/h-c0n/2020/rsactf_2.png)

This happens because the message is too long and in order to supress this error we must provide the input as bytes and not as base64. You can read more about this error and find the solution [here](https://stackoverflow.com/questions/23205592/openssl-data-greater-than-mod-len).  
In order to do so we have to simply base64 decode the ciphertext. We can use the Kali preinstalled `base64` tool.
```cat cipher | base64 -d > rawcipher```
Now, when trying again to decrypt it using the private RSA key:

![](/images/CTF/h-c0n/2020/rsactf_3.png)

We get the first characters of the flag. This means the flag was split across the ciphertext we were originally given. So we base64 decode every single ciphertext and then decrypt them with the private RSA key, one by one. When reading all the resulting files we get the flag:

![](/images/CTF/h-c0n/2020/rsactf_4.png)

```
H-c0n{1aa36c2eb49a2f427e57c715bda839e6}
```


## Baby Malicious (Forensic)
>You are in a forensic department, there is an aggressive malware campaign and your colleagues in the Incident Management department have sent you the following obfuscated macro to analyze.

In this challenge the downloaded file is an obfuscated [VBA](https://en.wikipedia.org/wiki/Visual_Basic_for_Applications) (Visual Basic for Applications). There are different tools that can analyze VBA files but we root for [ViperMonkey](https://github.com/decalage2/ViperMonkey). *(oletools are also very effective)*

ViperMonkey prints out the following analysis results:

![](/images/CTF/h-c0n/2020/baby_malicious_1.png)

So the script is opening a Shell and downloading something from https://bit.ly/2NgCC0O. It's also important to keep in mind the author's debug print: `BPStegano with SALCHICHON`.

The link downloads an image called *whereisyourgod.png*:  
![](/images/CTF/h-c0n/2020/whereisyourgod.png)

Using `binwalk` to find possible hidden files within it had no possitive results. The next thing we did was use the author's hint about [BPStegano](https://github.com/TapanSoni/BPStegano).  

Once BPStegano is installed we execute it and try to extract the secret from the image using `SALCHICHON` as password.

![](/images/CTF/h-c0n/2020/baby_malicious_2.png)
![](/images/CTF/h-c0n/2020/baby_malicious_3.png)

The tool successfully extracts the hidden message. The flag is:
```
H-c0n{5619b327cc5ecce85a7fc99a14a6c5c5}
```

## Ok, I got this (Radio)
> We have seen a boy with an antenna next to the garage door. In one of his hands it seemed to have a yardstick one. Can you help us find out what the boy was trying to send?

Props to [Kashmir54](https://twitter.com/ManuSanchez54) for giving us a helping hand with this one!

In this callenge we were given a .wav file. The first thing we did (s*after analyzing the .wav file with tools like `file`, `binwalk`, etc...*) was opening it with [Audacity](https://www.audacityteam.org/) and try to play it. 
*<red>Playing the sound resulted in an insta RIP for our ears, even though we were prepared for it and lowered system's volume.</red>*

Timeline of Audacity:  
![](/images/CTF/h-c0n/2020/radio1_1.png)

Reproducing the file results in an unintelligible high-pitched noise. Nevertheless, zooming in the sound graph is pretty elucidating/enlightening. 

Zoomed-in timeline of Audacity:  
![](/images/CTF/h-c0n/2020/radio1_2.png)

We can clearly see the high and low notes. So we thought this could be a representation of zeros `0` and ones `1` i.e. crafting the resultant file on a bit basis. 

In order to analyze the .wav and extract all the bits we used Python and two modules: [wavefile](https://pypi.org/project/wavefile/) and [BitVector](https://pypi.org/project/BitVector/). [Here](https://stackoverflow.com/questions/2060628/reading-wav-files-in-python) you can find some examples of wavefile usage and how to obtain sound parameters like frecuencies, number of frames, etc...

We measured the minimum length of the higher notes and it turns out to be <yellow>739</yellow> frames. So we assumed each bit is 739 frames long. We tried then writing to a file a 1 bit whenever there is a high freq note and a 0 bit whenever there is a low freq one. *(The frequencies are high: 0.984375 and low: -0.0078125)*. The resultant file was useless. We then tried to invert the bits, a 0 for the high freq and a 1 for the low freq. The resultant file was rubbish. Next we took into account the length of the high freq souns *(note how the lower ones are always the same legnth)*. We then tried the same thing but now counting the actual frames and applying modulus 739 `% 739` so whenever the high freq note is longer than 739 it sould write 2 or more bits. We tried with 1 as high and 0 as low and viceversa, both resultant files were useless. 

Then we want back to researching and found a [post](https://leonjza.github.io/blog/2016/10/02/reverse-engineering-static-key-remotes-with-gnuradio-and-rfcat/) that explains how to reverse engineer some SDR (Software Defined Radio) captures and, luckily enough, the author [Leonjza](https://twitter.com/leonjza) used a Yardstick One transceiver to capture the data just like the description of this challenge. 

Reading the writeup we understood that only high freq notes must be taken into account and their representation, as stated by the post, is the following one:

![](/images/CTF/h-c0n/2020/radio1_3.png)

We then measured again high values and understood that the **short high freq notes are 739 frames long** and the **long high freq are three times as long, 2217 frames**. With this information in mind, we implemented an algorithm that counts the number of consecutive high freq (0.984375) frames/bits and writes to a file a 0 bit whenever there are 2217 consective frames (long) and a 1 bit whenever there are 739 consecutive frames (short), according to the image and the post. The resultant file was, once again, useless. We then **<gold>inverted the bits</gold>**, a 0 bit for the short high freqs and a 1 bit for the long high freqs. The resultant file was, surprisingly, useful!

In the following image you can see the bits output after analyzing the recording. 

![](/images/CTF/h-c0n/2020/radio1_4.png)

We wrote it to a file called `bogus_file` with Python's `BitVector` and printed the contents of the file:

![](/images/CTF/h-c0n/2020/radio1_5.png)
![](/images/CTF/h-c0n/2020/radio1_6.png)

The flag is:  
`H-c0n{2326cf36b8473d611d449f117d09399f}`

This is the Python script we used to analyze the .wav file and get the flag.

```python
#!/usr/bin/python3
#RazviOverflow

import wavefile
import sys
import BitVector

def wav_to_binary(filename = 'file1.wav'):
    w = wavefile.load(filename)
    print("PRINTED: ", w, "LENGTH: ", len(w[1][0]), "\n", "FIRST:", w[1][0][0], "SECOND:", w[1][0][1])
    count = 0
    bits_list = []
    for index in range(len(w[1][0])):
    	if(index == len(w[1][0])-1):
    		break

    	# Higher than zero means a high freq frame 
    	# (lower freq frames are negative, barely but sill)
    	if(w[1][0][index] > 0): 
    		count += 1
	    	if(w[1][0][index] != w[1][0][index+1]):
	    		if(count > 739): # LONG = 1
	    			bits_list.append("1")
	    		else: # SHORT = 0
	    			bits_list.append("0")
	    		count = 0

    print("String length:", len(string),"\nContents:", string)
    bv = BitVector.BitVector(bitstring = string)
    FILEOUT = open("bogus_file", "wb")
    bv.write_to_file(FILEOUT)
    FILEOUT.close()

    return w[1][0]

signal = wav_to_binary(sys.argv[1])
print("read "+str(len(signal))+" frames")
print("in the range "+str(min(signal))+" to "+str(min(signal)))
```

### Please keep in mind:

At the time we found Leonjza's post that helped us solve the challenge there was a important typo. The bit values he posted are inverted, that is, **SHORT is 0** and **LONG is 1**.

After solving the challenge with our own script, we found that Leonjza developed a tool for this task and he mentioned it at the end of his post. The tool is called [oktools](https://github.com/leonjza/ooktools) and can automatically analyze the .wav file and give the same output that we managed to get, but it does automatically and fully transparent to the user. We did it the hard way but we leanrt quite a few things! 

![](/images/CTF/h-c0n/2020/radio1_7.png)

## Samurai (Stego)
> "The general who is skilled in defense hides in the most secret recesses of the earth"
Sun Tzu's Art of War

In this callenge we're given a image called `samurai.png`:  
![](/images/CTF/h-c0n/2020/samurai_1.png)

After analyzing the .png file with `binwalk` or `foremost` we found that it has a .zip file hidden within it. After extracting the zip file *(called 27552.zip)* and decompressing it, there was a .wav file called wind.wav. We opened the file but this time with [Sonic Visualizer](https://www.sonicvisualiser.org/). When playing the .wav file it looks just like repetitive noise but lightly different toward the middle. That's how it looks in Sonic Visualizer:

![](/images/CTF/h-c0n/2020/samurai_2.png)

Inspecting the frequenc spectogram (Pane -> Add peak frequency spectrogram) gives us the h-c0n logo and the word `SHINOBI`.

![](/images/CTF/h-c0n/2020/samurai_3.png)

You can also inspect the spectogram with Audacity but the results are not as clear as with Sonic Visualizer.

After obtaining the word SHINOBI we tried several things in order to continue toward the flag. Using `exiftool` we are able to read the metadata of a given file. There's the output of samurai.png:  

![](/images/CTF/h-c0n/2020/samurai_4.png)

Nothing strange except the author's name. At first we thought it was a troll random string but googling it turns out it's an actual person and has his/her own git repo! In the repo there are several tools and one of them is called [stegpy](https://github.com/dhsdshdhk/stegpy) and is used to encode or retrieve information from images and audio files through steganography. 

We installed it and using `SHINOBI` as password we managed to get the flag:

![](/images/CTF/h-c0n/2020/samurai_5.png)

```
H-c0n{3899dcbab79f92af727c2190bbd8abc5}
```

## User Flag and Machine Flag (Boot2Root)

Unfortunately I cannot give full details about this challene (getting the user flag and root flag) because the computers to compromise were shut down once the qualifier ended. Anyways, I'll write down details about what we did.

We were a link to a page with [CMSMS](https://www.cmsmadesimple.org/) ver 2.2.5 installed. After researching a bit we found out that CMSMS prior to version 2.2.10 has a SQL Injection vulnerability that allows to obtain admin credentials. We used [this script](https://packetstormsecurity.com/files/152356/CMS-Made-Simple-SQL-Injection.html) from Packet Storm Security in order to obtain the credentials. The script can get the hash of the password but if you want to actually crack it you must provide a wordlist. We used the famous and all powrful [Rockyou](https://www.kaggle.com/wjburns/common-password-list-rockyoutxt). After executing the script and providing rockyou as wordlist we are given the admin credentials.

![](/images/CTF/h-c0n/2020/boot2root_1.png)

We can nos access the content manager CMSMS with user: `admin` and password: `lalala`. Once inside the content manager there are a lot of options and actions the admin can do. After playing around a bit we found out the one that we are looking for is the content manager. 

![](/images/CTF/h-c0n/2020/boot2root_2.png)

In the content file manager the admin can inspect, edit, upload, copy, rename, etc... files uploaded to the server.

![](/images/CTF/h-c0n/2020/boot2root_3.png)

After several tests we found that renaming existing files is not possible but it is possible to copy alrady existing files and give the copy a specific name. Furthermore, inspecting the alrady existing files we noticed that `cmsmsrce.txt` *(that could stand for CMSMS Remote Code Execution)* contains a php script that simply reads the `cmd` parameter of the url.

![](/images/CTF/h-c0n/2020/boot2root_4.png)

We decided then to copy the file using the content file manager and rename the copy as `script.php`. We can now use this URL to execute remote bash commmands on the server that's hosting CMSMS in the form os `url.com/script.php?cmd=bash_command`. Using this ineffective form of bash terminal, we were able to discover the directories and its contents. 

![](/images/CTF/h-c0n/2020/boot2root_5.png)

The directory `/home/prequal/backups` caught our attention since it contained a public and a private RSA keys. We copied the keys to /var/html/www so we could see them in CMSMS content file manager. We then copied the contents of the private key file to our local systems and tried to ssh to the remote computer with it. We assume the user shares the name with the directory: `prequal`

![](/images/CTF/h-c0n/2020/boot2root_6.png)

Unfortunately to establish the connection a passphrase or password is required. In order to crack it we used John The Ripper. First we convert the RSA private key to a format understandable by John. In order to do so, `ssh2john.py` must be used.

```
python /usr/share/john/ssh2john.py id_rsa > id_rsa_hash
```

Then we bruteforced the passphrase with the same `rockyou` dictionary used before. 

```
john --wordlist="/usr/share/wordlists/rockyou.txt" id_rsa_hash
```

![](/images/CTF/h-c0n/2020/boot2root_7.png)

The password is `12345678`. We can successfully connect to the server.

![](/images/CTF/h-c0n/2020/boot2root_8.png)

The user flag is:
```
H-c0n{3ab7568bdae26ac11f6b9e14cad546f9}
```

Now, in order to obtain root flag we looked the entire system (wherever the user prequal had permission) for files with read or write privileges for the user prequal. We used tools like `linenum`, `linuxprivchecker` or `linux smart enumeration` but got no interesting info. However, we discovered that the directory `/var/backups` contained a shadow.bak.1 file that had indeed read permissions for the user prequal.

![](/images/CTF/h-c0n/2020/boot2root_9.png)
![](/images/CTF/h-c0n/2020/boot2root_10.png)

That's very useful information and a hash of the root user password that we can try to crack, once again bruteforcing. In order to crack the root hash from the shadow backup we used [Hashcat](https://hashcat.net/hashcat/). After trying rockyou dictionary (quite a few minutes) we had no candidate for the password. We tried another very well known dictonary, `credentials` from [Sec Lists](https://github.com/danielmiessler/SecLists/tree/master/Passwords/Common-Credentials) *(the top 1 million credentials)*

Using Hashcat we were able to crack the password in 26 minutes (using a kali VM). You can find a tutorial on how to crack hashes with Hashcat [here](https://samsclass.info/123/proj10/p12-hashcat.htm) and [here](https://null-byte.wonderhowto.com/how-to/crack-shadow-hashes-after-getting-root-linux-system-0186386/).
```
hashcat -m 1800 -a 0 -o cracked hash ~/Downloads/10-million-password-list-top-1000000.txt -O --force
```

![](/images/CTF/h-c0n/2020/boot2root_11.png)

The password for the user root is `lp0520`. We can now `substitute user (su)` root and try the password out. 

![](/images/CTF/h-c0n/2020/boot2root_12.png)

It works. We can then inspect the /root directory and read the flag. The root flag is:
```
H-c0n{5a9136f587379fbf8bb8eab0d89080e0}
```

## Modulated secret (Radio)
> A radio amateur has approached us, very worried, saying that he has been able to capture a broadcast in which a secret was being shared. He had to leave because he had a jumping competition, so he sent us the capture of the broadcast. Can you help us recover the secret?  
DOWNLOAD: https://drive.google.com/open?id=1evWfrTqZ4U1rY47dLcwz9kRnhybq1o6A  
NOTE: This challenge has a case insensitive flag.

In this challenge we are given a huge file called `damn` that looks like some kind of raw data since it has no metadata. Tools like `file`, `binwalk` or `exiftool` gave no useful output. 

We tried opening it with Sonic Visualizer and we couldn't import the file. We tried Audacity and, even though it opens the file, looking at the time graph or the spectogram was useless. Finally, we tried to read it with [gqrx-sdr](http://gqrx.dk/). Gqrx's GUI is not very intuitive (in my opinion) but we could open the file. 

![](/images/CTF/h-c0n/2020/radio2_1.png)

After opening the file, we played around with the parameters and modulated the frequency (AM) until something understandable was playing. 

![](/images/CTF/h-c0n/2020/radio2_2.png)

The flag was voice-dictated and it was split among 3 different frecuencies. Hearing each chunk of the flag with the proper frequency allowed us to compose the flag.

The flag is:
```
h-c0n{4ed54c18599748c654f614806a645832}
```

