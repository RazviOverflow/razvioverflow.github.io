---
title: "Microcorruption - New Orleans"
date: 2018-09-11
categories: [microcorruption, reverse engineering]
tags: [microcorruption, new orleans, assembly, ctf, tutorial, walkthrough, debug]
description: Microcorruption New Orleans level explained in detail. We will see how to solve the level and understand the underlying concepts. 
hasComments: true
image: /images/microcorruption-levels-image.png
---
After completing the tutorial tutorial level, explained in detail [here](/microcorruption/tutorial), we are tossed into the wild. New Orleans is the first level that no longer guides the process of debugging and reversing nor holds our hand or gives us fancy hints. We are now facing the assembly code all by ourselves. Let's break it! 

As we will always do, the first thing to inspect is our `main` function because that's where our program starts. *(This may change in the future)* 

New Orleans' main has the following code:
``` 
438 <main>
4438:  3150 9cff      add	#0xff9c, sp
443c:  b012 7e44      call	#0x447e <create_password>
4440:  3f40 e444      mov	#0x44e4 "Enter the password to continue", r15
4444:  b012 9445      call	#0x4594 <puts>
4448:  0f41           mov	sp, r15
444a:  b012 b244      call	#0x44b2 <get_password>
444e:  0f41           mov	sp, r15
4450:  b012 bc44      call	#0x44bc <check_password>
4454:  0f93           tst	r15
4456:  0520           jnz	#0x4462 <main+0x2a>
4458:  3f40 0345      mov	#0x4503 "Invalid password; try again.", r15
445c:  b012 9445      call	#0x4594 <puts>
4460:  063c           jmp	#0x446e <main+0x36>
4462:  3f40 2045      mov	#0x4520 "Access Granted!", r15
4466:  b012 9445      call	#0x4594 <puts>
446a:  b012 d644      call	#0x44d6 <unlock_door>
446e:  0f43           clr	r15
4470:  3150 6400      add	#0x64, sp
```

The structure is almost identical to previous level main. A string gets printed, user inserts his/her password, the password is checked and depending on that check result, which is stored in `r15`, it either unlocks the door or jumps over it and executes until `__stop_progExec__` is reached and program ends with no success.

Nevertheless, there is a little but very important difference. At address `0x4450` there is a call to `create_password` function. Let's find out what `create_password` is up to.

```
447e <create_password>
447e:  3f40 0024      mov	#0x2400, r15
4482:  ff40 6600 0000 mov.b	#0x66, 0x0(r15)
4488:  ff40 6900 0100 mov.b	#0x69, 0x1(r15)
448e:  ff40 7300 0200 mov.b	#0x73, 0x2(r15)
4494:  ff40 3500 0300 mov.b	#0x35, 0x3(r15)
449a:  ff40 6100 0400 mov.b	#0x61, 0x4(r15)
44a0:  ff40 6b00 0500 mov.b	#0x6b, 0x5(r15)
44a6:  ff40 2900 0600 mov.b	#0x29, 0x6(r15)
44ac:  cf43 0700      mov.b	#0x0, 0x7(r15)
44b0:  3041           ret
```

First of all, at instruction `0x447e`, the program is placing the hex number 0x2400 into `r15`. At this point you may feel a little confused about when a value is a simply number, an integer, or a memoy address. It does not matter. It is just data being placed into a register. Data is represented in bits that form bytes and those bytes are placed either in the stack, heap, registers, etc... They are simply bytes. The difference comes at the time of reading, using, interpreting and manipulating those bytes. For example, if you would now do a *mov r15, sp*, sp content would automatically be 0x2400 and that would be treated as a memory address since sp is a pointer that points (wow) to some memory location. 

