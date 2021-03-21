# Mini RSA

## Problem

> What happens if you have a small exponent? There is a twist though, we padded the plaintext so that (M ** e) is just barely larger than N. Let's decrypt this: ciphertext

* [ciphertext](./ciphertext)

## Solution

1. I spent a while (2 hours) searching for resources to solve this. However, [this Cryptography StackExchange comment](https://crypto.stackexchange.com/a/6771) is where I found the solution. Other helpful resources include: [RSA Padding Schemes - Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Padding_schemes), [Cryptography StackExchange 1](https://crypto.stackexchange.com/a/64304), [Cryptography StackExchange 2](https://crypto.stackexchange.com/a/80346), and [Cryptography StackExchange 3](https://crypto.stackexchange.com/a/111)

2. Without padding, encryption of `m` is `m^e mod n`: the message `m` is interpreted as an integer, then raised to exponent `e`, and the result is reduced modulo `n`. If `e = 3` and `m` is short, then `m^3` could be an integer which is smaller than `n`, in which case the modulo operation is a no-operation. In that case, you can just compute the cube root of the value you have. However, we cannot simply compute `c^(1/3)` (where `c` is the ciphertext) because there is a slight amount of padding to the message to make `m^e` larger than `n`, which makes the modulo operation take effect.

3. With a short `m` slightly wider than `n^(1/e)`, which is what we have, we are given `c = m^e mod n` and can find by enumeration `k` such that `k * n + c` is an `e`th power: then `m = (k * n + c)^(1/e)`.

4. We can use python and write a [solution script](./script.py) to search though thousnads of values for `k` until we find one that contains the start of the flag. When we find the padding amount, we can increase the precision and rerun the calculation to get the entire flag. Keeping the precision high enough just to see the beginning of the flag speeds up the enumeration of `k`.

### Flag

`picoCTF{e_sh0u1d_b3_lArg3r_a166c1e3}`
