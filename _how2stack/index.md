---
title: "How2Stack"
date: 2025-05-06
categories: [pwn, binary exploitation, binexp, tutorial]
image: /images/247ctf/pwnable/hidden_flag_function/stack_behavior.png
tags: [assembly, tutorial, walkthrough, debug, reverse engineering, exploiting, pwn, binary exploitation]
description: Binary exploitation (PWN) tutorials to help you understand the foundations of stack-based exploitation techniques.
---
<style>
	/* Responsive iframe */ 
	.video-container {
	    position: relative;
	    width: 100%;
	    height: 0;
	    padding-bottom: 56.25%;
	}
	.video {
	    position: absolute;
	    top: 0;
	    left: 0;
	    width: 100%;
	    height: 100%;
	}
</style>

Binary exploitation (PWN) tutorials to help you understand the foundations of stack-based exploitation techniques.

I will be posting the videos I record as well as online resources for you to further understand the underlying concepts and techniques. 

Contents:
* Basic Concepts:
	* **Endianness**
	* **Global Offset Table (GOT) and Procedure Linkage Table (PLT)**
	* **How to debug the exploit**
* Exploitation Techniques:
	* **Buffer Overflow**
	* **Execution Flow Hijacking (ret2win)**
	* **Shellcode Execution (ret2shellcode)**
	* **Integer Overflow / Underflow**
	* **Format String**
	* **PIE and Canary Bypass**
	* **GOT overwrite**
	* **Return Oriented Programming (ROP)**
	* **Return to Libc (ret2libc)**
	* **Making stack executable with malicious mprotect call**
	* **Advanced Format String**
		* **vfprintf internal buffer**
		* **Abusing %s and %n**

## Endianness

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/T8E_JRqN0fY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## Buffer Overflow

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/0_merdYty4Y" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/DiyFDCuyPqg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## Execution Flow Hijackintg (ret2win)

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/-VUtXwDm5yQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## Shellcode Execution (ret2shellcode)

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/6Yiupj3XHrM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## Integer Overflow / Underflow

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/Mfaq4PW8H1I" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## Format String
<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/0-ulL3Y0MS8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## PIE and Canary Bypass

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/FpKL2cAlJbM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## Global Offset Table (GOT) and Procedure Linkage Table (PLT)

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/B4-wVdQo040" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## GOT overwrite

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/9SWYvhY5dYw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## Return Oriented Programming (ROP)

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/8zRoMAkGYQE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## Return to Libc (ret2libc)

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/TTCz3kMutSs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## How to debug the exploit

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/CWxDhp0OFzI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## Making stack executable with malicious mprotect call

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/r_tysAKIELs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

## Advanced Format String

### vfprintf internal buffer

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/K690__BET10" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>

### Abusing %s and %n

<div class="video-container">
	<iframe width="840" height="478" src="https://www.youtube.com/embed/FF8SRxMP8Bc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" class="video" allowfullscreen></iframe>
</div>