---
title: "Microcorruption - Montevideo"
date: 2019-02-18
categories: [microcorruption, reverse engineering]
tags: [microcorruption, tutorial, assembly, ctf, montevideo, walkthrough, debug]
description: Microcorruption Montevideo level explained in detail. We will see how to solve the level and understand the underlying concepts. 
hasComments: true
image: /images/microcorruption-levels-image.png
---

When you enter the level, as always, there is a pop up manual. The last paragraph states the following:
> This is Software Revision 03. We have received unconfirmed reports
    of issues with the previous series of locks. We have reimplemented
    much  of the  code according  to our  internal Secure  Development
    Process

Turns out they "reimplemented much of the code" following their *<red>Secure Development Process</red>*. Well, let us find out how reliable that process is and, of course, how can we break it. 

Inspecting `main` function you'll notice it simply calls `<login>` function, allocated at `0x44f4`. *<gold>(Please remember your addresses may be different)</gold>*

Allrighty then, let's see what `login` actually does.
```
44f4 <login>
44f4:  3150 f0ff      add	#0xfff0, sp
44f8:  3f40 7044      mov	#0x4470 "Enter the password to continue.", r15
44fc:  b012 b045      call	#0x45b0 <puts>
4500:  3f40 9044      mov	#0x4490 "Remember: passwords are between 8 and 16 characters.", r15
4504:  b012 b045      call	#0x45b0 <puts>
4508:  3e40 3000      mov	#0x30, r14
450c:  3f40 0024      mov	#0x2400, r15
4510:  b012 a045      call	#0x45a0 <getsn>
4514:  3e40 0024      mov	#0x2400, r14
4518:  0f41           mov	sp, r15
451a:  b012 dc45      call	#0x45dc <strcpy>
451e:  3d40 6400      mov	#0x64, r13
4522:  0e43           clr	r14
4524:  3f40 0024      mov	#0x2400, r15
4528:  b012 f045      call	#0x45f0 <memset>
452c:  0f41           mov	sp, r15
452e:  b012 4644      call	#0x4446 <conditional_unlock_door>
4532:  0f93           tst	r15
4534:  0324           jz	#0x453c <login+0x48>
4536:  3f40 c544      mov	#0x44c5 "Access granted.", r15
453a:  023c           jmp	#0x4540 <login+0x4c>
453c:  3f40 d544      mov	#0x44d5 "That password is not correct.", r15
4540:  b012 b045      call	#0x45b0 <puts>
4544:  3150 1000      add	#0x10, sp
4548:  3041           ret
```

At a first glance there are some functions that catch my eye: 
- At address `0x4510` there is `getsn` which receives `0x30` (via `r14`) and `0x2400` (via `r15`) as parameters. 
- At address `0x451a` there is `strcyp` which receives `0x2400` (via `r14`) and `sp`'s *<orange>(Stack Pointer)</orange>* value at that particular moment (via `r15`) as parameters.
- At address `0x4528` there is `memset` which receives `NULL byte` (via `clr r14`) and `0x2400` (via `r15`) as parameters.
- Finally, at address `0x452e` there is `conditional_unlock_door`. 

Based on this information, what we can deduce so far is:
1. Our buffer is 48 (0x30) bytes long.
2. Our buffer first gets stored at address `0x2400`.
3. It then gets copied to whatever `sp` *<orange>(Stack Pointer)</orange>* value is at that particular point of execution.
4. The original copy at `0x2400` gets zeroed by `memset`.

Let's confirm that behavior and correct our assumptions. I suggest placing breakpoints right after each important function. 

<p align="center">
<img src="/images/microcorruption-montevideo0.png">
</p>

Before executing the program, I also suggest you to track `r15` is order to see it's value into Live Memory Dump window. In order to track a register you must simply execute `track rN` command, where N is the register number. In this particular case it'd be `track r15`.

When we're asked to input data, as always, we'll provide some easily recognizable bytes. In my case, I provided 50 bytes. You can copy your input from here:

ASCII: 
```
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```
HEX: 
```
4141414141414141414142424242424242424242434343434343434343434444444444444444444445454545454545454545
```

<p align="center">
<img src="/images/microcorruption-montevideo1.png">
</p>

