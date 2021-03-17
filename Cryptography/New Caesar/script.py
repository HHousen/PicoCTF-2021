import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

cipher_text = "kjlijdliljhdjdhfkfkhhjkkhhkihlhnhghekfhmhjhkhfhekfkkkjkghghjhlhghmhhhfkikfkfhm"

def b16_decode(solve):
    dec = ""
    for idx in range(0, len(solve), 2):
        # Get the current and next letters so we can create the one letter that
        # was split in half by `b16_encode`.
        c1 = solve[idx]
        c2 = solve[idx + 1]
        # Determine the location of these letters in the alphabet. The coresponds to
        # the code inside the square brackets `ALPHABET[int(binary[:4], 2)]` from
        # `b16_encode`.
        c1 = ALPHABET.index(c1)
        c2 = ALPHABET.index(c2)
        # Convert the numbers to binary
        binary1 = "{0:04b}".format(c1)
        binary2 = "{0:04b}".format(c2)
        # Add the two binary strings together to recover the encoded character
        binary = int(binary1 + binary2, 2)

        dec += chr(binary)
    return dec

def unshift(c, k):
    # Offset the letters in the opposite direction.
    t1 = ord(c) + LOWERCASE_OFFSET
    t2 = ord(k) + LOWERCASE_OFFSET
    # Instead of moving forward through the alphabet, move backwards.
    return ALPHABET[(t1 - t2) % len(ALPHABET)]

def is_ascii(s):
    return len(s) == len(s.encode())

# Try every possible offset to see what key produces the flag.
for letter in ALPHABET:
    # `letter` is the key
    dec = ""
    # Apply the opposite of the `shift` function on each letter.
    for i, c in enumerate(cipher_text):
        dec += unshift(c, letter)
    # Reverse the `b16_encode` function.
    dec = b16_decode(dec)
    # Only show potential flags that are ascii.
    if is_ascii(dec) and " " not in dec:
        print("Flag: picoCTF{%s}" % dec)
