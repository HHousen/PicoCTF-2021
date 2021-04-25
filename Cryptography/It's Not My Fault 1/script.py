import re
import hashlib
import gmpy2
from gmpy2 import mpz
from functools import partial
from multiprocessing import Pool
from pwn import *

host = args.HOST or "mercury.picoctf.net"
port = int(args.PORT or 26695)


def solve_md5(string_start, hash_end):
    idx = 0
    while True:
        test_string = string_start + str(idx)
        test_string_hash = str(hashlib.md5(test_string.encode("utf-8")).hexdigest())

        if test_string_hash[-len(hash_end) :] == hash_end:
            return test_string

        idx += 1


io = connect(host, port)

md5_pow_info = io.recvline().decode().strip()
string_start = re.findall('"(.*?)"', md5_pow_info)[0]
hash_end = md5_pow_info[-6:]

log.info(
    "MD5 PoW string must start with %s and hash must end with %s"
    % (string_start, hash_end)
)
progress = log.progress("Bruteforcing MD5 PoW")
md5_solution = solve_md5(string_start, hash_end)
progress.success("MD5 PoW String Found: %s" % md5_solution)
io.sendline(md5_solution)

progress = log.progress("Getting public modulus and clue")

n = int(io.recvline().decode().strip().replace("Public Modulus :  ", ""))
e = int(io.recvline().decode().strip().replace("Clue :  ", ""))

progress.success("Success")

BITS = 20
MAX_RANGE = 1 << BITS


def bruteforce_test(d_p, e, n, m):
    # Apply the algorithm from https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-4/
    # to check if a value for `d_p` is correct
    p = gmpy2.gcd(m - pow(m, e * d_p, n), n)

    if p > 1:
        # If the value of `d_p` is correct, then find `q` from the
        # bruteforced value of `p`.
        n = mpz(n)
        q = n // p
        return True, (mpz(p), mpz(q))

    return False, d_p


def bruteforce_solve(e, n, m, progress, num_process=6):
    _bruteforce_test = partial(bruteforce_test, e=e, n=n, m=m)
    pool = Pool(num_process)
    # Loop through all possible values for `d_p` in chunks of 1000 using a pool
    # of worker processes.
    for return_values in pool.imap(_bruteforce_test, range(MAX_RANGE), chunksize=1000):
        # If one of the values returns `True` then return the `(p, q)` tuple.
        if return_values[0]:
            return return_values[1]
        # If the solution was not found, then log the progress
        elif return_values[1] % 1000 == 0:
            percent_complete = (return_values[1] / MAX_RANGE) * 100
            progress.status(str(round(percent_complete, 2)) + "%")


progress = log.progress("Bruteforcing RSA-CRT d_p")
m = random.randint(1000, 100_000)  # Random number as long as `m < n`
p, q = bruteforce_solve(e, n, m, progress)
progress.success("p=%i, q=%i" % (p, q))
# Add then convert the `mpz` values to string so they can be sent properly
solution = str(p + q)

io.sendline(solution)
io.interactive()