The next 8 instructions, from `0x4482` to `0x44ac`, are moving bytes intro addresses relatives to `r15`. This is called relative offset addressing. You can read about it [here](https://stackoverflow.com/questions/21207778/what-does-0x0r15-mean) and about general relative addressing [here](https://www.webopedia.com/TERM/R/relative_address.html). Relative addressing is coded in the way of <gold>x</gold><red>(baseAddr)</red>. It essentially means retrieving <red>(baseAddr)</red>'s value, adding <gold>x</gold> to it and treating it as memory address. Since `r15` is 0x2400, instruction at `0x4482` will place #0x66 into address 0x2400, instruction at `0x4488` will place #0x69 into address 0x2401 and so forth.

You will notice, however, the instruction being used is `mov.b` rather than `mov`. In MSP430 family, <red>.b</red> suffix is oposite to <purple>.w or no suffix</purple>. You can read more about it in this [Microcorruption-related post](https://stackoverflow.com/questions/37533375/mov-vs-mov-b-assembly-language-instruction). 

We do also have a very useful [excerpt from MSP430's manual](https://www.ti.com/sc/docs/products/micro/msp430/userguid/as_5.pdf) which provides us a very handy instruction's set overview.

<p align="center">
<img src="/images/microcorruption-new-orleans-instruction-overview.png">
</p>

So, what `create_password` does is placing a sequence of 8 bytes starting from `0x2400` all the way to `0x2407`. ***(Plase note that the bytes placed at these addresses may differ. I guess they are randomly generated based on every single user's name.)***

In order to check that, we can place a breakpoint at `0x44b0`, right before `create_password` finishes, execute te program and inspect memory contents at that very moment. 

<p align="center">
<img src="/images/microcorruption-new-orleans-bp0.png">
</p>

You will notice that when the program reaches the breakpoint, at address `0x2400` there will be indeed the aforementioned bytes.

<p align="center">
<img src="/images/microcorruption-new-orleans-bp1.png">
</p>

You will notice in the <orange>Live Memory Dump</orange> window that at the right there is a column mainly composed by dots. Well, that column is the ASCII representation of the bytes you see selected. You can see the word "fis5ak)". That's because bytes 66, 69, 73, etc... have a printable ASCII character. In order to find all ASCII characters and their respective octal, hexadecimal, decimal, etc... representation you can insert *man ascii* in a Unix-like system shell or simply google it. If you look closely, the word "fis5ak" has only 7 characters while function `create_password` moves 8 bytes starting from address `0x2400`. That's because the last byte is the null trailing byte that marks the end of a char sequence, also called a string, and it is not ASCII printable. You can see the full ASCII printable characters [here](http://facweb.cs.depaul.edu/sjost/it212/documents/ascii-pr.htm).

If we look back at `main` for a moment, we can see `unlock_door` gets called at address `0x446a` and it's executed based upon the result of instruction at address `0x4544` which is set by `check_password`. Let's find out what does `check_password` do. 

```
44bc <check_password>
44bc:  0e43           clr	r14
44be:  0d4f           mov	r15, r13
44c0:  0d5e           add	r14, r13
44c2:  ee9d 0024      cmp.b	@r13, 0x2400(r14)
44c6:  0520           jne	#0x44d2 <check_password+0x16>
44c8:  1e53           inc	r14
44ca:  3e92           cmp	#0x8, r14
44cc:  f823           jne	#0x44be <check_password+0x2>
44ce:  1f43           mov	#0x1, r15
44d0:  3041           ret
44d2:  0f43           clr	r15
44d4:  3041           ret
```

The first thing we see is some registers work. It clears out `r14` *(that is, it performs `r14 = 0`)*, it moves content of `r15` into `r13` and adds `r14` to `r13` into `r13` *(`r13 += r14`)*. In order to know what `r15` value is at this point, we can either set a breakpoint at instruction `0x44be` for example, or simply look at the code itself. The `main` function, before calling `check_password`, operates `mov sp, r15` at `0x444e`. This means that `r15` points at the address where our input is living in memory *(stack)*.

At address `0x44c2` we see there is a byte comparison. `cmp.b @r13, 0x2400(r14)` is simply performing, in human language, ***(compare the byte stored at address saved in r13 with contents of the address stored at r14 with 0x2400 offset)***. Remember the `cmp` instruction what really does inside is `0x2400(r14) - @r13` and sets the flags accordingly without saving the result. 

If result of the comparison is other than zero, that is, the bytes are not equal, `jne` at `0x44c6` will get executed jumping all the way down to `0x44d2` finishing the function. If the result is zero, if the bytes are equal, `r14` will be incremented by one.

At instruction `0x44ca` there is `cmp #0x8, r14` which compares the value of r14 with hexadecimal number 0x8. If the two values are not equal, it jumps back to `0x44be` starting a new iteration of the loop. IF they indeed are equal, hexadecimal 0x1 is placed into `r15` and exits the function. *(Remember that `r15` must be different from zero after `check_password` so main can call `unlock_door`)*

### Solution

In other words, `check_password` is checking byte per byte the user input against the password created by `create_password` that was previously stored at address `0x2400`. Please note how `r14` gets incremented by one with every character from user's input that matches the bytes at '0x2400'. That's the way the function iterates over the stored bytes, with relative addressing. Think it that way:

> Suppose r15 is 0x4000. <br>
Repeat until r14 ix 0x8<br>
**Iteration 1.**  <br>
r14 = 0x0. r13 = r15 + r14 (0x4000 + 0x0). Byte at 0x4000 equals to byte at 0x2400(0)? If so, r14 += 0x1 and go to Iteration 2.<br>
**Iteration 2.** <br>
r14 = 0x1. r13 = 0x4000 + 0x1. Byte ate 0x4001 equals to byte at 0x2400(1)? If so, r14 += 0x1 and go to Iteration 3. <br>
...

Notice how `0x2400(1)` is exactly the same as `1(0x2400)`. That's what relative addressing is. 

So, the <gold>solution </gold> is pretty straight forward. We must provide as input the exact 7 bytes *(because the null trailing byte in implicit to gets function)* `create_password` is placing into memory.

Input can be either inserted as text or hexadecimal encoded.

<p align="center">
<img src="/images/microcorruption-new-orleans-solution0.png">
</p>

<p align="center">
<img src="/images/microcorruption-new-orleans-solution1.png">
</p>

<p align="center">
<img src="/images/microcorruption-new-orleans-solved.png">
</p>

### Recap

In this level we've seen the how important is to read the code seeking for hardcoded values, what ASCII is and what .b suffix means in the context of MSP430 assembly language.

## More levels
* Click [here](/microcorruption/sydney) to see next level (Sydney).
* Click [here](/microcorruption/tutorial) to see previous level (Tutorial).
* Click [here](/microcorruption) to see levels index. 

