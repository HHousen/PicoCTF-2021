# Trivial Flag Transfer Protocol

## Problem

> Figure out how they moved the flag.

## Solution

1. Open the packet capture file in wireshark. Go to File > Export Objects > TFTP.

2. If we preview the `instructions` document we find: `GSGCQBRFAGRAPELCGBHEGENSSVPFBJRZHFGQVFTHVFRBHESYNTGENAFSRE.SVTHERBHGNJNLGBUVQRGURSYNTNAQVJVYYPURPXONPXSBEGURCYNA`. Putting this into [quipqiup](https://www.quipqiup.com/) decodes it to `t ftp doesnt encrypt our traffic so we must disguise our flag transfer figure out away to hide the flag and i will check back for the plan`. The encoding is simply ROT13 so [quipqiup](https://www.quipqiup.com/) is overkill. You can use [cryptii](https://cryptii.com/) instead.

3. The `plan` document says `VHFRQGURCEBTENZNAQUVQVGJVGU-QHRQVYVTRAPR.PURPXBHGGURCUBGBF`, which decodes to `i used the program and hid it with due diligence check out the photos`.

4. Save the `program.deb` file. Let's see if we can use it to decode the images. The `program.deb` is actually `steghide` (this is easily seen if you extract it), so install it if you don't already have it installed with `sudo dpkg -i program.deb`.

5. The hint from the `plan` document suggests that `DUEDILIGENCE` (uppercase because the encoded text is uppercase) is the password.

6. We can use `steghide` on every image included in the packet capture file. The flag is hidden in the last image `picture3.bmp`. So run `steghide extract -sf picture3.bmp -p DUEDILIGENCE` and `cat flag.txt` to get the flag.

### Flag

`picoCTF{h1dd3n_1n_pLa1n_51GHT_18375919}`
