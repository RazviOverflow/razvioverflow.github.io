---
title: "Microcorruption - Hanoi"
date: 2018-09-17
categories: [microcorruption, reverse engineering]
tags: [microcorruption, tutorial, assembly, ctf, hanoi, walkthrough, debug]
description: Microcorruption Hanoi level explained in detail. We will see how to solve the level and understand the underlying concepts. 
hasComments: true
image: /images/microcorruption-levels-image.png
---

In this new level some things have changed. If you read the manual that pops up at the beginning of the level, you can notice that, toward the end, it states:

> There  is no  default  password  on the  LockIT  Pro HSM-1.   Upon
    receiving the  LockIT Pro,  a new  password must  be set  by first
    connecting the LockitPRO HSM to  output port two, connecting it to
    the LockIT Pro App, and entering a new password when prompted, and
    then restarting the LockIT Pro using the red button on the back.

That's essentially telling us the password is checked by other device we have no access to. 

If you were to execute the program, you will notice there is a message rembembering the password must be between 8 and 16 characters.

<p align="center">
<img src="/images/microcorruption-hanoi0.png">
</p>

So let's explore the code and find out what's happening! This time, main has no other task rather than calling `login` function.
```
4438 <main>
4438:  b012 2045      call	#0x4520 <login>
443c:  0f43           clr	r15
```

Exploring `login`'s code we can make some assumptions:

```
4520 <login>
4520:  c243 1024      mov.b	#0x0, &0x2410
4524:  3f40 7e44      mov	#0x447e "Enter the password to continue.", r15
4528:  b012 de45      call	#0x45de <puts>
452c:  3f40 9e44      mov	#0x449e "Remember: passwords are between 8 and 16 characters.", r15
4530:  b012 de45      call	#0x45de <puts>
4534:  3e40 1c00      mov	#0x1c, r14
4538:  3f40 0024      mov	#0x2400, r15
453c:  b012 ce45      call	#0x45ce <getsn>
4540:  3f40 0024      mov	#0x2400, r15
4544:  b012 5444      call	#0x4454 <test_password_valid>
4548:  0f93           tst	r15
454a:  0324           jz	$+0x8
454c:  f240 2600 1024 mov.b	#0x26, &0x2410
4552:  3f40 d344      mov	#0x44d3 "Testing if password is valid.", r15
4556:  b012 de45      call	#0x45de <puts>
455a:  f290 9100 1024 cmp.b	#0x91, &0x2410
4560:  0720           jne	#0x4570 <login+0x50>
4562:  3f40 f144      mov	#0x44f1 "Access granted.", r15
4566:  b012 de45      call	#0x45de <puts>
456a:  b012 4844      call	#0x4448 <unlock_door>
456e:  3041           ret
4570:  3f40 0145      mov	#0x4501 "That password is not correct.", r15
4574:  b012 de45      call	#0x45de <puts>
4578:  3041           ret
```

First of all, at address `0x453c` there is a call to `getsn`. This time it is calling `getsn` instead of `get_password` we've seen in previous levels. *(Even though `get_password` was in turn calling `getsn` inside, but that's none of our concern)* When using `getsn` one must pass two argmuments, the buffer where data must be stored and the number of bytes to be copied into it. This reminds us somehow of glibc's [fgets](https://linux.die.net/man/3/fgets). *(Remember we are in MSP430 context)*. So judging by the previous `mov` instructions at addresses `0x4534` and `0x4538`, we can assume that our input will be stored at address `0x2400` and a maximum of `0x1c` (28 decimal) bytes will be copied. This means that our input will be stored from `0x2400` all the way up to `0x241b`. So the message being printed at the beginning of execution has no meaning. Passwords can be whatever length with a maximum of 28 characters. **<red>The moral is to never trust what printed instructions say and always test the program beyond them.</red>**

At address `0x4544` a call to `test_password_valid` is made. The function's title is pretty self explanatory. We can see that right before the call, there is a `mov #0x2400, r15`. That's because it is passing as argument to `test_password_valid` the address the password to check is stored at. 

