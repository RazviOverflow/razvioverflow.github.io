---
title: "247CTF - Hidden Flag Function"
date: 2021-02-22
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
- Format string vulnerability, by Syracuse University. [Link](http://www.cis.syr.edu/~wedu/Teaching/cis643/LectureNotes_New/Format_String.pdf)

You can also learn about format string in video format, [LiveOverflow](https://www.youtube.com/results?search_query=liveoverflow+format+string)'s videos on the topic are very recommended.





In order to abuse the vulnerability and leak memory contents, we can make use of the positional specifier and the string format specifier. As it was aforementioned, if the address dereferenced by the `%s` format specifier is an invalid address, the program will crash (*netcat connection will close*). 

Since we don't control what addresses are placed in the stack and neither can we debug it, my approach was to simply leak each and every address from the stack. That is, iterate and step through every position following the next pattern: `%{index}$s` where `index = 1`. In the next execution, `index = index + 1` and so forth. This pattern translated to a format specified is as simple as `$1$x`.

```python

```

Executing the exploit that abuses the vulnerability and leaks the memory, we will eventually leak the corresponding environment variable.

<p align="center">
	<img src="/images/247ctf/pwnable/confused_environment_read/exploited.png">
</p>

I hope you enjoyed my write-up. I'd be delighted to know whether it helped you progress and learn new things. Do not hesitate to reach me out via [Twitter](https://twitter.com/Razvieu)! I'm always eager to learn new things and help others out :)

## More challenges
* Click [here](/247ctf) to see 247CTF index.