import itertools
import string
import hashlib
from tqdm import tqdm

# For each portion of the salt store the text, the range of known characters,
# and the known characters.
salt_segments = [
    ("pVOjnnmk", slice(4, 12), "bff126dc"),
    ("RGiledp6", slice(14, 22), "b3070000"),
    ("Mvcezxls", slice(2, 10), "00ffd6c3"),
]

# We know what the key/password starts with thanks to the hint.
key_password = "D1v1"

# Let's bruteforce all ascii leters and digits.
alphabet = string.ascii_letters + string.digits
# Loop through all of the unknown segments.
for idx, (salt_segment_text, salt_segment_slice, salt_segment_expected) in enumerate(
    salt_segments
):
    # Try every possible 4-character long permutation of the characters in the
    # alphabet.
    for attempt in tqdm(
        itertools.permutations(alphabet, 4),
        desc="Bruteforcing Segment %i/3" % (idx + 1),
        total=13388280,
    ):
        attempt = "".join(attempt)
        segment = attempt + salt_segment_text
        segment_hash = hashlib.md5(segment.encode()).hexdigest()
        # If the hash of the attempt and salt segment text on the range stored
        # equals the expected value, then save the portion of the password and
        # `break`` to the next segment.
        if segment_hash[salt_segment_slice] == salt_segment_expected:
            print("Found segment #%i: %s" % (idx + 1, attempt))
            key_password += attempt
            break

print("Key/Password is %s" % key_password)
