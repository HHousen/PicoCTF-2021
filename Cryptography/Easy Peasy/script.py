#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host mercury.picoctf.net --port 20266 otp.py
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = 'otp.py'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'mercury.picoctf.net'
port = int(args.PORT or 20266)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
continue
'''.format(**locals())

io = start()
io.recvuntil("This is the encrypted flag!\n")
encrypted_flag = str(io.recvline(), "ascii").strip()
# The length of the flag is the length of the encrypted flag divided by 2
# because of line 19 (`"{:02x}".format(ord(p) ^ k)`) where string formatting
# is used to output the flag as a hexadecimal string where each character is
# represetned by 2 characters.
flag_len = int(len(encrypted_flag)/2)

# Create a filler payload to reset the `c` variable in `otp.py` to 0 so we
# can use the same key that was used to encrypt the flag.
filler = "a"*(50000-flag_len)
io.sendlineafter("What data would you like to encrypt? ", filler)

def xor_list_str(a, b):
    # `a` is a list and `b` is a string
    return ''.join(list(map(lambda p, k: chr(p ^ ord(k)), a, b)))

def hex_to_dec_list(input_hex):
    # Convert a hex string to a decimal array.
    # Split the hex string into groups of 2.
    input_hex = [input_hex[i:i+2] for i in range(0, len(input_hex), 2)]
    # Convert each two hex characters to decimal.
    output = [int(x, 16) for x in input_hex]
    return output

# Create a message that we know that is the same length as the flag so
# that the same key is used to encrypt it.
message = "a"*flag_len

io.sendlineafter("What data would you like to encrypt? ", message)
io.recvuntil("Here ya go!\n")

encrypted_message = str(io.recvline(), "ascii").strip()
# Convert the encrypted message output by the program to a list of decimal
# numbers.
encrypted_message = hex_to_dec_list(encrypted_message)
# Find the key by xoring the encrypted message with the known clear text
# message as described at https://cs.stackexchange.com/a/365.
key = xor_list_str(encrypted_message, message)
log.success("Found Key: %s" % key)

# Convert the encrypted flag output by the program to a list of decimal
# numbers that represent ascii characters.
encrypted_flag = hex_to_dec_list(encrypted_flag)
# Decrypt the flag by xoring it with the key.
flag = xor_list_str(encrypted_flag, key)

log.success("Found Flag: picoCTF{%s}" % flag)
