# Let's get dynamic

## Problem

> Can you tell what this file is reading? chall.S

* [chall.S](./chall.S)

## Solution

1. First, compile the program: `gcc -g chall.S -o chall`. The `-g` flag compiles with debugging symbols.

2. If we run the program and enter some text, we get `Correct! You entered the flag.`, which doesn't seem correct.

3. I decompiled the `chall` binary using Ghidra to look at a c representation. There is a `memcmp` instruction which looks like it compares our input to the flag.

4. We can run the binary in gdb with `gdb chall` to debug it. I placed a breakpoint at the `memcmp` statement with `b memcmp` and then ran the program with `r`. We reach the breakpoint and now we can look at the source index and destination index registers, which are `rsi` and `rdi` respectively. We can view the source index as a string like so: `printf "%s\n", $rsi`, which prints the flag.

5. GDB output:

    ```
    $ gdb chall
    Reading symbols from chall...
    (gdb) b memcmp
    Breakpoint 1 at 0x1060
    (gdb) r
    Starting program: ./chall 
    a

    Breakpoint 1, __memcmp_avx2_movbe () at ../sysdeps/x86_64/multiarch/memcmp-avx2-movbe.S:59
    59      ../sysdeps/x86_64/multiarch/memcmp-avx2-movbe.S: No such file or directory.
    (gdb) printf "%s\n", $rsi
    picoCTF{dyn4m1c_4n4ly1s_1s_5up3r_us3ful_14bfa700}
    ```

### Flag

`picoCTF{dyn4m1c_4n4ly1s_1s_5up3r_us3ful_14bfa700}`
