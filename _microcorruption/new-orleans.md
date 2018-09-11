---
title: "Microcorruption - New Orleans"
date: 2018-09-10
categories: [microcorruption, reverse engineering]
tags: [microcorruption, new orleans, assembly, ctf, tutorial, walkthrough, debug]
description: Microcorruption New Orleans level explained in detail.
hasComments: true
image: /images/microcorruption-levels-image.png
---
After completing the tutorial tutorial level, explained in detail [here](/microcorruption/tutorial), we are tossed into the wild. New Orleans is the first level that no longer guides the process of debugging and reversing nor holds our hand or gives us fancy hints. We are now facing the assembly code all by ourselves. Let's break it! 

As we will always do, the first thing to inspect is our `main` function because that's where our program starts, for now. 

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

Nevertheless, there is a little but very important difference. At address `0x4440` there is a call to `create_password` function. Let's find out what `create_password` is up to.

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

First of all, at instruction `0x447e` it is placing the hex number 0x2400 into `r15`. At this point you may feel a little confused about when a value is a simply number, an integer, or a memoy address. It does not matter. It is just data placed into a register. Data is represented in bits that form bytes and those bytes are placed either in the stack, heap, registers, etc... They are simply bytes. The difference comes at the time of reading, using, interpreting and manipulating those bytes. # TODO (text is incomplete but i gotta go)

## More levels
* Click [here](/microcorruption/new-orleans) to see next level (New Orleans).
* Click [here](/microcorruption/tutorial) to see previous level (Tutorial).
* Click [here](/microcorruption) to see levels index. 