When `test_password_valid` finishes, there is a `tst r15` *(check if it's zero)* at address `0x4548`. If it is zero, it jumps to `0x4552` *(using the '<blue>$</blue>' operator explained in the previous level)* otherwise it doesn't take the jump executing `mov.b #0x26, &0x2410`. This instruction is simply putting the byte 0x26 into memory address &0x2410. Please note the '<purple>&</purple>' operand before a hex number denotes **<yellow>"at that memory address"</yellow>**.

At address `0x455a` a comparison is being made. `cmp.b #0x91, &0x2410` is checking whether the value 0x91 is at memory address 0x2410. If it indeed is, it unlock the door. Otherwise it prints out "The password is not correct" and finishes the execution. 

So, <red>as an early analysis</red> we could say that, in order to unlock the level, we must input something that after calling `test_password_valid` places into `r15` zero. This way, we jump over instruction `0x454c` which places `0x26` into memory address `0x2410`. Then we must get, somehow, the value `0x91` to be into memory address `0x2410`. Unlocking the level definitely depends on `0x91` being at memory address `0x2410` or not. We shall, then, explore how `test_password_valid`'s code looks like.
```
4454 <test_password_valid>
4454:  0412           push	r4
4456:  0441           mov	sp, r4
4458:  2453           incd	r4
445a:  2183           decd	sp
445c:  c443 fcff      mov.b	#0x0, -0x4(r4)
4460:  3e40 fcff      mov	#0xfffc, r14
4464:  0e54           add	r4, r14
4466:  0e12           push	r14
4468:  0f12           push	r15
446a:  3012 7d00      push	#0x7d
446e:  b012 7a45      call	#0x457a <INT>
4472:  5f44 fcff      mov.b	-0x4(r4), r15
4476:  8f11           sxt	r15
4478:  3152           add	#0x8, sp
447a:  3441           pop	r4
447c:  3041           ret
```
Strange. Based upon my analysis there is nothing related to placing `0x91` into `0x2410` **<red>but</red>** we can definitely learn something. If you look closely, you will notice at address `0x446e` there is a `call #0x457a <INT>`. That's a call to system's interruption function. Right above it, the previous instruction, is pushing `0x7d` value into the stack. That's because `INT` *(interruption)* function must know what interruption to execute. How can we actually know what `0x7d` interruption means? Pretty simple, we must look for it in the [LockIT Pro Manual](https://microcorruption.com/manual.pdf) that was already mentioned at the very first level, [Tutorial](/microcorruption/tutorial).

At page 7 of the Manual we can see INT declaration.

<p align="center">
<img src="/images/microcorruption-hanoi-manual0.png">
</p>

From pages 8 to 10 we can see all interruptions the system can execute. In this very case, `0x7d` means as follows:

<p align="center">
<img src="/images/microcorruption-hanoi-manual1.png">
</p>

So it takes two arguments. In our case `r14` is the password to test and `r15` is the location of the flag to overwrite is the password is correct. This definitely is related to solving the level since we already stated before that we need a zero in `r15` upon exiting `test_password_valid`. Knowing interruptions is very important and will be later used in future levels. Another example is `unlock_door` function.
```
4448 <unlock_door>
4448:  3012 7f00      push	#0x7f
444c:  b012 7a45      call	#0x457a <INT>
4450:  2153           incd	sp
4452:  3041           ret
```
As you can see, `0x7f` is being pushed into the stack right before `INT` is being called.

<p align="center">
<img src="/images/microcorruption-hanoi-manual2.png">
</p>

It takes no arguments, it simply unlocks the door. 

Coming back to unlocking the level, we do not have access to the code that decides what value must be placed into `r15` because it belongs to another piece of hardware. 

Well then, what are we ought to do? **HEY, wait a second.** We just saw that unlocking the level depends upon `0x91` value being or not at `0x2410` memory address. We also saw that, despite what the program says about password being between 8 and 16 chars, we control input from `0x2400` all the way up to `0x241b` which means **<gold>the flag that determines if the level is unlocked lives within the memory range we control via our input.</gold>** That is, we can insert the flag to unlock the level via our input no matter if the rest of the password is correct.

The only unkown that remains is whether `r15` will be zero at `0x4544`. Remember we want it to be zero so the `0x91` we're about to place at `0x2410` doesn't get overwritten by the instruction at `0x454c`. Let us place a breakpoint right at `0x4548` and input some random chars and see what `r15`'s value is.

We place the breakpoint.

<p align="center">
<img src="/images/microcorruption-hanoi1.png">
</p>

We input some random characters. *(24 x A in my case)*

<p align="center">
<img src="/images/microcorruption-hanoi2.png">
</p>

And then we confirm `r15` is indeed zero when the breakpoint is hit. **That's fantastic!**

<p align="center">
<img src="/images/microcorruption-hanoi3.png">
</p>

### Solution

As we've seen before, in order to solve the level there must be a `0x91` at address `0x2410`. Since our input is stored from `0x2400` to `0x241b`, it is as easy as counting up bytes. 

We have to input 16 random bytes, from `0x2400` to `0x240f` and then `0x91`. Since `0x91` is not a printable ASCII character, we will hex encode our input. 

In my case my input was: **<yellow>4141414141414141414141414141414191</yellow>**

<p align="center">
<img src="/images/microcorruption-hanoi4.png">
</p>

And the level is solved! :D

<p align="center">
<img src="/images/microcorruption-hanoi5.png">
</p>

### Recap

In this level we've seen how important is to understand what functions are being used and what parameters do they take as well as knwoing the memory range we're working into and system interruptions.

## More levels
* Click [here](/microcorruption/cusco) to see next level (Cusco).
* Click [here](/microcorruption/sydney) to see previous level (Sydney).
* Click [here](/microcorruption) to see levels index.