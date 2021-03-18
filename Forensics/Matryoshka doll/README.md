# Matryoshka doll

## Problem

> Matryoshka dolls are a set of wooden dolls of decreasing size placed one inside another. What's the final one? Image: this

* [Image](./dolls.jpg)

## Solution

1. The problem suggests files places inside of other files, so let's run `binwalk dolls.jpg`.

    ```
    DECIMAL       HEXADECIMAL     DESCRIPTION
    --------------------------------------------------------------------------------
    0             0x0             PNG image, 594 x 1104, 8-bit/color RGBA, non-interlaced
    3226          0xC9A           TIFF image data, big-endian, offset of first image directory: 8
    272492        0x4286C         Zip archive data, at least v2.0 to extract, compressed size: 378956, uncompressed size: 383938, name: base_images/2_c.jpg
    651614        0x9F15E         End of Zip archive, footer length: 22
    ```

    Sure enough, there are several files.

2. We can extract the files by running `binwalk --dd='.*' dolls.jpg` and then `cd _dolls.jpg.extracted`.

3. After some trial and error, the correct solution is to extract the zip file, `cd base_images`, and then repeat step 3 on `2_c.jpg`.

4. Now that you are in `_2_c.jpg.extracted`, extract the zip file and repeat step 3.

5. Repeat the above steps of extracting and `binwalk`ing until you end up at this path: `_dolls.jpg.extracted/base_images/_2_c.jpg.extracted/base_images/_3_c.jpg.extracted/base_images/_4_c.jpg.extracted/136DA-(1)`. There is a `flag.txt` file in this directory that contains the flag.

### Flag

`picoCTF{336cf6d51c9d9774fd37196c1d7320ff}`
