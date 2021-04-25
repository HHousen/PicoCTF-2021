# It's Not My Fault 1

## Problem

> What do you mean RSA with CRT has an attack that's not a fault attack? Connect with nc mercury.picoctf.net 26695. not_my_fault.py

* [not_my_fault.py](./not_my_fault.py)

## Solution

1. The first step of this problem is to get past the MD5 proof-of-work. We need to find a string that starts with a random 5 character long string and creates an MD5 hash that ends with a string of 6 random hex characters. This can be bruteforced with a simple script.

2. After we complete the md5 proof-of-work section, we are shown the public modulus and a clue, which is the public exponent. There is a function called `get_flag` that is called and will print the flag if we pass in `p+q` in less than 15 minutes. The public exponent, `e`, was generated using the two Chinese Remainder Theorem (CRT) exponents, `d_p` and `d_q`. `d_p` is at most 20 bits (a number between 1 and 1048576).

3. We can try to bruteforce `d_p` and thus find `p` and `q` using the approach discussed at [Attacking RSA for fun and CTF points – part 4](https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-4/), which I found by searching "rsa crt small dp bruteforce". However, searching for "rsa crt attack -fault" finds [this answer on MathOverflow](https://mathoverflow.net/a/120166), which discusses a much more complicated bruteforce that will execute much faster. This method is described on page 506 of Galbraith's book "Mathematics of Public Key Cryptography", where it is attributed to Pinch.

4. Since the math behind Pinch method is complicated, I'm going to be implementing the basic brute force approach from [here](https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-4/). You can learn more about the bruteforce on [that page](https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-4/), but the important part is this code:

    ```python
    >>> n=95580702933509662811256129990158655210667121276245053843875590334281563078868202152845967187641817281520364662600110239110410372520340630639373679599982371620736610194814723749147422221945978800055101110346161945811520158431287139909125886966214800526831490560384144156085296004816333892025839072729987354233
    >>> e=1817084480271067137841898198122075168542117135135738925285694555698012943264936112861815937200507849960517390660821911331068907250788900674614345400567411
    >>> m = 7516789928765 # random number
    >>> for dp in range(1000000):
    ...    f = gmpy2.gcd(m-pow(m, e*dp, n), n)
    ...    if f > 1:
    ...        print(dp, f)
    ...        break
    ...
    187261 8275629468590614667884614599278593237258686111405345888268221129814081809682982742676180514534238891248302334619164139839173447495925780801832743975865311
    >>> p = 8275629468590614667884614599278593237258686111405345888268221129814081809682982742676180514534238891248302334619164139839173447495925780801832743975865311
    >>> q = n // p
    >>> p*q == n
    True
    ```

5. In the solution [script](./script.py), I implement the above bruteforce using Python's `multiprocessing` module to run it on multiple threads because we only have 15 minutes. Without multiprocessing, it would take about 1h20m to run completely on my computer.

6. Running the [script](./script.py) produces the following output:

    ```
    [+] Opening connection to mercury.picoctf.net on port 26695: Done
    [*] MD5 PoW string must start with 31950 and hash must end with bdf98c
    [+] Bruteforcing MD5 PoW: MD5 PoW String Found: 319507851758
    [+] Getting public modulus and clue: Success
    [+] Bruteforcing RSA-CRT d_p: p=6755585209747918163868616886189762801438723814293780076178965401337533787532793973718733625630017793302088239336261323736906089254764788312712004326117117, q=13014663099444252202371035556694916836922288463424074950271603159273262042649683760419705683944766998631464971606746251919923961539027359455369007457245187
    [*] Switching to interactive mode
    picoCTF{1_c4n'7_b3l13v3_17'5_n07_f4ul7_4774ck!!!}
    [*] Got EOF while reading in interactive
    ```

### Flag

`picoCTF{1_c4n'7_b3l13v3_17'5_n07_f4ul7_4774ck!!!}`
