# Milkslap

## Problem

> [🥛](http://mercury.picoctf.net:16940/)

## Solution

1. When we view the source of the website, we can look at the stylesheet at `/style.css`, and see that it loads an image from `concat_v.png`. Let's download this image.

2. Since this image is a PNG, we can use a steganography tool called `zsteg` like so: `zsteg concat_v.png`

    `zsteg concat_v.png` output:

    ```
    imagedata           .. text: "\n\n\n\n\n\n\t\t"
    b1,b,lsb,xy         .. text: "picoCTF{imag3_m4n1pul4t10n_sl4p5}\n"
    b1,bgr,lsb,xy       .. <wbStego size=9706075, data="\xB6\xAD\xB6}\xDB\xB2lR\x7F\xDF\x86\xB7c\xFC\xFF\xBF\x02Zr\x8E\xE2Z\x12\xD8q\xE5&MJ-X:\xB5\xBF\xF7\x7F\xDB\xDFI\bm\xDB\xDB\x80m\x00\x00\x00\xB6m\xDB\xDB\xB6\x00\x00\x00\xB6\xB6\x00m\xDB\x12\x12m\xDB\xDB\x00\x00\x00\x00\x00\xB6m\xDB\x00\xB6\x00\x00\x00\xDB\xB6mm\xDB\xB6\xB6\x00\x00\x00\x00\x00m\xDB", even=true, mix=true, controlbyte="[">                                                                                 
    b2,r,lsb,xy         .. file: SoftQuad DESC or font file binary
    b2,r,msb,xy         .. file: VISX image file
    b2,g,lsb,xy         .. file: VISX image file
    b2,g,msb,xy         .. file: SoftQuad DESC or font file binary - version 15722
    b2,b,msb,xy         .. text: "UfUUUU@UUU"
    b4,r,lsb,xy         .. text: "\"\"\"\"\"#4D"
    b4,r,msb,xy         .. text: "wwww3333"
    b4,g,lsb,xy         .. text: "wewwwwvUS"
    b4,g,msb,xy         .. text: "\"\"\"\"DDDD"
    b4,b,lsb,xy         .. text: "vdUeVwweDFw"
    b4,b,msb,xy         .. text: "UUYYUUUUUUUU"
    ```

    As you can see, the flag is shown in the output.

3. More information about different steganography tools can be found on [HackTricks Stego Tricks](https://book.hacktricks.xyz/stego/stego-tricks)

### Flag

`picoCTF{imag3_m4n1pul4t10n_sl4p5}`
