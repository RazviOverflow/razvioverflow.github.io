---
title: "247CTF - Hidden Flag Function"
date: 2021-02-15
categories: [247ctf, ctf]
image: /images/247ctf/logo_0.png
tags: [247ctf, assembly, ctf, tutorial, walkthrough, debug, reverse engineering, exploiting, pwn, binary exploitation, confused environment read, format string]
description: 247CTF Confused Environment Read (PWN) challenge explained in detail. We will see how to solve the challenge and understand the underlying concepts.
hasComments: true
---

![247ctf0](/images/247ctf/pwnable/confused_environment_read/description.png)

This binary exploitation challenge is, at the moment of writing this write-up, rated as *EASY* with a difficulty score of 2.22 out of 5.0. Its description states the following:

> Can you abuse our confused environment service to read flag data hidden in an environment variable?

There is no binary to download an reverse this time. Instead we are given a URL and a port to connect to. In order to connect, I'll be using [netcat](https://en.wikipedia.org/wiki/Netcat) along with [rlwrap](https://github.com/hanslub42/rlwrap). In case you are wondering what rlwrap does, it basically wraps the readline commands and allows a user to use key arrows with commands line netcat, avoiding the annoying and infamous `^[[D^[[A` and such. 

Connecting to the challenge is as easy as `rlwarp nc URL PORT`

<p align="center">
	<img src="/images/247ctf/pwnable/confused_environment_read/execution.png">
</p>

Given that we can only interact with the execution of the binary and we have no idea what the source code is, the natural step to follow is to try several inputs and see if it breaks, looking for possible vulnerabilities. As shown in the image above, the binary is vulnerable to [**FORMAT STRING**](https://en.wikipedia.org/wiki/Printf_format_string). There are several <yellow>very good</yellow> technical papers or articles about the format string vulnerability, I'll link some:

- Format string vulns in gory detail, by Ron Bowes. [Link](https://blog.skullsecurity.org/2015/defcon-quals-babyecho-format-string-vulns-in-gory-detail)
- Exploiting Format String vulnerabilities, by scut from Team Teso. [Link](https://cs155.stanford.edu/papers/formatstring-1.2.pdf)
- Format string exploitation tutorial, by Saif El-Sherei. [Link](https://www.exploit-db.com/docs/english/28476-linux-format-string-exploitation.pdf)
- Format string attack, by OWASP. [Link](https://owasp.org/www-community/attacks/Format_string_attack)
- Format string exploitation, by Fuzzysecurity. [Link](https://www.fuzzysecurity.com/tutorials/expDev/10.html)



## More challenges
* Click [here](/247ctf) to see 247CTF index.