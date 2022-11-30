---
title: "Microcorruption - Sydney"
date: 2018-09-13
categories: [microcorruption, reverse engineering]
tags: [microcorruption, tutorial, assembly, ctf, sydney, walkthrough, debug, endianness, nuxi problem]
description: Microcorruption Sydney level explained in detail. We will see how to solve the level and understand the underlying concepts. 
hasComments: true
image: /images/microcorruption-levels-image.png
---
After solving the previous level called New Orleans, explained in detail [here](/microcorruption/new-orleans), our next objective in the list, and in the map, is called Sydney. 

In the manual that appears at the beginning, in the last paragraph, you can read the following statement:
>   This is  Software Revision 02.  We have received reports  that the
    prior  version of  the  lock was  bypassable  without knowing  the
    password. We have fixed this and removed the password from memory.

So, apparently, there will be no more hardcoded password. Let's find out!

```
4438 <main>
4438:  3150 9cff      add	#0xff9c, sp
443c:  3f40 b444      mov	#0x44b4 "Enter the password to continue.", r15
4440:  b012 6645      call	#0x4566 <puts>
4444:  0f41           mov	sp, r15
4446:  b012 8044      call	#0x4480 <get_password>
444a:  0f41           mov	sp, r15
444c:  b012 8a44      call	#0x448a <check_password>
4450:  0f93           tst	r15
4452:  0520           jnz	#0x445e <main+0x26>
4454:  3f40 d444      mov	#0x44d4 "Invalid password; try again.", r15
4458:  b012 6645      call	#0x4566 <puts>
445c:  093c           jmp	#0x4470 <main+0x38>
445e:  3f40 f144      mov	#0x44f1 "Access Granted!", r15
4462:  b012 6645      call	#0x4566 <puts>
4466:  3012 7f00      push	#0x7f
446a:  b012 0245      call	#0x4502 <INT>
446e:  2153           incd	sp
4470:  0f43           clr	r15
4472:  3150 6400      add	#0x64, sp
```

Inspecting `main` we can see there is no silly `create_password` as before. We still have `check_password` at instruction `0x444c` and afterwards a test on `r15` that determines whether the password is correct. Once again, we must insert such an input so that `r15` at instruction `0x4450` has whatever value but zero. Let's check what `check_password` is all about.

```
448a <check_password>
448a:  bf90 782e 0000 cmp	#0x2e78, 0x0(r15)
4490:  0d20           jnz	$+0x1c
4492:  bf90 3d67 0200 cmp	#0x673d, 0x2(r15)
4498:  0920           jnz	$+0x14
449a:  bf90 3d33 0400 cmp	#0x333d, 0x4(r15)
44a0:  0520           jne	#0x44ac <check_password+0x22>
44a2:  1e43           mov	#0x1, r14
44a4:  bf90 635e 0600 cmp	#0x5e63, 0x6(r15)
44aa:  0124           jeq	#0x44ae <check_password+0x24>
44ac:  0e43           clr	r14
44ae:  0f4e           mov	r14, r15
44b0:  3041           ret
```

There are 4 `cmp` comparing some argument against some contents of memory addresses relatives to `r15`. Remember at this point `r15` points at the address, its value is a memory address, where our input is stored because in the `main` function, right before calling `check_password`, there is a `mov sp, r15` at `0x444a`.

