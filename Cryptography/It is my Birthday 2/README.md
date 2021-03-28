# It is my Birthday 2

## Problem

> My birthday is coming up again, but I want to have a very exclusive party for only the best cryptologists. See if you can solve my challenge, upload 2 valid PDFs that are different but have the same SHA1 hash. They should both have the same 1000 bytes at the end as the original invite. <http://mercury.picoctf.net:21110/> invite.pdf

* [invite.pdf](invite.pdf)

## Solution

1. This challenge initially seems extremely difficult if not impossible. The SHAttered collision took the equivalent of 6,500 years of single-CPU computations and 110 years of single-GPU computations for a total cost of approximately $100,000! And this challenge wants us to create our own SHA-1 collision!?!

2. Looking around online does show that people have [reduced the cost and complexity](https://en.wikipedia.org/wiki/SHA-1#Attacks) of this attack... but all of the current methods still cost tens of thousands of dollars.

3. The following summary is adapted from [cs-ahmed/Hands-on-SHA1-Collisions-Using-sha1collider](https://github.com/cs-ahmed/Hands-on-SHA1-Collisions-Using-sha1collider). SHAttered (by Stevens et al.) was the first ever practical and public SHA-1 collision between two PDF files. The type of collision they created was a fixed-prefix collision: A collision created by having identical starts of files, followed by distinct, slight differences in a small amount of the files, which is where the collision appears. After the collision is created, all that follows in both files (i.e. the suffixes of the files) must be identical. However, their collision was strategically placed to take advantage of a special property of the JPEG images in the PDFs: JPEG comments. Essentially, both files have the image data embedded inside, they just start displaying the image at at different byte depending on the value of a JPEG comment.

4. The two PDFs that Google created as part of SHAttered are publically available on the [SHAttered website](https://shattered.io/): [PDF 1](https://shattered.io/static/shattered-1.pdf) / [PDF 2](https://shattered.io/static/shattered-2.pdf). However, these files will not meet the criteria for the challenge because they do not have the same 1000 bytes at the end as the [original invite](invite.pdf). So, lets get the last 1000 bytes from the [original invite](invite.pdf) and append them to both of the SHAttered PDFs.

5. We can get the last 1000 bytes of the [original invite](invite.pdf) using `tail -c 1000 invite.pdf > invite-bytes`. Next, we run a simply Python [script](./script.py) to append these bytes to both SHAttered PDFs: `python script.py solve-1.pdf solve-2.pdf` (where `solve-2.pdf` and `solve-2.pdf` are the two SHAttered PDFs). Uploading these PDFs to the website gives the flag. These final output PDFs are in the same directory as this file: [solve-1.pdf](./solve-1.pdf) / [solve-2.pdf](./solve-2.pdf)

6. Initially, I thought simply appending the bytes wouldn't work because it would make the PDF invalid. However, this is not the case. I'm not entirely sure why, but it probably has to do with the `EOF` bytes at the end of the PDF. The PDF reader might just ignore the appended bytes when determining if the PDF is valid.

7. PDFs with arbitrary content and be SHA-1 collided using [nneonneo/sha1collider](https://github.com/nneonneo/sha1collider). Essentially, the image in the SHAttered PDFs can be replaced with any other image to generate two PDFs with different content but identical SHA-1 hashes.

8. Another way to solve this problem would be using a tool like [nneonneo/sha1collider](https://github.com/nneonneo/sha1collider) to create a collision involving the actual content from the [original invite](invite.pdf). We can use a hex editor, such as [HexEd.it](https://hexed.it/), to create a slightly different version of the invite called `invite2.pdf`. Then, we can run `./collide.py invite.pdf invite2.pdf` and finally append the last 1000 bytes of the original invite with `python script.py out-invite.pdf out-invite2.pdf`. These final output PDFs are also in this directory: [out-invite.pdf](./out-invite.pdf) / [out-invite2.pdf](./out-invite2.pdf)

### Flag

`picoCTF{h4ppy_b1rthd4y_2_m3_6d84abf6}`
