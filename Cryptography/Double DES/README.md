# Double DES

## Problem

> I wanted an encryption service that's more secure than regular DES, but not as slow as 3DES... The flag is not in standard format. nc mercury.picoctf.net 1903 ddes.py

* [ddes.py](./ddes.py)

## Solution

1. Connect to get the encrypted flag: `nc mercury.picoctf.net 1903` to get `6f745ccee635f76746be185541b9f9c046b8d707f93d0522e2325fb041c59ec7bbbaa818d7c51381`. For this challenge we will need a set of plaintext and ciphertext strings so I encrypt `13371337` and get `8f45ca8a9264c2aa` back as the encrypted data.

2. [Regular DES](https://en.wikipedia.org/wiki/Data_Encryption_Standard#Brute-force_attack) is vulnerable to bruteforce since it only uses an 8 byte key. [Triple DES](https://en.wikipedia.org/wiki/Triple_DES) is used to remedy this, but it too is now insecure. Since we are able to obtain a set of plaintext and ciphertext, we will probably be using a known plaintext attack.

3. Double DES is vulnerable to a [meet-in-the-middle attack](https://en.wikipedia.org/wiki/Meet-in-the-middle_attack). [This StackExchange answer](https://security.stackexchange.com/a/122626) explains the attack perfectly. Basically, you start with the plain text, and then you bruteforce every possible key, encrypt the plain text, and store the results in a dictionary. Then, you take the original encrypted data (`8f45ca8a9264c2aa` in this case) and bruteforce decrypt it using every possible key, storing the results as you go. Then, you find the intersection between the encrypted and decrypted values. The keys corresponding to the overlapping value are the two keys used in the Double DES algorithm.

4. This challenge makes the above attack even easier because it only uses 6 bytes (instead of the standard 8 used in DES) and simply uses padding (aka two spaces) for the last 2 bytes. The [solve script](./script.py) bruteforces the first and second key using the aforementioned exploit. Then it finds the intersection using Python's `set` class. Finally, now that both keys are known, the encrypted flag is decrypted.

### Flag

`cb120914153b84dbc68fedd574b395f2`
