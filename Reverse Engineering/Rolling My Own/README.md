# Rolling My Own

## Problem

> I don't trust password checkers made by other people, so I wrote my own. It doesn't even need to store the password! If you can crack it I'll give you a flag. remote `nc mercury.picoctf.net 23773`

* [remote](./remote)

## Solution

1. Running the program and typing in a password produces an `Illegal instruction (core dumped)`, which is interesting:

    ```
    $ ./remote 
    Password: a
    Illegal instruction (core dumped)
    ```

2. Summary of the paper linked in the hints: [Anti-disassembly using Cryptographic Hash Functions](http://pages.cpsc.ucalgary.ca/~aycock/papers/eicar06-ad.pdf) ([Publisher Link](https://link.springer.com/article/10.1007/s11416-006-0011-3)).

    * The idea for anti-disassembly is to combine a `key` with a "salt" value, and feed the result as input into a cryptographic hash function. A sub-sequence from the output of the hash function between bytes `lb` and `ub` will be interpreted as machine code. This sub-sequence is called a `run`. The salt value is set to ensure that the desired `run` appears in the output of the hash function when the correct key is provided.
    * The task of the analyst is to determine precisely what the code does when executed (the value of `run`) and what the target is (the correct value of `key`).
    * If the wrong `key` value is used, then the `run` is unlikely to consist of useful code. The resistant code could simply try to run it anyway, and possibly crash. This explains the `Illegal instruction (core dumped)` we observe when running the program. It is expecting the correct value of `key` but when provided with the incorrect one it runs the algorithm anyway and thus executes meaningless binary code. What we type in for the password impacts the code that the program executes.
    * An analyst who finds some resistant code has several pieces of information immediately available. The `salt`, the values of `lb` and `ub`, and the `key`'s domain (although not its value) are not hidden.
    * Information hidden from an analyst:
        * The `key`'s value. An analyst may know that a computer virus using this anti-disassembly technique targets someone or something, but would not be able to uncover specifics.
        * The `run`. The analyst knows the `salt` and the domain of the key, so given the `run`, the analyst can find the `key` by exhaustively testing every possible value.

3. We start by decompiling the binary using Ghidra. The main function is below:

    ```c++
    undefined8 FUN_00100b6a(void)

    {
        size_t sVar1;
        void *__ptr;
        undefined8 *puVar2;
        long in_FS_OFFSET;
        int local_100;
        int local_fc;
        int local_e8 [4];
        undefined8 local_d8;
        undefined8 local_d0;
        undefined8 local_c8;
        undefined8 local_c0;
        undefined8 local_b8;
        undefined8 local_b0;
        undefined local_a8;
        char acStack153 [65];
        char local_58 [72];
        long local_10;
        
        local_10 = *(long *)(in_FS_OFFSET + 0x28);
        setbuf(stdout,(char *)0x0);
        local_c8 = 0x57456a4d614c7047;
        local_c0 = 0x6b6d6e6e6a4f5670;
        local_b8 = 0x367064656c694752;
        local_b0 = 0x736c787a6563764d;
        local_a8 = 0;
        local_e8[0] = 8;
        local_e8[1] = 2;
        local_e8[2] = 7;
        local_e8[3] = 1;
        memset(acStack153 + 1,0,0x40);
        memset(local_58,0,0x40);
        printf("Password: ");
        fgets(acStack153 + 1,0x40,stdin);
        sVar1 = strlen(acStack153 + 1);
        acStack153[sVar1] = '\0';
        local_100 = 0;
        while (local_100 < 4) {
            strncat(local_58,acStack153 + (long)(local_100 << 2) + 1,4);
            strncat(local_58,(char *)((long)&local_c8 + (long)(local_100 << 3)),8);
            local_100 = local_100 + 1;
        }
        __ptr = malloc(0x40);
        sVar1 = strlen(local_58);
        FUN_00100e3e(__ptr,local_58,sVar1 & 0xffffffff);
        local_100 = 0;
        while (local_100 < 4) {
            local_fc = 0;
            while (local_fc < 4) {
            *(undefined *)((long)&local_d8 + (long)(local_fc * 4 + local_100)) =
                *(undefined *)((long)__ptr + (long)(local_e8[local_fc] + local_fc * 0x10 + local_100));
            local_fc = local_fc + 1;
            }
            local_100 = local_100 + 1;
        }
        puVar2 = (undefined8 *)mmap((void *)0x0,0x10,7,0x22,-1,0);
        *puVar2 = local_d8;
        puVar2[1] = local_d0;
        (*(code *)puVar2)(FUN_0010102b);
        free(__ptr);
        if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                            /* WARNING: Subroutine does not return */
            __stack_chk_fail();
        }
        return 0;
    }
    ```

    This function takes our input password and saves it to `acStack153`. Then it runs a loop 4 times to create `local_58` by appending chunks of the user input password and using `strncat`. Each iteration, it appends 4 bytes of the password and then 8 bytes of the `salt`. Ghirda did not decompile the `salt` clearly. `local_c8`, `local_c0`, `local_b8`, and `local_b0` are the 4 components of the `salt` and each one is 8 bytes. The loop index variable, `local_100` is bit shifted to the left by 3 (`local_100 << 3`) which moves the pointer to the next chunk of the `salt` each iteration.

4. The string created from the aforementioned loop (`local_58` becomes `param_2`) is passed to `FUN_00100e3e`, which is shown below:

    ```c++
    void FUN_00100e3e(long param_1,void *param_2,int param_3)

    {
        int iVar1;
        uint uVar2;
        int iVar3;
        long in_FS_OFFSET;
        void *local_a8;
        int local_98;
        int local_94;
        int local_90;
        MD5_CTX local_88;
        uchar local_28 [24];
        long local_10;
        
        local_10 = *(long *)(in_FS_OFFSET + 0x28);
        if (param_3 % 0xc == 0) {
            iVar1 = param_3 / 0xc;
        }
        else {
            iVar1 = param_3 / 0xc + 1;
        }
        local_98 = 0;
        local_a8 = param_2;
        while (local_98 < iVar1) {
            local_90 = 0xc;
            if ((local_98 == iVar1 + -1) && (param_3 % 0xc != 0)) {
            local_90 = iVar1 % 0xc;
            }
            MD5_Init(&local_88);
            MD5_Update(&local_88,local_a8,(long)local_90);
            local_a8 = (void *)((long)local_a8 + (long)local_90);
            MD5_Final(local_28,&local_88);
            local_94 = 0;
            while (local_94 < 0x10) {
            iVar3 = local_98 * 0x10 + local_94;
            uVar2 = (uint)(iVar3 >> 0x1f) >> 0x1a;
            *(uchar *)((int)((iVar3 + uVar2 & 0x3f) - uVar2) + param_1) = local_28[local_94];
            local_94 = local_94 + 1;
            }
            local_98 = local_98 + 1;
        }
        if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                            /* WARNING: Subroutine does not return */
            __stack_chk_fail();
        }
        return;
    }
    ```

    In short, this function takes the string computed in the previous step, splits it into four 12 byte chunks, computes the MD5 hash of each chunk, and stores the hashes.

5. Now, back in the `main` function, the program takes 4 bytes from each of the hashes starting at indexes 8, 2, 7, and 1, which are stored in `local_e8`. For example, the program extracts the 4 bytes starting at byte 8 from the first hash. These sequences are combined to create 16 bytes of shellcode. The shellcode is called with the address of `FUN_0010102b` as an argument, which means the `rdi` assembly register is set to the address of `FUN_0010102b`.

6. `FUN_0010102b` is the function that prints the flag:

    ```c++
    void FUN_0010102b(long param_1)

    {
        FILE *__stream;
        long in_FS_OFFSET;
        char local_98 [136];
        long local_10;
        
        local_10 = *(long *)(in_FS_OFFSET + 0x28);
        if (param_1 == 0x7b3dc26f1) {
            __stream = fopen("flag","r");
            if (__stream == (FILE *)0x0) {
            puts("Flag file not found. Contact an admin.");
                            /* WARNING: Subroutine does not return */
            exit(1);
            }
            fgets(local_98,0x80,__stream);
            puts(local_98);
        }
        else {
            puts("Hmmmmmm... not quite");
        }
        if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                            /* WARNING: Subroutine does not return */
            __stack_chk_fail();
        }
        return;
    }
    ```

    This function will print the flag if it receives `0x7b3dc26f1` as an argument (if the `rdi` assembly register is `0x7b3dc26f1`).

7. So, we can determine the value of `run` as defined in [the paper](http://pages.cpsc.ucalgary.ca/~aycock/papers/eicar06-ad.pdf). The value of `run` is the same as the shellcode. The shellcode has to call the function at `rdi`, which is the function to print the flag, while setting the `rdi` to `0x7b3dc26f1`, since the flag printing function checks for this argument, all while being exactly 16 bytes.

8. There is a hint that tells us that the password starts with `D1v1`, so we can determine the first 4 bytes. Let's manually apply the program. First, we append `GpLaMjEW`, which is the reversed (because of little endian) ascii value of `0x57456a4d614c7047`, to get `D1v1GpLaMjEW`. Next, we [calculate the MD5 hash of `D1v1GpLaMjEW`](https://gchq.github.io/CyberChef/#recipe=MD5()&input=RDF2MUdwTGFNakVX) and get `23f144e08b603e724889fe489f78fa53`. The actual shellcode is `4889fe48` because of the indexes discussed in step 5. The first index is 8 so we go to byte 8 and copy the next 4 bytes. You can use an [online disassembler](http://shell-storm.org/online/Online-Assembler-and-Disassembler/?opcodes=%5Cx48%5Cx89%5Cxfe%5Cx48&arch=x86-64&endianness=little&dis_with_addr=True&dis_with_raw=True&dis_with_ins=True#disassembly) or `ndisasm` (`echo -ne "\x48\x89\xFE\x48" | ndisasm -b64 -`, [more info](https://stackoverflow.com/a/44783138)) to convert this shellcode to assembly. The assembly is:

    ```assembly
    48 89 FE    mov rsi, rdi
    48          mov?
    ```

9. Since we know what the shellcode is supposed to do we can predict that the shellcode in assembly is probably:

    ```assembly
    48 89 FE                mov    rsi, rdi
    48 BF F1 26 DC B3 07    movabs rdi, 0x7b3dc26f1
    00 00 00 
    ff D6                   call   rsi
    C3                      ret
    ```

10. We can use the `asm` from `pwntools` to compile the assembly to shellcode: `python -c "from pwn import asm; print(asm('mov rsi, rdi; movabs rdi, 0x7b3dc26f1; call rsi; ret', arch='amd64'))"`. This command will output `H\x89\xfeH\xbf\xf1&\xdc\xb3\x07\x00\x00\x00\xff\xd6\xc3`, which we can manually convert to raw bytes to get `\x48\x89\xfe\x48\xbf\xf1\x26\xdc\xb3\x07\x00\x00\x00\xff\xd6\xc3`.

11. Now, we known the `run` and just need to figure out the `key` to get the flag. We can do this by bruteforcing the chunks of the `key`/password until we get MD5 hashes where the corresponding bytes match the bytes in the shellcode. In step 3, an intermediate form of the data is created by appending chunks of the user input password and the salt. In step 4, this intermediate form is split into 4 chunks and the md5 hash of each chunk is calculated. So, the first 4 bytes/characters of each of the 4 sections of the intermediate form are the `key`. In step 5, the sections of 4 bytes are extracted from the hashes at various offsets (8, 2, 7, and 1). We know what 4 bytes should be present at the offsets in each of these 4 hashes. Thus, we can conduct an MD5 bruteforce. This is better explained graphically, where `?` is a character of the key and `__` is a byte that doesn't matter:

    ```python
    MD5("????GpLaMjEW") = [__, __, __, __, __, __, __, __, 48, 89, FE, 48, __, __, __, __]
    MD5("????pVOjnnmk") = [__, __, BF, F1, 26, DC, __, __, __, __, __, __, __, __, __, __]
    MD5("????RGiledp6") = [__, __, __, __, __, __, __, B3, 07, 00, 00, __, __, __, __, __]
    MD5("????Mvcezxls") = [__, 00, FF, D6, C3, __, __, __, __, __, __, __, __, __, __, __]
    ```

    The salt values being hashed were taken from the decompiled `main` function, [converted from hexadecimal to ascii, and then reversed](https://gchq.github.io/CyberChef/#recipe=From_Hex('0x')Reverse('Character')&input=MHg2YjZkNmU2ZTZhNGY1Njcw) (because of little endian). We already know the `????` for the first segment because of the hint: `D1v1`.

12. We can write a Python [script](./script.py) to bruteforce these 3 unknown segments of the password using the corresponding known sections of the hash. Running the [script](./script.py) will print the password: `D1v1d3AndC0nqu3r`.

13. Finally, connect to the service with `nc mercury.picoctf.net 23773` and enter the password `D1v1d3AndC0nqu3r` to get the flag.

### Flag

`picoCTF{r011ing_y0ur_0wn_crypt0_15_h4rd!_3c22f4e9}`