Our first assumptions were right since there are only 48 bytes (you can count how many Es are there and you'll count up to 8) at address `0x2400`.

<p align="center">
<img src="/images/microcorruption-montevideo2.png">
</p>

Right when `strcpy` finishes, we can inspect `r15`'s value.

<p align="center">
<img src="/images/microcorruption-montevideo3.png">
<img src="/images/microcorruption-montevideo4.png">
</p>

And we can, in fact, inspect the memory via Live Memory Dump window and see that our buffer got indeed copied at address `0x43ee`.

<p align="center">
<img src="/images/microcorruption-montevideo5.png">
</p>

Then address `0x2400` gets zeroed and if you continue the execution you'll get "That password is not correct" and the program will either finish expectedly or crash.

Interesting, what ought we do now? Well, let's keep breakpointing the code and acquire more knowledge about what it does. Interestingly enough, last two instructions of `login` function are:
```
4544:  3150 1000      add	#0x10, sp
4548:  3041           ret
```
Let's breakpoint on both of them and see what happens at execution time. 

<p align="center">
<img src="/images/microcorruption-montevideo6.png">
</p>

Once again, I recommend you to provide a full-length input. That is, 48 or more bytes.
<p align="center">
<img src="/images/microcorruption-montevideo7.png">
<img src="/images/microcorruption-montevideo8.png">
</p>

You will notice `sp`'s value right before adding `0x10` is `0x43ee`. Isn't `0x43ee` familiar? Well, it indeed is. `0x43ee` is where our input gets stored after `strcpy` does it job. This means `sp` will point to `0x43fe` when `ret` instruction is about to get executed, right when `login` is about to finish. And that means **we can control return address of `login` function** because the buffer is 48 (0x30) bytes long starting at address `0x43ee`. That's nice!

<p align="center">
<img src="/images/microcorruption-montevideo9.png">
<img src="/images/microcorruption-montevideo10.png">
</p>

As we've seen in previous levels, this allows us to jump wherever we want when `login` function ends. But, **<gold>Where do we actually want to jump?</gold>**. Just like the last level, [Whitehorse](/microcorruption/whitehorse), we will have to write our own **<red>Shellcode</red>** but this time with some limitations. Let's move to solution section and learn how we can actually achieve a working input :)

### Solution

The first thing to have in mind is the function we're exploiting, the vulnerable function. In this case, it is `strcpy`. `strcpy` defines our exploiting context and it has, of course, some limitations. Let's read some official documentation about [strcpy()](http://www.cplusplus.com/reference/cstring/strcpy/):

> Copies the C string pointed by source into the array pointed by destination, including the terminating null character **<red>(and stopping at that point)</red>**

Those very last words are very important to us because they basically tell us **how to NOT** write our shellcode. That is, `0x00` is a badchar in this context since `strcpy` will stop copying from there on. A badchar, or badchar, is a character, or set of characters, that, given a vulnerable function, a context, renders the shellcode useless. You can read more about badchars all over the Internet. [This one](https://www.ihacklabs.com/en/poc-badchar-alternative-method/) and [this one](https://bulbsecurity.com/finding-bad-characters-with-immunity-debugger-and-mona-py/) are mere examples.

Now, keeping in mind badchars, let's design our shellcode. **<yellow>There are many solutions for this level</yellow>** and many variations of every solution, your imagination is the only limit. 

One solution that I implemented is very simple. We design such a payload whose length is lesser than 16 bytes (0x10) and then we jump to it. That is, we overwrite `login` return address with `0x43ee` address. Now, **<blue>what shall our shellcode do?</blue>** We can take advantage of code that already exists in the program's memory. 

As we've seen in previous levels, [LockitAll User Manual](https://microcorruption.com/manual.pdf) tells us how to insta-unlock the door. That is, pushing **0x7F** into the stack and calling **INT**. `INT` function is at address `0x454c`.

```
454c <INT>
454c:  1e41 0200      mov	0x2(sp), r14
4550:  0212           push	sr
4552:  0f4e           mov	r14, r15
4554:  8f10           swpb	r15
4556:  024f           mov	r15, sr
4558:  32d0 0080      bis	#0x8000, sr
455c:  b012 1000      call	#0x10
4560:  3241           pop	sr
4562:  3041           ret
```


## Recap



## More levels
* Click [here](/microcorruption/johannesburg) to see next level (Johannesburg).
* Click [here](/microcorruption/whitehorse) to see previous level (Whitehorse).
* Click [here](/microcorruption) to see levels index.