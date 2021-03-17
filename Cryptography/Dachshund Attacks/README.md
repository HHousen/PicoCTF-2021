# Dachshund Attacks

## Problem

> What if d is too small? Connect with nc mercury.picoctf.net 31133.

## Solution

1. I tried using [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool), but for some reason it would not solve this one even if I specified `--attack wiener`.

2. Instead, we can use the [owiener Python package](https://pypi.org/project/owiener/) in the solution [script](./script.py).

3. We can then decrypt the ciphertext using [an approach from RosettaCode](https://rosettacode.org/wiki/RSA_code#Python).

### Flag

`picoCTF{proving_wiener_1146084}`
