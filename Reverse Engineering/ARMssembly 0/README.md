# ARMssembly 0

## Problem

> What integer does this program print with arguments 182476535 and 3742084308? File: chall.S Flag format: picoCTF{XXXXXXXX} -> (hex, lowercase, no 0x, and 32 bits. ex. 5614267 would be picoCTF{0055aabb})

* [Source](./chall.S)

## Solution

1. We could either solve this challenge by manually reading the assembly and figuring out what it does or we could compile the assembly and run it. If you understand ARM assembly, reading it is probably easier than compiling and running it, but I don't have a good understanding of assembly so I'm going to compile it.

2. The following resources are useful to learn about how ARM assembly works:

    * [ARM Instruction Set Tutorial](https://azeria-labs.com/arm-instruction-set-part-3/)
    * [Arm Architecture Reference Manual](https://developer.arm.com/documentation/ddi0487/latest)

3. To learn how to cross compile ARM assembly on x86, which is what we will be doing, the following resources are helpful:

    * [Running Arm Binaries on x86 with QEMU-User](https://azeria-labs.com/arm-on-x86-qemu-user/)
    * [Running ARMv8 via Linux Command Line](https://github.com/joebobmiles/ARMv8ViaLinuxCommandline)

4. To compile ARMv8 as ARMv8 on a non-ARMv8 machine, we need a cross compiler. Thankfully, the GNU project has a suite of cross compiler tools that we can use for ARMv8. To install on Ubuntu (or other Debian based systems), run: `sudo apt install binutils-aarch64-linux-gnu`

5. Using the above two guides, we can run the following commands to cross compile the challenge ARM assembly code.

    ```
    aarch64-linux-gnu-as -o chall.o chall.S
    aarch64-linux-gnu-gcc -static -o chall chall.o
    ```

6. Now that we have the binary, we can use `file` to see that it is compiled for `ARM aarch64`. However, x86_64 systems cannot run this code so we need to emulate it. We can install a version of QEMU that runs statically in the background with `sudo apt install qemu-user-static` so we can run ARM binaries like normal programs.

7. Finally, we can run the challenge binary with the two provided arguments: `./chall 182476535 3742084308` to get the answer: `Result: 3742084308`.

8. The flag format expects the answer to be in hexadecimal, so we can use [RapidTables](https://www.rapidtables.com/convert/number/decimal-to-hex.html?x=3742084308) to convert our decimal result to the hexadecimal flag.

### Flag

`picoCTF{df0bacd4}`
