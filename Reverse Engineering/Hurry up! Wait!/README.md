# Hurry up! Wait!

## Problem

> svchost.exe

* [svchost.exe](./svchost.exe)

## Solution

1. First, I decompiled the binary using Ghidra. I then clicked though all of the functions until I came across this:

    ```c++
    void FUN_0010298a(void)

    {
        ada__calendar__delays__delay_for(1000000000000000);
        FUN_00102616();
        FUN_001024aa();
        FUN_00102372();
        FUN_001025e2();
        FUN_00102852();
        FUN_00102886();
        FUN_001028ba();
        FUN_00102922();
        FUN_001023a6();
        FUN_00102136();
        FUN_00102206();
        FUN_0010230a();
        FUN_00102206();
        FUN_0010257a();
        FUN_001028ee();
        FUN_0010240e();
        FUN_001026e6();
        FUN_00102782();
        FUN_001028ee();
        FUN_001023da();
        FUN_0010230a();
        FUN_0010233e();
        FUN_0010226e();
        FUN_001022a2();
        FUN_001023da();
        FUN_001021d2();
        FUN_00102956();
        return;
    }
    ```

2. The first function that `FUN_0010298a` calls is `ada__calendar__delays__delay_for`, which seems to create a long delay that prevents us from being able to simply run the program. However, the next functions that are called all look basically the same:

    ```c++
    void FUN_00102616(void)

    {
        ada__text_io__put__4(&DAT_00102cd8,&DAT_00102cb8,&DAT_00102cb8,&DAT_00102cd8);
        return;
    }


    void FUN_001024aa(void)

    {
        ada__text_io__put__4(&DAT_00102cd1,&DAT_00102cb8,&DAT_00102cb8,&DAT_00102cd1);
        return;
    }


    void FUN_00102372(void)

    {
        ada__text_io__put__4(&DAT_00102ccb,&DAT_00102cb8,&DAT_00102cb8,&DAT_00102ccb);
        return;
    }
    ```

3. Each function calls `ada__text_io__put__4`, but with different arguments. The first and last arguments differ each time `ada__text_io__put__4` is invoked, but they are equal within each call.

4. Double click on `DAT_00102cd8` in `FUN_00102616` to see that it is `p`. The next global value, `DAT_00102cd1`, in `FUN_001024aa` is `i`. `DAT_00102ccb` (from `FUN_00102372`) is `c` and `DAT_00102cd7` (from `FUN_001025e2`) is `o`. So, it seems that each function prints a character of the flag where each character is stored as a global variable.

5. We can double-click through each function (and go back to the calling function using the back button in Ghidra) to get the flag or a Ghidra script could be written to extract the flag, but it is faster to manually extract it.

### Flag

`picoCTF{d15a5m_ftw_eab78e4}`
