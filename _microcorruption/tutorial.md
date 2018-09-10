---
title: "Microcorruption - Tutorial"
date: 2018-09-09
categories: [microcorruption, reverse engineering]
tags: [microcorruption, tutorial, assembly, ctf, tutorial, walkthrough, debug]
description: Microcorruption tutorial level explained in detail.
hasComments: true
---
## Introduction
![microcorruption](/images/microcorruption-tutorial.png)

Since [microcorruption](https://microcorruption.com) is an embedded debugger, the tutorial level is probably one of the most important since it introduces all the commands that will later be needed as well as the general structure of the debugger itself. You can always input `help` in order to see debugger usage. Here is what `help` prints out:
```
Valid commands:
  Help - show this message
  Solve - solve the level on the real lock
  Reset - reset the state of the debugger
  (C)ontinue - run until next breakpoint
  (S)tep [count] - step [count] instructions
  step Over / (N)ext - step until out or pc is next instruction
  step Out / (F)inish - step until the function returns
  (B)reak [expr] - set a breakpoint at address
  (U)nbreak [expr] - remove a breakpoint
  (R)ead [expr] [c] - read [c] bytes starting at [expr]
  track [reg] - track the given register in memory
  untrack [reg] - removes the tracking of the given register
  (L)et [reg]/[addr] = [expr] - write to register or memory
  Breakpoints - show a list of breakpoints
  Insncount - count number of CPU cycles executed
  Manual - show the manual for this page

Scripting commands:
  #define name [commands] - alias "name" to run [commands].
  command;command - run first command, then second comamnd.

List of types:
  [reg] := 'r' followed by a number 0-15
  [addr] := base-16 integer or label name (e.g., 'main')
  [expr] := [reg] or [addr] or
            [expr]+[expr] or [expr]-[expr]
```
Please bear in mind that you will probably also need to check the [Lockitall LockIT Pro User Guide](https://microcorruption.com/manual.pdf) also known as <u>the manual</u>, as well as the [Assemlber or Disassembler](https://microcorruption.com/assembler). 

With all that in mind, let's go on and solve the very first level.
## Solving tutorial level

Starting with the level itself, you will notice from now on that reading and understanding assembly in a fluent fashion is very important. It is just a matter of practice. Here, in Microcorruption, we are working with a [16-bit architecture](https://en.wikipedia.org/wiki/16-bit#16-bit_architecture) and we will see its distinctive features, peculiarities. 

When you start reading the instructions, the code that will be executed, you may fight yourself somehow lost if you are not used to assembly language. Do not worry, I will guide you throughout all these posts. 

The first concept to elucidate is the MSP430 instruction set structure. They follow the pattern **<red>operation</red> <yellow>source</yellow>, <purple>destination</purple>**. For example, `mov #0x5, r15` is moving the hexadecimal number 0x5 into register `r15`. This differs from Intel's operation destination, source.

As always, there is a <blue>main</blue> function that marks our starting point. *Well, in fact there are other functions executed before main as __init_stack, __low_level_init and __do_copy_data but that's none of our concern as of right now.* 

Our main looks like this:

```
4438 <main>
4438:  3150 9cff      add	#0xff9c, sp
443c:  3f40 a844      mov	#0x44a8 "Enter the password to continue", r15
4440:  b012 5845      call	#0x4558 <puts>
4444:  0f41           mov	sp, r15
4446:  b012 7a44      call	#0x447a <get_password>
444a:  0f41           mov	sp, r15
444c:  b012 8444      call	#0x4484 <check_password>
4450:  0f93           tst	r15
4452:  0520           jnz	#0x445e <main+0x26>
4454:  3f40 c744      mov	#0x44c7 "Invalid password; try again.", r15
4458:  b012 5845      call	#0x4558 <puts>
445c:  063c           jmp	#0x446a <main+0x32>
445e:  3f40 e444      mov	#0x44e4 "Access Granted!", r15
4462:  b012 5845      call	#0x4558 <puts>
4466:  b012 9c44      call	#0x449c <unlock_door>
446a:  0f43           clr	r15
446c:  3150 6400      add	#0x64, sp
```
As you can see, instruction at address `0x4446` calls `get_password` and instruction at `0x444c` calls `check_password`. Right above each of them, there is `mov sp, r15` basically telling us `get_password` is storing it at `r15` and `check_password` is checking it from `r15`.

`sp` stands for <gold>Stack Pointer</gold>. Depending on the architecture it's implementation may differ but in MSP430's case it's the register whose value is always the address of the element on current stack frame top. Again, depending on the acrhitecture, it is called `sp`, `esp` for <gold>Extended Stack Pointer</gold>, `rip` on 64-bit machines, etc... Read more about MSP430 stack pointer [here](http://www.ti.com/sc/data/msp/databook/chp9.pdf) *(chapter 9.1.2.1)* and about general stack pointer [here](https://en.wikipedia.org/wiki/Stack_register). Read more about MSP430 registers [here](http://mspgcc.sourceforge.net/manual/x82.html) and about CPU registers (x86 architecture) [here](https://en.wikibooks.org/wiki/X86_Assembly/X86_Architecture).

Right at the instruction at `0x4450`, there is `tst r15`. `tst` stands for *test* and it is used to widely used to check some value against 0 and as a more efficient alternative to `cmp #0, argument`. It operates bitwise AND with the argument(s) and set the registers, also called flags, accordingly without saving the result. In the case of MSP430 microcontroller, `tst r15` is basically **r15 AND r15**. Read more about `tst` [here](https://stackoverflow.com/a/44749414).

The following instruction is `jnz #0x445e <main+0x26>` at `0x4520`. `jnz` stands for *jump if not zero*. In this context, not zero refers to the result of the last computed operation. In order to check if it is zero or not, the instruction inspects the flag that was previously modified by `tst`, the Zero Flag (ZF). In human language the instruction means ***if Zero Flag is 0, jump to address `0x445e`, otherwise continue***. Please note that ZF is set to 1 only when the result is 0. Read more about conditional jumps and zero flag [here](https://stackoverflow.com/a/14267642).

At address `0x445e`, previous jump's destination, we find that the string "Access Granted!" is being moved into register `r15`, a call to `puts` is being made in order to print it and, finally, a call to `unlock_door` that, obviously, unlocks the door and completes the level. 

So, the conclusion so far is that in order to solve this level `r15` must be different to zero after `check_password` call. Let's inspect `check_password`.

```
4484 <check_password>
4484:  6e4f           mov.b	@r15, r14
4486:  1f53           inc	r15
4488:  1c53           inc	r12
448a:  0e93           tst	r14
448c:  fb23           jnz	#0x4484 <check_password+0x0>
448e:  3c90 0900      cmp	#0x9, r12
4492:  0224           jeq	#0x4498 <check_password+0x14>
4494:  0f43           clr	r15
4496:  3041           ret
4498:  1f43           mov	#0x1, r15
449a:  3041           ret
```

At address `0x4484` we have `mov.b	@r15, r14`. Let's split it and see what's happening. First of all, it is moving one byte. Please notice the instruction suffix `mov`**<red>.b</red>**. Read more about MSP430 instruction suffixes [here](https://www.ti.com/sc/docs/products/micro/msp430/userguid/as_5.pdf). The <yellow>source</yellow> is `r15` but since there is an <blue>at sign '@'</blue> in front of the register, it doesn't mean *the content of* `r15`. It actually means to take `r15`'s content, treat it as a memory address and retrieve what is at that specific address. The <purple>destination</purple> is `r14`. So, in human language it means ***take the byte at address stored in `r15` and save it in `r14`***. 

At addresses `0x4486`and `0x4488` some increments are taking place. `inc` takes one single argument and increments it by one saving the result in that very same argument. That is, `inc r15` equals to `r15 += 1`. 

Instruction `0x448a` is checking if `r14` is zero. *Remember `r14` is the byte at addres stored in `r15`*. If it is not zero, it jumps back to `0x4484`. At address `0x448e` we find a comparison between hexadecimal 9 and content of `r12`. What `cmp` instruction essentially does is <purple>destination</purple> - <yellow>source</yellow>. In this particlar case it means `r12 - 0x9`. The result is not stored and operands are not affected, only flags are set accordingly. Read how `cmp` works internally [here](http://www.ti.com/lit/ug/slau144j/slau144j.pdf) *(Page 71)*. 

Afterwards, at address `0x4492` we see a *jump if equal* `jeq` instruction. `jeq` checks the ZF (Zero Flag) and if it is set, that is, if it is 1, it jumps to `0x4498`. Remember last `cmp` instruction because it is the one who sets ZF. At `0x4498`, jump's destination, we have `mov #0x1, r15`, which is moving hexadecimal 1 into `r15`, and afterwards `ret`. If `r12` is not equal to 0x9, it clears r15. `clr r15` is equivalent to `mov #0x0, r15`. 

### Solution

After analyzing the code, let us recapitulate and see what the solution shall be. The function that unlocks the door is `unlock_door`. It gets called from main at address `0x4466`. In order to reach that piece of code, `r15` at `0x4450` must **not** be zero. The content of `r15` is set at inside `check_password` that is called at `0x444c`. `check_password` reads byte per byte *(that is, incrementing by one the content of `r15` with each loop iteration)* starting at `@r15`(address where our input is stored) until it finds a null byte. Null byte is `\0` and it is used to represent end of character sequence. It is usually called null trailing byte. Read more about null-terminated strings [here](https://en.wikipedia.org/wiki/Null-terminated_string). If the number of bytes read is 0x9, `check_password` places 0x1 into `r15`, otherwise it places 0x0.

The <yellow>solution</yellow> of the level consists of providing as input whatever 8 characters, or bytes if you input it as hexadecimal. For example, "AAAABBBB" or "password".

<p align="center">
<img src="/images/microcorruption-tutorial-solved.png">
</p>

## More levels
* Click [here](/microcorruption/new-orleans) to see next level (New Orleans).
* Click [here](/microcorruption) to see levels index. 





