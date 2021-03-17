# Easy Peasy

## Problem

> A one-time pad is unbreakable, but can you manage to recover the flag? (Wrap with picoCTF{}) nc mercury.picoctf.net 20266 otp.py

* [otp.py](./otp.py)

## Solution

1. As stated in the description, this is a [one-time pad](https://en.wikipedia.org/wiki/One-time_pad) challenge. One of the criteria of a one-time pad is that the key is never reused in part or in whole. We can modify the program so that it does not meet this requirement.

2. The significant bug in the [otp.py](./otp.py) script appears on lines 34-36:

    ```python
    if stop >= KEY_LEN:
		stop = stop % KEY_LEN
		key = kf[start:] + kf[:stop]
    ```

    `stop` equals the previous ending point of the key plus the length of the new user input. However, if `stop` is greater than the key length, `stop` is set to `stop % KEY_LEN`. Thus, inputting just enough text to get to the end of the keyfile will set `stop` to 0 because `40000 % 40000` is `0`. `key_location` is then set to `stop` and `key_location` is returned. So, when we input the next string to be encrypted the `encrypt` function will receive `key_location=0`, thus allowing us to use the same key that was used to encrypt the flag.

3. Generate a `pwntools` template with `pwn template --host mercury.picoctf.net --port 20266 otp.py`.

4. The solve [script](./script.py) is commented and explains the solution. In brief, since we know a clear text message and an encrypted message, we can find the key (as explained in [this Computer Science StackExchange answer](https://cs.stackexchange.com/a/365)) and then decrypt the flag.

### Flag

`picoCTF{99072996e6f7d397f6ea0128b4517c23}`
