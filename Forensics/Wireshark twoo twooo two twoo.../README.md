# Wireshark twoo twooo two twoo...

## Problem

> Can you find the flag? shark2.pcapng.

* [shark2.pcapng](./shark2.pcapng)

## Solution

1. Upon initial inspection, there seem to be a lot of requests to a `/flag` endpoint. Each request shows a different flag so these must be a distraction.
2. After searching through the file I noticed many DNS requests for various subdomains of `reddshrimpandherring.com`. This looks like the suspicious traffic that one of the challenge hints refers to.
3. A lot of the DNS queries have a destination of 8.8.8.8. However, a subset have a destination for 18.217.1.57.
4. We can apply the filter `dns and ip.dst==18.217.1.57` to only see DNS requests to this IP address. If we take the subdomains of `reddshrimpandherring.com` and append them in order we get: `cGljb0NURntkbnNfM3hmMWxfZnR3X2RlYWRiZWVmfQ==`
5. Decoding the above string as base64 gives us the flag.
6. Alternatively, this file can be analyzed using [apackets.com](https://apackets.com/). Just upload the file, go to the DNS page, and scroll down to see the requests neatly organized.

### Flag

`picoCTF{dns_3xf1l_ftw_deadbeef}`
