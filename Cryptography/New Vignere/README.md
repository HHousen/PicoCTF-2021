# New Vignere

## Problem

> Another slight twist on a classic, see if you can recover the flag. (Wrap with picoCTF{}) `epdfglkfnbjbhbpicohidjgkhfnejeecmjfnejddgmhpndmchbmifnepdhdmhbah` new_vignere.py

* [new_vignere.py](./new_vignere.py)

## Solution

1. This challenge is similar to [New Caesar](../New%20Caesar/README.md) (the code is nearly identical) except its a Vignere cipher.

2. The hint for this challenge points to [The Cryptanalysis section of Vigenère Cipher Wikipedia Page](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher#Cryptanalysis), which explains the "Kasiski examination". We can use [an online Kasiski test tool](https://planetcalc.com/8550/) to automatically find the key length to be `9`. [DCode](https://www.dcode.fr/vigenere-cipher) shows that the key length could be `3`, `9`, or `6`.

3. The [Wikipedia page](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher#Cryptanalysis) recommends using [Kerckhoffs' method](https://en.wikipedia.org/wiki/Auguste_Kerckhoffs) to discover the key letter (Caesar shift) for each column of the vignere cipher. However, that does not work in this case because the Vigenère table has been scrambled by the `b16_encode` function.

4. According to Wikipedia: "Once the length of the key is known, the ciphertext can be rewritten into that many columns, with each column corresponding to a single letter of the key. Each column consists of plaintext that has been encrypted by a single Caesar cipher. The Caesar key (shift) is just the letter of the Vigenère key that was used for that column. Using methods similar to those used to break the Caesar cipher, the letters in the ciphertext can be discovered."

5. I sort of implement the above method. The problem is the `b16_encode` function, which splits the letters of the flag in two. Because of this function, we cannot simply bruteforce each column of the Vignere matrix as described above the output is transformed by the `b16_decode` function. The letters are merged together and the output might not fit within the alphabet even if the key is correct.

6. However, we can still use the above method to make educated guesses about the key since if the `b16_decode` function produces valid ascii output with a certain caesar key then it is likely to be the correct key. This bruteforce takes place on lines 53-77 of the [solve script](./script.py).

7. Next, we bruteforce the letters of the key that we could not make educated guesses for using `itertools.permutations`. We test every possible key (keeping the guessed letters constant) and display the output when it satisfying the assert statement on line 20 of [new_vignere.py](./new_vignere.py).

8. [solve script](./script) output:

    ```
    Vignere Matrix:
    [['e' 'p' 'd' 'f' 'g' 'l' 'k' 'f' 'n']
    ['b' 'j' 'b' 'h' 'b' 'p' 'i' 'c' 'o']
    ['h' 'i' 'd' 'j' 'g' 'k' 'h' 'f' 'n']
    ['e' 'j' 'e' 'e' 'c' 'm' 'j' 'f' 'n']
    ['e' 'j' 'd' 'd' 'g' 'm' 'h' 'p' 'n']
    ['d' 'm' 'c' 'h' 'b' 'm' 'i' 'f' 'n']
    ['e' 'p' 'd' 'h' 'd' 'm' 'h' 'b' 'a']
    ['h' '0' '0' '0' '0' '0' '0' '0' '0']]
    Trying column 0... Found key `b`... 
    Trying column 1... 
    Trying column 2... Found key `a`... 
    Trying column 3... 
    Trying column 4... Found key `a`... Found key `f`... Found key `g`... 
    Trying column 5... 
    Trying column 6... Found key `e`... 
    Trying column 7... Found key `p`... 
    Trying column 8... Found key `k`... 
    Key Possibilities: {0: ['b'], 1: -1, 2: ['a'], 3: -1, 4: ['a', 'f', 'g'], 5: -1, 6: ['e'], 7: ['p'], 8: ['k']}
    Bruteforcing 3 values...
    1791it [00:00, 8611.44it/s]
    Flag Possibility: picoCTF{94bf01ad4b8a63425c32c02ba4c9632f}
    3360it [00:00, 9305.95it/s]
    Bruteforcing Complete
    Total Guesses: 3504
    ```

### Flag

`picoCTF{94bf01ad4b8a63425c32c02ba4c9632f}`
