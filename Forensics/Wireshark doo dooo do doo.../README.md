# Wireshark doo dooo do doo...

## Problem

> Can you find the flag? shark1.pcapng.

* [shark1.pcapng](./shark1.pcapng)

## Solution

1. Open the file in wireshark and type in `tcp.stream eq 5` to get the 5th TCP stream.

2. Right click any entry, click follow, and then click "TCP Stream."

3. The flag will now be shown, but it is encoded: `Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}`

4. We can decode the flag by passing it through ROT13 since this is a basic Caesar's cipher. You can decode ROT13 using [CyberChef (click for recipe with input)](https://gchq.github.io/CyberChef/#recipe=ROT13(true,true,false,13)&input=R3VyIHN5bnQgdmYgY3ZwYlBHU3tjMzN4bm8wMF8xX2YzM19oX3FybnFvcnJzfQ), for instance.

### Flag

`picoCTF{p33kab00_1_s33_u_deadbeef}`
