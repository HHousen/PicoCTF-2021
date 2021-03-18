# Disk, disk, sleuth!

## Problem

> Use `srch_strings` from the sleuthkit and some terminal-fu to find a flag in this disk image: dds1-alpine.flag.img.gz

* [dds1-alpine.flag.img.gz](https://mercury.picoctf.net/static/4f3df7052b4121aff89af1a3f517afb1/dds1-alpine.flag.img.gz)

## Solution

1. Extract the disk by running `gunzip dds1-alpine.flag.img.gz`.

2. Make sure `autopsy` is installed (`sudo apt install autopsy`).

3. Use the `srch_strings` command as suggested by the challenge and then search for `picoCTF`: `srch_strings dds1-alpine.flag.img | grep picoCTF`

### Flag

`picoCTF{f0r3ns1c4t0r_n30phyt3_a011c142}`
