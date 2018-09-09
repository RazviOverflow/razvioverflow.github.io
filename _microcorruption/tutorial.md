---
title: "Microcorruption - Tutorial"
date: 2018-09-09
categories: [microcorruption, reverse engineering]
tags: [microcorruption, tutorial, assembly, ctf, tutorial, walkthrough, debug]
description: Microcorruption tutorial level explained in detail.
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

As always, there is a main function that marks our starting point. *Well, in fact there are other functions executed before main as __init_stack, __low_level_init and __do_copy_data but that's none of our concern as of right now.* 

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

Right at the instruction at `0x4450`, there is `tst r15`. `tst` stands for *test* and it is used to widely used to check some value against 0 and as a more efficient alternative to `cmp #0, argument`. It operates bitwise AND with the argument(s) and set the registers, also called flags, accordingly without saving the result. In the case of MSP430 microcontroller, `tst r15` is basically **r15 AND r15**. Read more about `tst` [here](https://stackoverflow.com/a/44749414).

The following instruction is `jnz #0x445e <main+0x26>` at `0x4520`. `jnz` stands for *jump if not zero*. In this context, not zero refers to the result of the last computed operation. In order to check if it is zero or not, the instruction inspects the flag that was previously modified by `tst`, the Zero Flag (ZF). In human language, the instruction means ***if Zero Flag is 0, jump to address `0x445e`, otherwise continue***. Please note that ZF is set to 1 only when the result is 0. Read more about conditional jumps and zero flag [here](https://stackoverflow.com/a/14267642).