You may notice after the comparisons there is always a jump instruction. The first two of them take as argument an <red>expression</red> rather than an address. The expression, when evaluated, will result into a memory address. The expression is a <green>sum</green> where one of the operands is '<blue>$</blue>'. In the context of MSP430 assembly language, '<blue>$</blue>' means *<gold>the current position</gold>*. That is, '<blue>$</blue>' retrieves the address where <gold>PC</gold> *(Program Counter)*, also known as <gold>IP</gold> *(Instruction Pointer)*, points right now. When the CPU is about to execute the instruction at address `0x4490`, PC has that exact value. When solving the expression `$+0x1c`, '<blue>$</blue>' will be replaced by PC's value at that very moment so `$+0x1c` will become `0x4490+0x1c`. The instruction will then be `jnz #0x44ac` *(because 0x4490+0x1c = 0x44ac)*. The jump after the next comparison at `0x4498` will jump to the same address. At that address, `0x44ac`, there is `clr r14` and afterwards the function finishes. Remember `clr r14` is equivalent to `mov #0, r14` and that's exactly what we do not want. You can read more bout <blue>$</blue> [here](https://stackoverflow.com/a/20411716).

Instruction at address `0x448a` is `cmp #0x2e78, 0x0(r15)`. Unlike the last level, this time there is no <red>.b</red> suffix to `cmp` instruction. Remember that <purple>.w suffix or no suffix</purple> means <orange>word</orange>. *(In the context of MSP430 microcontroller family)*

<p align="center">
<img src="/images/microcorruption-new-orleans-instruction-overview.png">
</p>

When we talk about "<orange>word</orange>" in the context of computing, we are talking about the <orange>word</orange> unit of information which is equivalent to 16 bits. In case you are unfamiliar with this very matter, you can read more [here](https://en.wikipedia.org/wiki/Units_of_information). Please note that you must make sure you clearly understand it since <yellow>this topic is one of the main foundations which computing is build upon</yellow>. Just to mention some, we have bits. 4 bits are sometimes called nibble or half a byte. 8 bits form a byte. 2 bytes form a word. 2 words form a double word. 2 doublewords form a quadword and so on.

<p align="center">
<img src="/images/data-representations.jpg">
</p>

Back to the code, instruction at `0x448a` is comparing two bytes. `0x2e78` with values at `r15` and `r15+1`. The "+1" is implicit to the `cmp` instruction because that's exactly what working with <orange>words</orange> means, taking two bytes at a time. If values at `r15` and `r15+1` are `0x2e78`, when perfomring the comparison the result will be 0, the ZF will be set and `jnz` won't be taken. 

At address `0x4492` we have `cmp #0x673d, 0x2(r15)`. Just like before, it is checking if values at memory `r15+2` and `r15+3` are equal to `0x673d`.

The same rule applies to comparisons at `0x449a` and `0x44a4`. 

What `check_password` does is checking if there is indeed:
- `0x2e78` from `r15` to `r15+1`
- `0x673d` from `r15+2` to `r15+3`
- `0x333d` from `r15+4` to `r15+5`
- `0x5e63` from `r15+6` to `r15+7`

That's exactly 8 bytes long password. Since we already know that our input is stored at `r15` and that same `r15` is later used in `check_password`, it is logic to think that providing those exact bytes as inpute we can solve the level. So let's do it. You can input hex encoded 

<p align="center">
<img src="/images/microcorruption-sydney-first-try.png">
</p>

<p align="center">
<img src="/images/microcorruption-sydney-first-try-failure.png">
</p>

Well, unexpected. What happened? Let's breakpoint it at `0x444c` in `main`, right where `check_password` is called, in order to inspect memory content.

<p align="center">
<img src="/images/microcorruption-sydney-bp0.png">
</p>

If you want to easily find where `r15` is pointing, you can write `track r15` and its marker will appear in Live Memory Dump box. 

<p align="center">
<img src="/images/microcorruption-sydney-bp1.png">
</p>

Everything looks allright. What could be happening? Lets debug it step by step using `s` command. Type `s` to jump to next instruction, inside `check_password` function. Inspecting memory with `read` or `r` commands also shows that apparently everything is right. Well, not everything is right.

We must take into account <yellow>another main topic in computer architecture</yellow>. We're talking about how data is represented into memory, also known as **<red>endianness</red>**.

There are tons of articles, papers, videos, etc.. addressing endianness. To summarize it, I will quote [wikipedia's article](https://en.wikipedia.org/wiki/Endianness) about endianness. There are several ways in which bytes can be arranged into memory. There is little-endian, big-endian *(also known as netowrk-endian)*, middle-endian, etc... with the first 2 being the most common. 
- In **<yellow><u>big-endian</u></yellow>** the most significant byte, the byte containing the most significant bit *(the leftmost byte)*, is stored first, at the lowest address. The least significant byte, then, has the higher address.
- In **<yellow><u>little-endian</u></yellow>** the least significant byte, *(the rightmost byte)* is stored first, at the lowest address. The most significant byte, then, has the higher address. 

As an example, let's use the char sequence "RAZVI OVERFLOW". Suppose each char is 1 byte and we are starting at address 0x00. Here is how a little-endian and big-endian architecture would store the data in memory. **<red>WARNING!</red>** This is just an example to understand the concept. Endianness is applied only to multi-byte numbers like words, doublewords and quadwords. In most cases, strings are UTF-8, which uses a single byte to represent each char and thus it is not affected by endianness (because you can not reorder bytes in a single byte value). You can read more about Strings and endianness here:

* https://cs.stackexchange.com/questions/103168/why-does-little-endian-apply-to-numbers-and-not-to-text-strings
* https://stackoverflow.com/questions/1568057/ascii-strings-and-endianness

<p align="center">
<img src="/images/endianness.png">
</p>

Different endianness representations problems are sometimes rrefered to as *the nuxi problem*. [Here](https://betterexplained.com/articles/understanding-big-and-little-endian-byte-order/) is a very good read about endianness and the nuxi problem. 

### Solution

Since MSP430 is **little endian**, as stated [here](https://en.wikipedia.org/wiki/TI_MSP430#MSP430_CPU), and it has 16-bit addressing, we must convert to little-endian each pair of byte. If it'd have been a 32-bit processor, we'd have to convert each 4 bytes and so on...

So, instead of inserting `2e78 673d 333d 5e63` we must input `782e 3d67 3d33 635e` *(without spaces)* in order for the little-endian machine to read and interpet the data as we expect to.

<p align="center">
<img src="/images/microcorruption-sydney-second-try.png">
</p>

And we're successfull :)

<p align="center">
<img src="/images/microcorruption-sydney-solved.png">
</p>

### Recap

In this level we've seen the use of <blue>$</blue> in expressions to specify relative addresses as argument to `jmp` instruction, we've seen several data representations such as bit, nibble, byte, word... and the very important concept called endianness.

## More levels
* Click [here](/microcorruption/hanoi) to see next level (Hanoi).
* Click [here](/microcorruption/new-orleans) to see previous level (New Orleans).
* Click [here](/microcorruption) to see levels index. 