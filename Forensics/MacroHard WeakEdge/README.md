# MacroHard WeakEdge

## Problem

> I've hidden a flag in this file. Can you find it? Forensics is fun.pptm

* [Forensics is fun.pptm](./Forensics%20is%20fun.pptm)

## Solution

1. Extract the PowerPoint presentation as a ZIP file, since PowerPoint files are actually ZIPs: `unzip Forensics\ is\ fun.pptm`

2. Looking through the extracted files, `ppt/slideMasters/hidden` looks suspicious.

3. Reading that file (`cat ppt/slideMasters/hidden`) shows `Z m x h Z z o g c G l j b 0 N U R n t E M W R f d V 9 r b j B 3 X 3 B w d H N f c l 9 6 M X A 1 f Q`.

4. We can decode that as base64 using [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true)&input=WiBtIHggaCBaIHogbyBnIGMgRyBsIGogYiAwIE4gVSBSIG4gdCBFIE0gVyBSIGYgZCBWIDkgciBiIGogQiAzIFggMyBCIHcgZCBIIE4gZiBjIGwgOSA2IE0gWCBBIDEgZiBR) to get the flag.

### Flag

`picoCTF{D1d_u_kn0w_ppts_r_z1p5}`
