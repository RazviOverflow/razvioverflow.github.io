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

That's essentially telling us the password is checked by other device we have no access to. So let's explore the code and find out what's happening!

This time, main has no other task rather than calling `login` function.
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

First of all, at address `0x453c` there is a call to `getsn`. This time it is calling `getsn` instead of `get_password` we've seen in previous levels. *(Even though `get_password` was in turn calling `getsn` inside, but that's none of our concern)* When using `getsn` one must pass two argmuments, the buffer where data must be stored and the number of bytes to be copied into it. This reminds us somehow of glibc's [fgets](https://linux.die.net/man/3/fgets). *(Remember we are in MSP430 context)*. So judging by the previous `mov` instructions at addresses `0x4534` and `0x4538`, we can assume that our input will be stored at address `0x2400` and a maximum of `0x1c` (28 decimal) bytes will be copied. This means that our input will be stored from `0x2400` all the way up to `0x241b`.  

At address `0x4544` a call to `test_password_valid` is made. The function's title is pretty self explanatory. We can see that right before the call, there is a `mov #0x2400, r15`. That's because it is passing as argument to `test_password_valid` the address the password to check is stored at. 

When `test_password_valid` finishes, there is a `tst r15` *(check if it's zero)* at address `0x4548`. If it is zero, it jumps to `0x4552` *(using the '<blue>$</blue>' operator explained in the previous level)* otherwise it doesn't take the jump executing `mov.b #0x26, &0x2410`. This instruction is simply putting the byte 0x26 into memory address &0x2410. Please note the '<purple>&</purple>' operand before a hex number denotes **<yellow>"at that memory address"</yellow>**.


Let's take a look to `test_password_valid`'s code:
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

### Solution

### Recap


## More levels
* Click [here](/microcorruption/cusco) to see next level (Cusco).
* Click [here](/microcorruption/hanoi) to see previous level (Hanoi).
* Click [here](/microcorruption) to see levels index.