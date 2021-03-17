# New Caesar

## Problem

> We found a brand new type of encryption, can you break the secret code? (Wrap with picoCTF{}) `kjlijdliljhdjdhfkfkhhjkkhhkihlhnhghekfhmhjhkhfhekfkkkjkghghjhlhghmhhhfkikfkfhm` new_caesar.py

## Solution

1. Let's reverse the [new_caesar.py](./new_caesar.py) program.

2. See comments in the solution [script](./script.py) for a detailed explanation. We reverse the encoding mechanism, then try the possible offsets, and print the possible flags.

### Flag

`picoCTF{et_tu?_1ac5f3d7920a85610afeb2572831daa8}`
