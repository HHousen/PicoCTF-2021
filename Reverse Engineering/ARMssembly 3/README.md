# ARMssembly 3

## Problem

> What integer does this program print with argument 2541039191? File: chall_3.S Flag format: picoCTF{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be picoCTF{0055aabb})

* [Source](./chall_3.S)

## Solution

1. This challenge can be solved using the exact same method as [ARMssembly 0](../ARMssembly%200/README.md).

2. Note that the output was `Result: 57`. Converting this to hexadecimal produces `39`. However, the instructions say that the flag is 32 bits, so we can simply pad out the hexadecimal to `00000039`.

### Flag

`picoCTF{00000039}`
