# gogo

## Problem

> Hmmm this is a weird file... enter_password. There is a instance of the service running at `mercury.picoctf.net:48728`.

* [enter_password](./enter_password)

## Solution

1. We can decompile the program using Ghidra and check out the `main` functions. There is a `checkPassword` function, which is shown below:

    ```c++
    void main.checkPassword(int param_1,uint param_2,undefined param_3)

    {
        uint *puVar1;
        uint uVar2;
        int iVar3;
        int *in_GS_OFFSET;
        undefined4 local_40;
        undefined4 local_3c;
        undefined4 local_38;
        undefined4 local_34;
        undefined4 local_30;
        undefined4 local_2c;
        undefined4 local_28;
        undefined4 local_24;
        byte local_20 [28];
        undefined4 uStack4;
        
        puVar1 = (uint *)(*(int *)(*in_GS_OFFSET + -4) + 8);
        if (register0x00000010 < (undefined *)*puVar1 ||
            (undefined *)register0x00000010 == (undefined *)*puVar1) {
            uStack4 = 0x80d4b72;
            runtime.morestack_noctxt();
            main.checkPassword();
            return;
        }
        if ((int)param_2 < 0x20) {
            os.Exit(0);
        }
        FUN_08090b18();
        local_40 = 0x38313638;
        local_3c = 0x31663633;
        local_38 = 0x64336533;
        local_34 = 0x64373236;
        local_30 = 0x37336166;
        local_2c = 0x62646235;
        local_28 = 0x39383338;
        local_24 = 0x65343132;
        FUN_08090fe0();
        uVar2 = 0;
        iVar3 = 0;
        while( true ) {
            if (0x1f < (int)uVar2) {
                if (iVar3 == 0x20) {
                    return;
                }
                return;
            }
            if ((param_2 <= uVar2) || (0x1f < uVar2)) break;
            if ((*(byte *)(param_1 + uVar2) ^ *(byte *)((int)&local_40 + uVar2)) == local_20[uVar2]) {
                iVar3 = iVar3 + 1;
            }
            uVar2 = uVar2 + 1;
        }
        runtime.panicindex();
        do {
            invalidInstructionException();
        } while( true );
    }
    ```

2. The `checkPassword` function runs a loop that XORs two characters and compares the result to another variable. The loop in assembly is shown below:

    ```assembly
    080d4b18 0f b6 2c 01     MOVZX      EBP,byte ptr [ECX + EAX*0x1]
    080d4b1c 83 f8 20        CMP        EAX,0x20
    080d4b1f 73 45           JNC        LAB_080d4b66
    080d4b21 0f b6 74        MOVZX      ESI,byte ptr [ESP + EAX*0x1 + 0x4]
                04 04
    080d4b26 31 f5           XOR        EBP,ESI
    080d4b28 0f b6 74        MOVZX      ESI,byte ptr [ESP + EAX*0x1 + 0x24]
                04 24
    080d4b2d 95              XCHG       EAX,EBP
    080d4b2e 87 de           XCHG       ESI,EBX
    080d4b30 38 d8           CMP        AL,BL
    ```

3. We can use GDB and set a breakpoint at `0x080d4b28` so we have access to the values that our input is XORed with and the values that the result of the XOR operation is compared with.

4. We launch the program in gdb with `gdb ./enter_password` and create the breakpoint with `b* 0x080d4b28`. We run the program with `r` and enter 32 `a`s since the decompiled code shows that the loop runs `0x20` times. You can generate a string of 32 `a`s for copy-pasting by running `python -c "print('a'*32)"`. According to the disassembly, our input should be at `$ecx`. If we run `x /32 $ecx`, sure enough we see our input:

    ```
    0x18414320:     0x61    0x61    0x61    0x61    0x61    0x61    0x61    0x61
    0x18414328:     0x61    0x61    0x61    0x61    0x61    0x61    0x61    0x61
    0x18414330:     0x61    0x61    0x61    0x61    0x61    0x61    0x61    0x61
    0x18414338:     0x61    0x61    0x61    0x61    0x61    0x61    0x61    0x61
    ```

5. The values that our input is XORed with are at `$esp+0x4` and the expected values are at `$esp+0x24`:

    ```
    (gdb) x /32 $esp+0x4
    0x18449f28:     0x38    0x36    0x31    0x38    0x33    0x36    0x66    0x31
    0x18449f30:     0x33    0x65    0x33    0x64    0x36    0x32    0x37    0x64
    0x18449f38:     0x66    0x61    0x33    0x37    0x35    0x62    0x64    0x62
    0x18449f40:     0x38    0x33    0x38    0x39    0x32    0x31    0x34    0x65
    (gdb) x /32 $esp+0x24
    0x18449f48:     0x4a    0x53    0x47    0x5d    0x41    0x45    0x03    0x54
    0x18449f50:     0x5d    0x02    0x5a    0x0a    0x53    0x57    0x45    0x0d
    0x18449f58:     0x05    0x00    0x5d    0x55    0x54    0x10    0x01    0x0e
    0x18449f60:     0x41    0x55    0x57    0x4b    0x45    0x50    0x46    0x01
    ```

6. Now, we can XOR these two values to get the input because if `x ^ y = z` then `y ^ z = x`,  where `x` is the input (`$ecx`), `y` are the values that the input is XORed with (`$esp+0x4`), and `x` are the expected values (`$esp+0x24`). We can use [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Hex('None')XOR(%7B'option':'Hex','string':'4a53475d414503545d025a0a5357450d05005d555410010e4155574b45504601'%7D,'Standard',true)&input=MzgzNjMxMzgzMzM2NjYzMTMzNjUzMzY0MzYzMjM3NjQ2NjYxMzMzNzM1NjI2NDYyMzgzMzM4MzkzMjMxMzQ2NQ) to compute the XOR between `3836313833366631336533643632376466613337356264623833383932313465` and `4a53475d414503545d025a0a5357450d05005d555410010e4155574b45504601` to get `reverseengineericanbarelyforward` as the output.

7. Let's run the program normally with `./enter_password` and enter `reverseengineericanbarelyforward` for the password:

    ```
    Enter Password: reverseengineericanbarelyforward
    =========================================
    This challenge is interrupted by psociety
    What is the unhashed key?
    ```

8. We need an unhashed key. The value that the input is XORed with at `$esp+0x4` converted from hex to ascii looks like a hash: `861836f13e3d627dfa375bdb8389214e`. I noticed this while building the CyberChef recipe for decoding the password. If we paste this into [CrackStation](https://crackstation.net/) we find that it is the md5 hash for `goldfish`. If we enter the password and then type in `goldfish` for the unhashed key, the program will read the `flag.txt` file.

9. Connect to the web service with `nc mercury.picoctf.net 48728`, send `reverseengineericanbarelyforward` for the password and `goldfish` for the unhashed key to get the flag:

    ```
    Enter Password: reverseengineericanbarelyforward
    =========================================
    This challenge is interrupted by psociety
    What is the unhashed key?
    goldfish
    Flag is:  picoCTF{p1kap1ka_p1c0b187f1db}
    ```

### Flag

`picoCTF{p1kap1ka_p1c0b187f1db}`
