# Very very very Hidden

## Problem

> Finding a flag may take many steps, but if you look diligently it won't be long until you find the light at the end of the tunnel. Just remember, sometimes you find the hidden treasure, but sometimes you find only a hidden map to the treasure. try_me.pcap

* [try_me.pcap](./try_me.pcap)

## Solution

1. Looking at the attached packet capture file we find that most of the traffic uses TLS and thus isn't viewable to us without the proper key. However, there are 5 requests sent over regular HTTP so let's focus on those for now.

2. We can use this filter `(http.request or ssl.handshake.type == 1) and !(udp.port eq 1900)` in wireshark to see initial HTTP and HTTPS traffic. We see that two images are downloaded:

    ```
    GET /NothingSus/duck.png HTTP/1.1
    GET /NothingSus/evil_duck.png HTTP/1.1
    ```

    We can extract these images from the PCAP file by going to File > Export Objects > HTTP and choosing "Save All".

3. The `evil_duck.png` image is much larger than `duck.png` yet appears to be of lower quality indicating that something is hidden inside of it. However, using tools such as `steghide` and `zsteg` reveals nothing.

4. Let's go back to the PCAP file because there is a lot of traffic that we ignored. We can use the same filter as before and then create columns for `Host` and `Server Name` using [this guide](https://book.hacktricks.xyz/forensics/pcaps-analysis/wireshark-tricks#identifying-domains) so we can easily see what websites the user visited. HTTPS hides the content and exact location of the request but it does not hide the server name.

5. The user searches something on Google, goes to `/NonthingSus` on an AWS instance, visits GitHub, goes to docs.microsoft.com, gets the `evil_duck.png` image from the AWS instance, logins in to Micosoft Teams, and finally goes to powershell.org.

6. I tried a lot of searching on GitHub and looking around on the Microsoft documentation (I even found the source of the image in the [Pittsburgh Magazine](https://www.pittsburghmagazine.com/this-giant-rubber-duck-is-coming-to-take-over-the-three-rivers-2/)), but what succeeded was a search for "powershell steganography" which revealed the [peewpw/Invoke-PSImage](https://github.com/peewpw/Invoke-PSImage) GitHub repository. This PowerShell script encodes a different PowerShell script in the pixels of a PNG file. The least significant 4 bits of 2 color values in each pixel are used to hold the payload. While we could write a script to extract this information, I used [PCsXcetra/Decode_PS_Stego](https://github.com/PCsXcetra/Decode_PS_Stego), which I found from the aforementioned search. The executable that [PCsXcetra/Decode_PS_Stego](https://github.com/PCsXcetra/Decode_PS_Stego) provides is in this directory: [PowershellStegoDecode.exe](./PowershellStegoDecode.exe).

7. We can open the `evil_duck.png` image in the [PowershellStegoDecode.exe](./PowershellStegoDecode.exe) program to get the following output:

    ```powershell
    $out = "flag.txt"
    $enc = [system.Text.Encoding]::UTF8
    $string1 = "HEYWherE(IS_tNE)50uP?^DId_YOu(]E@t*mY_3RD()B2g3l?"
    $string2 = "8,:8+14>Fx0l+$*KjVD>[o*.;+1|*[n&2G^201l&,Mv+_'T_B"

    $data1 = $enc.GetBytes($string1)
    $bytes = $enc.GetBytes($string2)

    for($i=0; $i -lt $bytes.count ; $i++)
    {
        $bytes[$i] = $bytes[$i] -bxor $data1[$i]
    }
    [System.IO.File]::WriteAllBytes("$out", $bytes)
    ```

    This script xors the bytes of `string1` with `string2` to get the flag.

8. Pasting this output into PowerShell creates a file called `flag.txt` with the flag in it.

### Flag

`picoCTF{n1c3_job_f1nd1ng_th3_s3cr3t_in_the_im@g3}`
