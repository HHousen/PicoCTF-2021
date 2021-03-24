# Compress and Attack

## Problem

> Your goal is to find the flag. compress_and_attack.py `nc mercury.picoctf.net 50899`

* [compress_and_attack.py](./compress_and_attack.py)
* [Source](./vuln.c)

## Solution

1. Searching for the encryption used (`Salsa20`) suggests that [there are no published attacks](https://en.wikipedia.org/wiki/Salsa20#Cryptanalysis_of_Salsa20), so we'll need to look for a different attack vector.

2. Searching online for "compression and encryption" finds [this StackOverflow question](https://stackoverflow.com/a/30644897). Basically, since compression is applied before encryption and we control part of the text that is encrypted, we can strategically send payloads until the resulting cipher text length decreases. This idea is the basis for the [CRIME](https://en.wikipedia.org/wiki/CRIME) exploit, which the [StackOverflow question](https://stackoverflow.com/a/30644897) mentions.

3. Searching for "crime exploit python" reveals this amazing GitHub repository: [EiNSTeiN-/compression-oracle](https://github.com/EiNSTeiN-/compression-oracle). My slightly modified version of this script along with the solution to the challenge is in the [solution script](./script.py). The [solution script](./script.py) needs to be run with Python 2 because [EiNSTeiN-/compression-oracle](https://github.com/EiNSTeiN-/compression-oracle) is a very old repository. You can read more about the attack in the [EiNSTeiN-/compression-oracle README](https://github.com/EiNSTeiN-/compression-oracle/blob/master/README.md).

4. Running the [solution script](./script.py) produces the following output:

    ```
    [+] Opening connection to mercury.picoctf.net on port 50899: Done
    In round 0, ran all 29 guesses in 6 seconds
    After round #0, kept: 'picoCTF'+['{']
    In round 1, ran all 29 guesses in 6 seconds
    After round #1, kept: 'picoCTF{'+['s']
    In round 2, ran all 29 guesses in 6 seconds
    After round #2, kept: 'picoCTF{s'+['h']
    In round 3, ran all 29 guesses in 5 seconds
    After round #3, kept: 'picoCTF{sh'+['e']
    In round 4, ran all 29 guesses in 5 seconds
    After round #4, kept: 'picoCTF{she'+['r']
    In round 5, ran all 29 guesses in 6 seconds
    After round #5, kept: 'picoCTF{sher'+['i']
    In round 6, ran all 29 guesses in 5 seconds
    After round #6, kept: 'picoCTF{sheri'+['f']
    In round 7, ran all 29 guesses in 5 seconds
    After round #7, kept: 'picoCTF{sherif'+['f']
    In round 8, ran all 29 guesses in 5 seconds
    After round #8, kept: 'picoCTF{sheriff'+['_']
    In round 9, ran all 29 guesses in 5 seconds
    After round #9, kept: 'picoCTF{sheriff_'+['y']
    In round 10, ran all 29 guesses in 6 seconds
    After round #10, kept: 'picoCTF{sheriff_y'+['o']
    In round 11, ran all 29 guesses in 7 seconds
    After round #11, kept: 'picoCTF{sheriff_yo'+['u']
    In round 12, ran all 29 guesses in 7 seconds
    After round #12, kept: 'picoCTF{sheriff_you'+['_']
    In round 13, ran all 29 guesses in 7 seconds
    After round #13, kept: 'picoCTF{sheriff_you_'+['s']
    In round 14, ran all 29 guesses in 6 seconds
    After round #14, kept: 'picoCTF{sheriff_you_s'+['o']
    In round 15, ran all 29 guesses in 5 seconds
    After round #15, kept: 'picoCTF{sheriff_you_so'+['l']
    In round 16, ran all 29 guesses in 6 seconds
    After round #16, kept: 'picoCTF{sheriff_you_sol'+['v']
    In round 17, ran all 29 guesses in 6 seconds
    After round #17, kept: 'picoCTF{sheriff_you_solv'+['e']
    In round 18, ran all 29 guesses in 5 seconds
    After round #18, kept: 'picoCTF{sheriff_you_solve'+['d']
    In round 19, ran all 29 guesses in 5 seconds
    After round #19, kept: 'picoCTF{sheriff_you_solved'+['_']
    In round 20, ran all 29 guesses in 6 seconds
    After round #20, kept: 'picoCTF{sheriff_you_solved_'+['t']
    In round 21, ran all 29 guesses in 6 seconds
    After round #21, kept: 'picoCTF{sheriff_you_solved_t'+['h']
    In round 22, ran all 29 guesses in 6 seconds
    After round #22, kept: 'picoCTF{sheriff_you_solved_th'+['e']
    In round 23, ran all 29 guesses in 5 seconds
    After round #23, kept: 'picoCTF{sheriff_you_solved_the'+['_']
    In round 24, ran all 29 guesses in 6 seconds
    After round #24, kept: 'picoCTF{sheriff_you_solved_the_'+['c']
    In round 25, ran all 29 guesses in 5 seconds
    After round #25, kept: 'picoCTF{sheriff_you_solved_the_c'+['r']
    In round 26, ran all 29 guesses in 5 seconds
    After round #26, kept: 'picoCTF{sheriff_you_solved_the_cr'+['i']
    In round 27, ran all 29 guesses in 6 seconds
    After round #27, kept: 'picoCTF{sheriff_you_solved_the_cri'+['m']
    In round 28, ran all 29 guesses in 5 seconds
    After round #28, kept: 'picoCTF{sheriff_you_solved_the_crim'+['e']
    Retrying connection...
    [+] Opening connection to mercury.picoctf.net on port 50899: Done
    In round 29, ran all 29 guesses in 6 seconds
    After round #29, kept: 'picoCTF{sheriff_you_solved_the_crime'+['}']
    Flag: picoCTF{sheriff_you_solved_the_crime}
    ```

5. I modified the [EiNSTeiN-/compression-oracle](https://github.com/EiNSTeiN-/compression-oracle) code to not use threading since it messed with `pwntools`, exit when the `}` character is kept, and of course added the details specific to this challenge.

### Flag

`picoCTF{sheriff_you_solved_the_crime}`
