#!/usr/bin/python3 -u
import random
import string
import hashlib
import time

from Crypto.Util.number import inverse, getPrime, bytes_to_long, GCD
from sympy.ntheory.modular import solve_congruence

FLAG = open('flag.txt', 'r').read()

def CRT(a, m, b, n):
	val, mod = solve_congruence((a, m), (b, n))
	return val

def gen_key():
	while True:
		p = getPrime(512)
		q = getPrime(512)
		if GCD(p-1, q-1) == 2:
			return p, q

def get_clue(p, q, BITS):
	while True:
		d_p = random.randint(1, 1 << BITS)
		d_q = random.randint(1, q - 1)
		if d_p % 2 == d_q % 2:
			d = CRT(d_p, p - 1, d_q, q - 1)
			e = inverse(d, (p - 1) * (q - 1))
			print("Clue : ", e)
			return

def get_flag(p, q):
	start = time.time()
	ans = int(input())
	if (time.time() - start) > (15 * 60):
		print("Too long!")
		exit()
	else:
		if ans == p + q:
			print(FLAG)
		else:
			print("oops...")


#PoW

vals1 = "".join([random.choice(string.digits) for _ in range(5)])
vals2 = "".join([random.choice(string.hexdigits.lower()) for _ in range(6)])
user_input = input("Enter a string that starts with \"{}\" (no quotes) which creates an md5 hash that ends in these six hex digits: {}\n".format(vals1, vals2))
user_hash = hashlib.md5(user_input.encode()).hexdigest()

if user_input[:5] == vals1 and user_hash[-6:] == vals2:
	p, q = gen_key()
	n = p * q
	print("Public Modulus : ", n)
	get_clue(p, q, 20)
	get_flag(p, q)
