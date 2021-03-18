# Play Nice

## Problem

> Not all ancient ciphers were so bad... The flag is not in standard format. `nc mercury.picoctf.net 6057` playfair.py

* [Program](./playfair.py)

## Solution

1. Look at the source code and at the bottom it links to [the Wikipedia page for a Playfair cipher](https://en.wikipedia.org/wiki/Playfair_cipher)

2. Find a Playfair cipher decoder, such as [DCode](https://www.dcode.fr/playfair-cipher). Paste in the ciphertext `y7bcvefqecwfste224508y1ufb21ld` and the alphabet/key `meiktp6yh4wxruavj9no13fb8d027c5glzsq`. Make sure to increase the grid size to 6x6 so the entire alphabet fits.

3. Click "Decrypt" to get `WD9BUKBSPDTJ7SKD3KL8D6OA3F03G0` convert this to lowercase with `python -c "print('WD9BUKBSPDTJ7SKD3KL8D6OA3F03G0'.lower())"` to get `wd9bukbspdtj7skd3kl8d6oa3f03g0`.

4. Paste the decrypted text into the program on the server to get the flag: `Congratulations! Here's the flag: 2e71b99fd3d07af3808f8dff2652ae0e`.

### Flag

`2e71b99fd3d07af3808f8dff2652ae0e`
