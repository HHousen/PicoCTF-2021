# Weird File

## Problem

> What could go wrong if we let Word documents run programs? (aka "in-the-clear"). Download file.

* [Document](./weird.docm)

## Solution

1. Download the file and open it in Word or LibreOffice. In LibreOffice, go to Tools > Marcos > Edit Macros. Then, on the left, navigate to weird.docm > Project > Document Objects > ThisDocument. Here, you will see the Python program that prints the string `cGljb0NURnttNGNyMHNfcl9kNG5nM3IwdXN9`.
2. Putting the above string into [CyberChef](https://gchq.github.io/CyberChef) and using the magic block produces the flag.

### Flag

`picoCTF{m4cr0s_r_d4ng3r0us}`
