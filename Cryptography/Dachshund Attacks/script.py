from pwn import *

host = args.HOST or 'mercury.picoctf.net'
port = int(args.PORT or 31133)
io = connect(host, port)

io.recvline()
e = int(str(io.recvline(), "ascii").split(": ")[1].strip())
n = int(str(io.recvline(), "ascii").split(": ")[1].strip())
c = int(str(io.recvline(), "ascii").split(": ")[1].strip())
print("e = %i" % e)
print("n = %i" % n)
print("c = %i" % c)

import owiener
d = owiener.attack(e, n)

# Below is based on https://rosettacode.org/wiki/RSA_code#Python
decrypted_text = pow(c, d, n)
print("Flag: %s" % binascii.unhexlify(hex(decrypted_text)[2:]).decode())  # [2:] slicing, to strip the 0x part 
 