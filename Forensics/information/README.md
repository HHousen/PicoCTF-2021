# information

## Problem

> Files can always be changed in a secret way. Can you find the flag? cat.jpg

* [cat.jpg](./vuln)
* [Source](./vuln.c)

## Solution

1. Download the image and use `exiftool cat.jpg`. The license field looks suspicious:

    ```
    ExifTool Version Number         : 12.16
    File Name                       : cat.jpg
    Directory                       : .
    File Size                       : 858 KiB
    File Modification Date/Time     : 2021:03:15 14:24:46-04:00
    File Access Date/Time           : 2021:03:16 15:08:38-04:00
    File Inode Change Date/Time     : 2021:03:16 15:08:32-04:00
    File Permissions                : rw-r--r--
    File Type                       : JPEG
    File Type Extension             : jpg
    MIME Type                       : image/jpeg
    JFIF Version                    : 1.02
    Resolution Unit                 : None
    X Resolution                    : 1
    Y Resolution                    : 1
    Current IPTC Digest             : 7a78f3d9cfb1ce42ab5a3aa30573d617
    Copyright Notice                : PicoCTF
    Application Record Version      : 4
    XMP Toolkit                     : Image::ExifTool 10.80
    License                         : cGljb0NURnt0aGVfbTN0YWRhdGFfMXNfbW9kaWZpZWR9
    Rights                          : PicoCTF
    Image Width                     : 2560
    Image Height                    : 1598
    Encoding Process                : Baseline DCT, Huffman coding
    Bits Per Sample                 : 8
    Color Components                : 3
    Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
    Image Size                      : 2560x1598
    Megapixels                      : 4.1
    ```

2. We can decode this string using [CyberChef](https://gchq.github.io/CyberChef/). Paste in the string and drag in the magic block into the recipe.

### Flag

`picoCTF{the_m3tadata_1s_modified}`
