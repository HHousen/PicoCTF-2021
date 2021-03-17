# Transformation

## Problem

> I wonder what this really is... enc `''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])`

* [enc](./enc)

## Solution

1. `cat enc`: `灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸弲㘶㠴挲ぽ`

2. The python code in the challenge text is the program used to encode the original flag. It is the program that we need to reverse.

3. The program shifts the bits for every other letter of the flag left by 8 bits (1 byte). Then, it adds the next latter of the flag to the shifted value. In other words, each letter is represented as a byte and they are joined together in pairs of two.

4. We can reverse this (see [script.py](./script.py)) by looping through the encoded flag and for each loop we:

    1. Shift the bits right to get the first letter in the pair.

    2. Convert the encoded character to bytes and get the last byte to get the second letter in the pair.

    3. Append the letters to the `flag` variable.

### Flag

`picoCTF{16_bits_inst34d_of_8_26684c20}`
